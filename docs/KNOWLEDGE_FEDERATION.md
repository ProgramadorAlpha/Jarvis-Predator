# Federación de conocimiento: Jarvis, Klyp y mentores

## Objetivo

La memoria del ecosistema no es un único prompt ni un megagrafo. Se compone de tres índices especializados y un mapa ejecutivo que decide cuál consultar.

| Pregunta | Índice primario | Evidencia final |
|---|---|---|
| Arquitectura, interfaz, herramientas y control local | Grafo de Jarvis Predator | Código y documentos de Jarvis |
| Oferta, clientes, embudos, campañas y servicios | Grafo canónico de Klyp Agencia | Documentos y entregables de Klyp |
| Estrategia atribuible a un mentor | RAG de mentores | Fragmento citado: mentor, título, URL y minuto/página |

## Índices

### 1. Jarvis Predator — control local

El snapshot compartido está en `graphify-out/`. Es el punto de entrada para saber qué módulos controlan interfaz, ejecución, herramientas, memoria o mensajería local.

### 2. Klyp Agencia — operación comercial

El repositorio canónico es `ProgramadorAlpha/Klyp-Agencia_marketing-IA`; la carpeta de trabajo master es `agencia-marketing-ia`, sin sufijo. Los worktrees con sufijos de proveedor no son fuente de verdad. Su registro portable vive en [`../knowledge-federation/klyp-agency-index.json`](../knowledge-federation/klyp-agency-index.json).

### 3. Mentores — RAG de evidencia

El catálogo [`../knowledge-federation/mentor-rag-catalog.json`](../knowledge-federation/mentor-rag-catalog.json) solo describe cobertura y rutas de consulta. Las transcripciones, vídeos, libros y vector DB permanecen en la biblioteca canónica y no se copian aquí. Una respuesta basada en mentor debe recuperar la evidencia original y citarla.

## Mapa ejecutivo

El fichero [`../knowledge-federation/executive-map.json`](../knowledge-federation/executive-map.json) contiene las relaciones de operación entre dominios. Cada enlace declara si está **activo** o **planificado**:

- Jarvis es el centro de mando local.
- Klyp define y entrega la operación de marketing.
- El RAG de mentores aporta evidencia para decisiones y playbooks.
- Cortana/Hermes es el canal de ejecución y avisos en VPS.
- La publicación social automatizada es un flujo planificado: no debe presentarse como producción hasta que tenga evidencia de publicación y verificación.

## Actualización segura

Ejecuta, desde este repositorio, con rutas locales explícitas:

```powershell
python scripts/build_federated_indexes.py `
  --agency-root $env:KLYP_AGENCY_ROOT `
  --mentor-root $env:MENTOR_RAG_ROOT `
  --vector-chunks 9276
```

El script lee solo el snapshot de Klyp y los `metadata.json` de mentores. No envía transcripciones a Gemini ni lee claves. Después valida con:

```powershell
python scripts/validate_knowledge_federation.py
```

El proceso semanal publica solamente los catálogos y el mapa ejecutivo cuando cambian. No publica material bruto de mentores ni datos de clientes.
