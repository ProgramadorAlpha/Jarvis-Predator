## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Federated knowledge routing

Do not combine every business source into this repository's graph. Route by question:

- **Jarvis / local control:** use this repository's `graphify-out/graph.json` first.
- **Klyp agency services, clients, offers, or marketing operations:** read `knowledge-federation/klyp-agency-index.json`, then query the canonical Klyp graph identified there.
- **Mentor advice, claims, or strategy evidence:** read `knowledge-federation/mentor-rag-catalog.json`, then use the canonical RAG query tool. Cite mentor, title, URL and time/page; do not treat catalogue metadata as evidence.
- **Cross-domain architecture:** start with `docs/KNOWLEDGE_FEDERATION.md` and `knowledge-federation/executive-map.json`.

External source roots are configured outside Git through `KLYP_AGENCY_ROOT` and `MENTOR_RAG_ROOT`. Never add those roots, API keys, vector databases, transcripts, or source media to this repository.
