# MoneyGraph backend chapter prompts

These prompts turn the 12-part implementation roadmap into isolated, reviewable stages. Run them in numeric order. Each chapter must preserve all contracts and tests from earlier chapters, must not implement later chapters, and must finish with tests and an explicit checklist.

Roadmap source: the shared architecture discussion supplied for this project. The files below expand its chapter summaries into executable implementation prompts.

| Chapter | Implementation status |
|---|---|
| 1. Foundation | Complete |
| 2. Ingestion | Complete |
| 3. Directed graph | Complete |
| 4. Features | Complete |
| 5. Role engine | Complete |
| 6–12 | Prompt ready; implementation pending in order |

1. [Chapter 1 — Foundation and contracts](01-foundation.md)
2. [Chapter 2 — Dataset loading and validation](02-ingestion.md)
3. [Chapter 3 — Directed graph construction](03-graph.md)
4. [Chapter 4 — Feature engineering](04-features.md)
5. [Chapter 5 — Role engine](05-roles.md)
6. [Chapter 6 — Role score and evidence](06-score-evidence.md)
7. [Chapter 7 — Clustering](07-clustering.md)
8. [Chapter 8 — Priority ranking](08-ranking.md)
9. [Chapter 9 — SQLite and exports](09-persistence.md)
10. [Chapter 10 — API contracts](10-api-contracts.md)
11. [Chapter 11 — FastAPI endpoints](11-api.md)
12. [Chapter 12 — Integration and regression](12-integration.md)
