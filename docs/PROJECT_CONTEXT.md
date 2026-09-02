# Jarvis Predator — Contexto del proyecto

## Propósito

Jarvis Predator es la superficie local de interacción y control: integra voz, interfaz de escritorio, planificación, ejecución de herramientas, memoria y mensajería. Dentro del ecosistema de Jose, Jarvis es el centro de mando local; Cortana/Hermes vive en el VPS y opera como asistente conversacional y de avisos.

## Mapa de conocimiento

El mapa técnico compartido está en [`../graphify-out/graph.html`](../graphify-out/graph.html). Su fuente de datos es [`../graphify-out/graph.json`](../graphify-out/graph.json) y su auditoría es [`../graphify-out/GRAPH_REPORT.md`](../graphify-out/GRAPH_REPORT.md).

Antes de investigar arquitectura o impacto de cambios:

1. Consulta el grafo con `graphify query`, `graphify path` o `graphify explain`.
2. Abre solamente los archivos y líneas que el subgrafo señale.
3. Trata el grafo como un índice: el código y los documentos fuente son la evidencia final.

No cargues el JSON completo en un prompt ni lo uses como sustituto de las fuentes.

## Límites del sistema

- **Jarvis Predator:** interfaz y ejecución local.
- **Cortana / Hermes:** automatización y mensajería en VPS; no copiar secretos del VPS a este repositorio.
- **Klyp / agencia de marketing:** opera en su propio espacio de conocimiento. Sus procesos y clientes no deben mezclarse automáticamente con la arquitectura de Jarvis.
- **Mentores:** se consultan desde el RAG canónico con citas; un grafo ayuda a orientarse, pero no reemplaza transcripciones ni evidencia.

## Mantenimiento del grafo

- Los hooks de Git actualizan de forma local el mapa de **código** después de commits o cambios de rama, sin usar un modelo externo.
- Los cambios de documentos, PDFs o imágenes requieren extracción semántica. Se procesan con Gemini únicamente para los archivos modificados y usando caché.
- La revisión semanal controla cambios semánticos y respeta el límite operativo definido para Gemini.
- Nunca guardar `GEMINI_API_KEY`, `GOOGLE_API_KEY`, tokens, `.env`, cachés ni rutas absolutas de usuario en Git.

## Arranque para colaboradores

1. Ejecuta `powershell -ExecutionPolicy Bypass -File scripts/bootstrap_graphify.ps1`.
2. Para análisis semántico, configura `GEMINI_API_KEY` como variable de entorno de usuario; no la escribas en archivos del repositorio.
3. Lee este archivo y `AGENTS.md` antes de modificar arquitectura, automatización o memoria.
