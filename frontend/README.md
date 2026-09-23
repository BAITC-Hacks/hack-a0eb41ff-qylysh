# MoneyGraph — AML Network Analysis

Frontend analyst workspace with a summary dashboard, local Cytoscape network, priority queue, node details, clusters, methodology, and data limitations. It uses the real backend by default. Set `VITE_USE_MOCK_API=true` for explicitly labelled demonstration fixtures.

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

`VITE_API_URL` can be set in a local `.env` file. Its default is `http://localhost:8000/api/v1`. Run the backend analytical snapshot before starting the API. `VITE_USE_MOCK_API=false` (the default) calls the real API; set it to `true` for labelled demonstration fixtures. Use `VITE_MOCK_SCENARIO=success`, `empty`, or `error` to verify UI states. API GIDs are decimal strings because the dataset's 18-digit identifiers exceed JavaScript's safe integer range. The current API field and browser checks are recorded in `../docs/INTEGRATION_STATUS.md`.

Detailed chapter prompts and the original frontend handoff report are in `../docs/FRONTEND_CHAPTER_PROMPTS.md` and `../docs/FRONTEND_IMPLEMENTATION_REPORT.md`.
