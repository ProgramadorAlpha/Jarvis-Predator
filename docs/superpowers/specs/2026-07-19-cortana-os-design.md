# Cortana OS — Diseño del Sistema
**Fecha:** 2026-07-19
**Estado:** Aprobado en sesión de brainstorming con Jose Luis
**Siguiente paso:** Plan de implementación de F0 (skill writing-plans)

## 1. Visión

Un asistente-sistema operativo personal ("Cortana") que opera 24/7 como chief of staff de un CEO:
conoce a Jose Luis (metas, negocio, disciplina personal), planifica su día en bloques de tiempo
exactos y medibles, vigila su CRM y sus finanzas, consulta su segundo cerebro de mentores, y le
habla por Telegram (y más adelante por voz vía Jarvis).

Documento maestro de prioridades: `BUILD_IT_LEGACY_90_DIAS.md` (raíz de este repo), que además
define reglas de lectura explícitas para Cortana (briefings, follow-ups <24h, revisión dominical,
confirmación antes de acciones externas).

## 2. Decisiones tomadas

| Decisión | Elección | Alternativas descartadas |
|---|---|---|
| Runtime/cuerpo de Cortana | Harness estilo Hermes/OpenClaw (open source, gateway Telegram, crons, memoria, skills) | Claude Code como cerebro; evolucionar Jarvis en Python |
| Dónde corre | VPS Hostinger ya existente (24/7 real) | Laptop con WSL2; mini-PC casero |
| Cerebro principal | Claude Pro (suscripción, auth tipo Claude Code) | API de pago |
| Cerebro barato/masivo | Ollama (GLM / Kimi) para indexado, resúmenes, clasificación | — |
| Cerebro multimodal/rápido | Gemini (key ya en uso en Jarvis) | Grok — descartado: la suscripción de consumidor no da acceso programático |
| CRM | El propio: CRM BuildItNow (Firebase) | Notion (queda opcional para docs) |
| Rol de Jarvis Predator | Front-end de voz en la laptop (Gemini Live); se conecta a Cortana en F5. No se toca antes | Convertirlo en el OS |

## 3. Arquitectura

```
Tú ── Telegram ─────────────┐
Tú ── voz (Jarvis, laptop) ─┤──▶ CORTANA (harness en VPS Hostinger, 24/7)
                            │      ├─ Identidad: SOUL/persona + BUILD_IT_LEGACY_90_DIAS.md
                            │      ├─ Memoria persistente + segundo cerebro (conocimiento/)
                            │      ├─ Crons: planificación nocturna, briefing matutino,
                            │      │        revisión dominical, vigilancia follow-ups <24h
                            │      ├─ Apps propias (Firebase, repos privados):
                            │      │    · CRM BuildItNow  ◀ webhooks / API ▶
                            │      │    · Finanzas Pro    ◀ API ▶
                            │      │    · Life OS "Arquitecto de Sistemas" ◀ API ▶
                            │      ├─ Expertos: agentes ECC (marketing, finanzas, outbound…)
                            │      └─ Seguridad: confirmación por Telegram antes de toda
                            │              acción externa (contactar, reservar, enviar, registrar)
```

### Apps propias a integrar (F2)

| App | Repo | Stack | URL | Notas |
|---|---|---|---|---|
| CRM BuildItNow | github.com/ProgramadorAlpha/CRM-BuilditNow (privado) | Next.js + Firebase (Firestore, Cloud Functions: `ai`, `alerts`, `auth`, `emails`, `events`, `leads`, `reports`) | crm-builditnow.web.app | Ya conectado a Google Ads y ElevenLabs; soporta webhooks |
| Finanzas Pro | github.com/ProgramadorAlpha/Finanzas-Pro (privado) | TypeScript + Firebase | finanzas-pro-app-2026.web.app | Net worth, presupuestos, bóveda cifrada (HMAC/vault docs en repo) |
| Life OS "Arquitecto de Sistemas" | github.com/ProgramadorAlpha/Arquitecto-de-Sistemas (privado) | JavaScript + Firebase, carpeta `api` | arquitecto-sistemas-2026.web.app | Rituales, bloques, rachas. Jose Luis quiere monetizarlo |

**Principio de integración (por monetización futura):** Cortana se conecta como *cliente externo*
vía API/webhook genéricos. Cero lógica de Cortana dentro de las apps; la integración con
asistentes IA se convierte en feature vendible del producto.

## 4. Reparto de cerebros (economía de tokens)

- **Claude Pro** → razonamiento, planificación, orquestación, conversación principal.
- **Ollama (GLM/Kimi)** → trabajos masivos: indexar `conocimiento/`, resúmenes, clasificación.
- **Gemini** → visión/multimodal y tareas rápidas; además sigue siendo el cerebro de voz de Jarvis.

## 5. Fases

Cada fase tiene su propio ciclo plan → ejecución → verificación. No se avanza sin criterio de éxito cumplido.

- **F0 — Cimientos.** Harness instalado en el VPS (Docker), bot de Telegram creado y whitelisted,
  auth de Claude Pro + Ollama + Gemini, identidad de Cortana escrita (quién es Jose Luis, tono,
  reglas de seguridad, doc de 90 días como contexto maestro).
  ✅ *Éxito: conversación por Telegram con contexto personal y persistencia entre sesiones.*
- **F1 — Ritual CEO.** Cron nocturno (propuesta del día siguiente en bloques exactos), briefing
  matutino, revisión dominical con las métricas del doc de 90 días.
  ✅ *Éxito: ciclo noche→día→domingo funcionando una semana completa.*
- **F2 — Conexión con las 3 apps.** Inventario de endpoints/webhooks reales (leyendo los repos),
  puente seguro (service account Firebase / API keys en el VPS), Cortana suscrita a eventos del
  CRM (lead nuevo, cambio de fase, conversiones) y escribiendo los bloques del día en el Life OS.
  ✅ *Éxito: briefing matutino cruza Life OS + CRM + Finanzas; planificación nocturna escribe
  bloques reales en el Life OS.*
- **F3 — Segundo cerebro.** Estructura de `conocimiento ejemplo/` promovida a conocimiento real
  en el workspace del VPS; indexado con Ollama; Cortana lo consulta al aconsejar.
- **F4 — Expertos y proactividad.** Agentes ECC importados como skills del harness; heartbeat
  proactivo (avisos sin que se le pregunte).
- **F5 — Voz.** Jarvis (laptop) conectado a Cortana (VPS): misma memoria e identidad, dos cuerpos.

## 6. Seguridad

- Whitelist: solo el Telegram de Jose Luis puede hablar con Cortana.
- Confirmación obligatoria antes de acciones externas (mensajes, reservas, escritura en CRM/apps),
  como exige la sección "Lectura para Cortana" del doc de 90 días.
- Secretos solo en variables de entorno del VPS; nunca en repos.
- Backup del workspace de Cortana en repo git privado.
- ⚠️ Hallazgo a corregir en F2: `Finanzas-Pro` tiene un `.env` committeado en la raíz del repo
  (privado, pero mala práctica). Rotar esos secretos y sacarlo del historial cuando toquemos esa app.

## 7. Fuera de alcance (por ahora)

- Modificar Jarvis Predator (solo se toca en F5).
- Notion como CRM (descartado; opcional para documentación).
- Grok/xAI.
- Cambio de nombre/branding del Life OS (decisión de negocio de Jose Luis, no bloquea la integración).
