# Install & Run (minimal)

These are quick instructions to get a local demo running. Adapt based on chosen stack.

Prerequisites

- Node.js 16+ and npm (or pnpm/yarn)

Local (if using a Node/Vite scaffold)

1. From repo root:

   ```powershell
   npm install
   npm run start
   ```

   1. Open the host and port displayed by the server (e.g., <http://localhost:3000>).

No-backend demo

- If you prefer a static/demo-only build, keep processing client-side and persist to IndexedDB/localStorage.

Deployment

- Use Vercel or Netlify for quick deploys; configure build as `npm run build` and deploy the `dist` folder.

If you want I can scaffold a minimal Vite + React starter and add the demo-mode placeholder. Let me know and I'll create it.
