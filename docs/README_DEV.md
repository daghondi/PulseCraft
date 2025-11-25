Developer quick-start

1. From the `PulseCraft` folder, install dependencies:

```powershell
npm install
```

2. Start the demo server:

```powershell
npm run start
```

3. Open http://localhost:3000 in your browser to run Demo Mode.

Notes

- The demo uses a minimal local orchestrator at `/api/demo/run` and stores sessions in `data/`.
- Replace the placeholder composer with Azure OpenAI or Azure ML calls later; use `PRODUCT_REQUIREMENTS.md` for architecture guidance.
