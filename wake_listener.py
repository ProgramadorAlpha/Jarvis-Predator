"""Local clap and Spanish wake phrase listener for MARK XXXIX."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import queue
import random
import re
import socket
import subprocess
import threading
import time
import unicodedata
from pathlib import Path

import numpy as np
import psutil
import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models" / "vosk-model-small-es-0.42"
RUNTIME_DIR = BASE_DIR / "runtime"
LOG_DIR = BASE_DIR / "logs"
BRIEFING_PATH = RUNTIME_DIR / "startup_briefing.json"
RUN_SCRIPT = BASE_DIR / "run.ps1"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
CHROME_PROFILE = "Default"
WHATSAPP_APP_ID = (
    r"shell:AppsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
)
BAD_VIDEO_URL = "https://www.youtube.com/watch?v=dsUXAEzaC3Q&autoplay=1"
SAMPLE_RATE = 16000
BLOCK_SIZE = 1024
PHRASE_TIMEOUT = 12.0
SINGLE_INSTANCE_PORT = 47639

_BRIEFING_PREFIX = (
    "This is an internal startup event. Do not call any tool. "
    "Speak the following Spanish welcome naturally, as JARVIS would: "
)

BRIEFINGS = [
    # 1 — clásico con datos de sistema
    _BRIEFING_PREFIX + (
        "\"Buenos días. Sistemas completamente operativos. Procesador al 11%, "
        "memoria disponible al 70%, red estable. Tienes notificaciones pendientes "
        "y tus proyectos activos siguen en marcha. ¿En qué trabajamos hoy?\""
    ),
    # 2 — mercados y productividad
    _BRIEFING_PREFIX + (
        "\"Bienvenido de nuevo. El mercado ha abierto al alza hoy, con el sector "
        "tecnológico liderando subidas. Sin alertas críticas en el sistema. "
        "Todo listo para que empieces a producir. A sus órdenes.\""
    ),
    # 3 — clima y estado general
    _BRIEFING_PREFIX + (
        "\"Conexión establecida. He revisado el estado del sistema: todo nominal. "
        "Sin procesos anómalos ni amenazas detectadas. "
        "¿Cuál es la misión de hoy?\""
    ),
    # 4 — nocturno / sesión tardía
    _BRIEFING_PREFIX + (
        "\"Inicio de sesión registrado. El sistema lleva activo sin incidencias. "
        "Todos los módulos funcionando al 100%. "
        "Listo para recibir instrucciones. ¿Continuamos donde lo dejaste?\""
    ),
    # 5 — directo y conciso
    _BRIEFING_PREFIX + (
        "\"Sistemas en línea. Red estable, latencia mínima. "
        "Sin alertas pendientes. "
        "A la espera de instrucciones.\""
    ),
    # 6 — foco en proyectos
    _BRIEFING_PREFIX + (
        "\"Bienvenido. He revisado tus proyectos activos y todo sigue en orden. "
        "Tienes tareas pendientes que podrían necesitar tu atención hoy. "
        "¿Por dónde empezamos?\""
    ),
    # 7 — arranque rápido y motivador
    _BRIEFING_PREFIX + (
        "\"Arranque completado. Todos los sistemas operativos y sin errores. "
        "Es un buen momento para ser productivo. "
        "Dime qué necesitas y lo gestionamos.\""
    ),
    # 8 — estilo Iron Man
    _BRIEFING_PREFIX + (
        "\"Conexión activa, señor. Diagnóstico completo superado. "
        "Traje Mark treinta y nueve listo para operar. "
        "¿Cuál es el plan para hoy?\""
    ),
    # 9 — informe de estado completo
    _BRIEFING_PREFIX + (
        "\"Sistema iniciado correctamente. Sin actualizaciones críticas pendientes, "
        "sin amenazas de seguridad detectadas, rendimiento óptimo. "
        "Sus aplicaciones están funcionando al 100%. "
        "¿En qué puedo servirle?\""
    ),
]


def _log(message: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}"
    with (LOG_DIR / "wake-listener.log").open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line, flush=True)


def _normalize(text: str) -> str:
    value = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in value if not unicodedata.combining(ch))


def _wake_phrase_detected(text: str) -> bool:
    normalized = _normalize(text)
    words = re.findall(r"[a-z]+", normalized)
    has_wake = any(
        difflib.SequenceMatcher(None, word, "despierta").ratio() >= 0.72
        for word in words
    )
    compact = "".join(words)
    jarvis_variants = (
        "jarvis",
        "yarvis",
        "harvis",
        "jarbis",
        "yarbis",
        "yaavis",
        "yaavis",
    )
    has_name = any(variant in compact for variant in jarvis_variants)
    if not has_name:
        has_name = any(
            difflib.SequenceMatcher(None, word, "jarvis").ratio() >= 0.66
            for word in words
        )
    return has_wake and has_name


def _jarvis_processes() -> list[psutil.Process]:
    found = []
    for process in psutil.process_iter(["name", "cmdline"]):
        try:
            name = (process.info["name"] or "").lower()
            command = " ".join(process.info["cmdline"] or []).lower()
            if name == "pythonw.exe" and "main.py" in command:
                found.append(process)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return found


def _write_briefing() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    briefing = random.choice(BRIEFINGS)
    temp = BRIEFING_PATH.with_suffix(".tmp")
    temp.write_text(
        json.dumps({"created_at": time.time(), "prompt": briefing}, indent=2),
        encoding="utf-8",
    )
    temp.replace(BRIEFING_PATH)


def _hidden_popen(command: list[str], **kwargs):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    kwargs.setdefault("startupinfo", startupinfo)
    kwargs.setdefault("creationflags", subprocess.CREATE_NO_WINDOW)
    return subprocess.Popen(command, **kwargs)


def _launch_jarvis() -> None:
    if _jarvis_processes():
        return
    _write_briefing()
    python_exe = BASE_DIR / ".venv" / "Scripts" / "pythonw.exe"
    if not python_exe.exists():
        # Fallback: use the PowerShell script if the venv is missing
        _hidden_popen(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", str(RUN_SCRIPT)],
            cwd=BASE_DIR,
        )
        return

    # pythonw.exe is already windowless — no STARTUPINFO/CREATE_NO_WINDOW needed.
    # Open log handles first, pass to Popen, then close our copies (child keeps its own).
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONUNBUFFERED": "1"}
    stdout_f = open(log_dir / "jarvis.log", "a", encoding="utf-8")
    stderr_f = open(log_dir / "jarvis-error.log", "a", encoding="utf-8")
    try:
        subprocess.Popen(
            [str(python_exe), "main.py"],
            cwd=BASE_DIR,
            env=env,
            stdout=stdout_f,
            stderr=stderr_f,
        )
    finally:
        stdout_f.close()
        stderr_f.close()


def _launch_whatsapp() -> None:
    _hidden_popen(["explorer.exe", WHATSAPP_APP_ID])


def _focus_window_after_delay(title: str, delay: float) -> None:
    def worker():
        time.sleep(delay)
        try:
            from pywinauto import Desktop

            windows = [
                window
                for window in Desktop(backend="uia").windows()
                if title.lower() in window.window_text().lower()
            ]
            if windows:
                windows[0].restore()
                windows[0].set_focus()
                _log(f"Focused window: {title}.")
        except Exception as exc:
            _log(f"Could not focus {title}: {exc}")

    threading.Thread(target=worker, daemon=True).start()


def _launch_youtube_after_delay(delay: float = 10.0) -> None:
    def worker():
        time.sleep(delay)
        if CHROME.exists():
            _hidden_popen(
                [
                    str(CHROME),
                    f"--profile-directory={CHROME_PROFILE}",
                    BAD_VIDEO_URL,
                ],
                cwd=CHROME.parent,
            )
            _log("YouTube opened with Michael Jackson - Bad.")

    threading.Thread(target=worker, daemon=True).start()


def run_welcome_routine() -> None:
    _log("Wake phrase accepted; starting welcome routine.")
    _launch_jarvis()
    _launch_whatsapp()                    # independent of JARVIS — no need to wait
    _launch_youtube_after_delay(delay=5.0)  # reduced from 10s → 5s
    _focus_window_after_delay("J.A.R.V.I.S", 3)   # reduced from 4s → 3s
    _focus_window_after_delay("J.A.R.V.I.S", 8)   # reduced from 14s → 8s


def _wait_until_jarvis_stops() -> None:
    while _jarvis_processes():
        time.sleep(3)


def _is_clap(samples: np.ndarray, noise_rms: float) -> bool:
    if samples.size == 0:
        return False
    signal = samples.astype(np.float32) / 32768.0
    peak = float(np.max(np.abs(signal)))
    rms = float(np.sqrt(np.mean(signal * signal)) + 1e-9)
    crest = peak / rms
    return (
        peak >= max(0.00025, noise_rms * 8)
        and rms >= max(0.00004, noise_rms * 2.5)
        and crest >= 5.0
    )


def _is_activation_clap(samples: np.ndarray, noise_rms: float) -> bool:
    if not _is_clap(samples, noise_rms):
        return False
    signal = samples.astype(np.float32) / 32768.0
    peak = float(np.max(np.abs(signal)))
    rms = float(np.sqrt(np.mean(signal * signal)) + 1e-9)
    return peak >= 0.02 and peak / rms >= 4.5


def listen_forever(model: Model) -> None:
    audio_queue: queue.Queue[bytes] = queue.Queue(maxsize=50)

    def callback(indata, frames, time_info, status):
        del frames, time_info
        if status:
            _log(f"Audio status: {status}")
        try:
            audio_queue.put_nowait(bytes(indata))
        except queue.Full:
            pass

    while True:
        if _jarvis_processes():
            _wait_until_jarvis_stops()
            time.sleep(1)

        noise_rms = 0.00005
        clap_armed_until = 0.0
        speech_after = 0.0
        speech_blocks = 0
        last_partial = ""
        recognizer = KaldiRecognizer(model, SAMPLE_RATE)
        _log("Listening for 'despierta Jarvis' (clap optional).")

        try:
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                dtype="int16",
                channels=1,
                callback=callback,
            ):
                while not _jarvis_processes():
                    data = audio_queue.get(timeout=2)
                    samples = np.frombuffer(data, dtype=np.int16)
                    now = time.monotonic()

                    signal = samples.astype(np.float32) / 32768.0
                    rms = float(np.sqrt(np.mean(signal * signal)) + 1e-9)
                    clap = _is_clap(samples, noise_rms)
                    if clap and now > clap_armed_until:
                        clap_armed_until = now + PHRASE_TIMEOUT
                        peak = float(np.max(np.abs(signal)))
                        crest = peak / max(rms, 1e-9)
                        _log(
                            "Clap detected "
                            f"(peak={peak:.5f}, rms={rms:.5f}, crest={crest:.1f}); "
                            "evaluating activation."
                        )
                        if _is_activation_clap(samples, noise_rms):
                            clap_armed_until = now + PHRASE_TIMEOUT
                            speech_after = now + 0.4
                            speech_blocks = 0
                            _log(
                                "Strong clap accepted; waiting for voice confirmation."
                            )
                        try:
                            import winsound

                            winsound.Beep(880, 100)
                        except Exception:
                            pass
                    elif not clap:
                        noise_rms = 0.98 * noise_rms + 0.02 * min(rms, 0.01)

                    accepted = recognizer.AcceptWaveform(data)
                    result = json.loads(
                        recognizer.Result()
                        if accepted
                        else recognizer.PartialResult()
                    )
                    text = str(result.get("text") or result.get("partial") or "")
                    if text and text != last_partial:
                        last_partial = text
                        _log(f"Speech heard: {text!r}")
                    if _wake_phrase_detected(text):
                        _log(f"Recognized wake phrase: {text!r}")
                        break
                    if now <= clap_armed_until and now >= speech_after:
                        voice_threshold = max(0.001, noise_rms * 8)
                        if rms >= voice_threshold:
                            speech_blocks += 1
                        else:
                            speech_blocks = max(0, speech_blocks - 1)
                        if text or speech_blocks >= 4:
                            detail = text or f"{speech_blocks} voice blocks"
                            _log(
                                "Voice confirmed after clap: "
                                f"{detail!r}. Activating."
                            )
                            break
        except queue.Empty:
            _log("Microphone produced no data; reopening stream.")
            time.sleep(1)
            continue
        except Exception as exc:
            _log(f"Listener error: {exc}")
            time.sleep(3)
            continue

        run_welcome_routine()
        time.sleep(5)
        _wait_until_jarvis_stops()


def _single_instance_socket() -> socket.socket:
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", SINGLE_INSTANCE_PORT))
    listener.listen(1)
    return listener


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trigger",
        action="store_true",
        help="Run the welcome routine immediately for testing.",
    )
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    try:
        instance_socket = _single_instance_socket()
    except OSError:
        _log("Wake listener is already running.")
        return

    if args.trigger:
        run_welcome_routine()
        time.sleep(12)
        return

    if not MODEL_DIR.exists():
        _log(f"Spanish Vosk model is missing: {MODEL_DIR}")
        return

    SetLogLevel(-1)
    _log("Loading local Spanish speech model.")
    model = Model(str(MODEL_DIR))
    _log("Wake listener ready.")
    try:
        listen_forever(model)
    finally:
        instance_socket.close()


if __name__ == "__main__":
    main()
