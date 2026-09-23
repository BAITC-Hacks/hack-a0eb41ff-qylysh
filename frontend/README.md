# MoneyGraph — AML Network Analysis

Frontend MVP foundation for the analyst workspace. This chapter includes the shared layout, navigation, GID search routing, mock overview metrics, and placeholder pages. Graph rendering and backend requests are reserved for later chapters.

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

`VITE_API_URL` can be set in a local `.env` file. See `.env.example`; no API requests are made in this chapter.
