# Test Plan

This document lists quick tests and QA checks for the PulseCraft MVP. Keep tests minimal and quick to run.

Smoke tests (manual)

- Start the app and run the Demo Mode end-to-end.
- Verify results persist and can be reloaded.
- Verify export/import produces the same viewable result.

Unit tests (automated)

- Processing function: given known input, produce expected output.
- Persistence: save and load roundtrip returns equivalent data.

Edge cases

- No network: demo mode should run with saved/simulated data.
- Missing sensor permissions: show a clear fallback message and use simulated data.
- Large input: enforce file-size limits and show progress.

QA checklist for demo

- Demo Mode completes within expected time.
- Saved results are reproducible.
- README has exact run steps for judges.

Add automated tests as time permits (vitest/jest) and a small e2e smoke script if time allows (Puppeteer/Cypress).
