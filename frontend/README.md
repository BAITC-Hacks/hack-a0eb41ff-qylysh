# MoneyGraph — AML Network Analysis

Frontend analyst workspace with a summary dashboard, local Cytoscape network, priority queue, node details, clusters, methodology, and data limitations. It runs with explicitly labelled demonstration fixtures by default because the domain backend endpoints are not implemented yet.

## Run locally

Requires Node.js 20.19+ or 22.12+.

Run these commands from `frontend/`:

```bash
npm install
npm run dev
```

Open the local URL printed by Vite. To check the production build:

```bash
npm run build
```

`VITE_API_URL` can be set in a local `.env` file. `VITE_USE_MOCK_API=true` uses labelled demonstration fixtures; set it to `false` to call the API. Use `VITE_MOCK_SCENARIO=success`, `empty`, or `error` to verify UI states. DTOs other than `/summary` remain frontend candidates until they are agreed with the backend contract and OpenAPI.

Detailed chapter prompts and the current verification report are in `../docs/FRONTEND_CHAPTER_PROMPTS.md` and `../docs/FRONTEND_IMPLEMENTATION_REPORT.md`.
