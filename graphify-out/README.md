# Artefactos compartidos de Graphify

Este directorio publica un mapa portable de Jarvis Predator para humanos y agentes.

- `graph.html`: visor interactivo descargable.
- `graph.json`: subgrafo y relaciones consultables por herramientas.
- `GRAPH_REPORT.md`: auditoría, cobertura y coste de extracción.
- `manifest.json`: línea base para detectar cambios incrementales.

Los archivos de caché, resultados intermedios, historial local, rutas de máquina y credenciales se ignoran deliberadamente. No añadas claves API ni archivos `.env` aquí.

Para configurar el mapa en una clonación nueva, consulta [`../docs/PROJECT_CONTEXT.md`](../docs/PROJECT_CONTEXT.md) y ejecuta `scripts/bootstrap_graphify.ps1`.
