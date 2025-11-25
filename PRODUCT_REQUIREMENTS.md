# PulseCraft — Product Requirements Document (PRD)

Last updated: 2025-11-25

This document orients development for the PulseCraft hackathon project and provides a step-by-step roadmap to ship a compelling MVP and a judge-ready demo.

Relevant resources (in this workspace):

- `Hackathon Challenge track and Rules.pdf`

- `PulseCraft Concept Description.pdf`

## 1) Background & Objective

PulseCraft aims to [short description from concept]. The objective for the hackathon is to deliver a working, demonstrable MVP that addresses the core user problem, meets hackathon rules, and is easy to present to judges.

Primary success criteria:

- A live, interactive demo that implements the core value proposition.

- Clear metrics / qualitative evidence the product solves the stated problem.

- A concise slide/video demo and working repo with run instructions.

## 2) Constraints & Assumptions

- Follow all rules and allowed resources from `Hackathon Challenge track and Rules.pdf` (eligibility, third-party libraries, IP rules, judging criteria).

- Timebox: treat the hackathon as a 48–72 hour event. Plan deliverables accordingly.

- Team size and skills: assume at least one frontend, one backend, one designer (or generalist) available.

- Infrastructure: prefer simple, reliable cloud services or local-first stacks to reduce ops overhead.

## 3) The Contract (short)

- Inputs: user actions (signup/login optional), sensor/data input (if applicable), configuration/settings.

- Outputs: UI responses, visualizations, saved data (local or remote), shareable demo mode.

- Error modes: network failures, missing sensors/permissions, invalid inputs.

- Success: end-to-end demo reproduces core scenario with data flow from input to visible output and logs.

## 4) MVP (must-have for hackathon)

Focus on the smallest set that shows the product's core value.

- Core Feature 1 — Primary Flow
  - Description: implement the main use case that demonstrates the product value (e.g., capture -> process -> visualize).
  - Acceptance criteria: user can perform the flow in under 60s; output is accurate/meaningful for demo.

- Core Feature 2 — Basic UI
  - Description: minimal, responsive UI to trigger and view results.
  - Acceptance criteria: clean, readable screens for primary flow and results; contains a demo button.

- Core Feature 3 — Persistence & Sharing
  - Description: persist demo data so results are reproducible; include a share or export option for judges.
  - Acceptance criteria: results saved & reloaded; export as JSON or screenshot possible.

- Core Feature 4 — Demo Mode & Slides
  - Description: a scripted demo flow (buttons or pre-recorded data) plus a short slide deck or 2–3 minute video explaining impact.
  - Acceptance criteria: demo can be replayed reliably during judging or recorded for submission.

## 5) Nice-to-have (if time permits)

- Authentication & user accounts

- Real-time collaboration or remote demo capability

- Advanced analytics / ML model improvements

- Hardware integration (if applicable) with graceful fallback to simulated data

## 6) User Stories (prioritized)

1. As a user, I want to trigger the primary flow so I can get a result I can act on. (MUST)

- Acceptance: flow completes with a visible result and confidence/score.

1. As a user, I want to view historical results so I can compare outcomes. (MUST)

- Acceptance: list or timeline shows saved results.

1. As a demo presenter, I want a Demo Mode that replays a recorded session. (MUST)

- Acceptance: one-click replay.

1. As an evaluator, I want an export of results and a short README so I can reproduce the demo. (MUST)

- Acceptance: exported file is reproducible and README has reproduction steps.

Edge cases to consider:

- No network connectivity — app must still allow demo playback using saved or simulated data.

- Missing permissions for sensors — fallback to simulated inputs and show clear messaging.

- Large input files — enforce limits and show progress/abort controls.

## 7) Suggested Tech Stack (pick what your team already knows)

- Frontend: React (Vite) or plain HTML/JS if time-constrained. Keep UI minimal and responsive.

- Backend: Node.js + Express (fast to iterate) or serverless functions (Vercel, Netlify). Alternatively, a static app with client-side logic and local persistence (IndexedDB) to reduce ops overhead.

- Data store: lightweight—SQLite, localStorage/IndexedDB, or Firebase (if team has an account).

- CI/CD: GitHub Actions for quick build/test and deployment to Vercel/Netlify.

- Optional: small ML model or inference via a microservice (Python/Flask) or client-side TF.js if relevant.

## 8) Architecture (high-level)

- Single-page app (SPA) or multi-page with these modules:
  - UI / Presentation
  - Core processing (client or server)
  - Data persistence & export
  - Demo Mode controller (record/replay)

Show diagram in the repo README if helpful (simple ASCII or image).

## 9) Testing & QA Plan

- Quick unit tests for critical logic (Node: jest / vitest). Keep tests minimal and fast.

- End-to-end smoke test: script that opens the app and runs Demo Mode (Cypress or Puppeteer optional).

- Manual checklist for demo run (see Demo checklist below).

## 10) Milestones & Timeline (48–72 hour friendly)

- Hour 0–4: Team alignment, finalize scope, create repo structure, basic UI skeleton.

- Hour 4–12: Implement Core Feature 1 (processing pipeline) + basic persistence.

- Hour 12–20: Implement UI flows and Demo Mode; wire persistence and export.

- Hour 20–30: Polish UI, write README, add demo script/video, tests and CI.

- Hour 30–48+: Buffer for bugs, polish, and rehearsed demo recording.

Assign owners and small tasks per milestone (one-liners in the repo Issues).

## 11) Demo Checklist (for judges)

- Clear 2-minute opening slide: problem, approach, impact.

- Live demo: user runs the primary flow from start to finish.

- Reproduce saved result and export/share it.

- Show resilience: offline/demo mode or fallback.

- Link to repo with run instructions and demo video.

## 12) Repository & Deliverables

- Add `README.md` with one-command run instructions.

- Add `docs/demo.mp4` (optional) and `docs/slides.pdf`.

- Ensure `package.json` scripts: start, build, test.

## 13) Risks & Mitigations

- Risk: time pressure — Mitigation: prioritize demo reliability over extra features.

- Risk: hardware dependencies — Mitigation: provide simulated data path.

- Risk: deployment / network flakiness — Mitigation: local-first demo mode and recorded video fallback.

## 14) Next steps (initial)

1. Confirm team roles and accept this PRD. (Owner: Team lead)

2. Create repo issues for each MVP user story and assign owners. (Owner: Team lead)

3. Start implementation using the timeline above. (Owner: Devs)

---
If you want, I can now:

- create a `PulseCraft/ROADMAP.md` with a task list split into issues and a calendar-style timeline, or

- open a small starter commit with a Vite + React scaffold and a Demo Mode placeholder.

Reference the hackathon rules file for final submission requirements: `Hackathon Challenge track and Rules.pdf`.

## 15) Azure-specific architecture & host resources

We will target Azure for the production-grade version and use a cloud-friendly, judge-safe subset for the hackathon MVP. Below is a concise architecture, how the host-provided resources map to our work, and an ops checklist.

Host-provided resources (from hackathon):

- Azure Synapse Retail Recommender Solution Accelerator — reference for building recommender pipelines and dataset patterns we can adapt for propensity scoring and product/offering ranking.

- Azure AI Foundry synthetic data guidance — use to generate realistic demo data and to justify synthetic inputs in the event of data privacy constraints.

- eShopLite sample app — gives a small e-commerce data model and user flows (sample events, checkout, product metadata) we can mirror for demo scenarios.

- ai-tour / DIY dataset + MCP examples — Multi-agent patterns, MCP examples, and small dataset integration that are useful for designing our agent-team approach for personalization.

How these resources will be used in PulseCraft:

- Use the eShopLite data schema as a demo dataset (customers, events, products) and map it to our `capture -> feature -> score -> message` pipeline.
- Leverage Synapse patterns for batch propensity scoring and feature store ideas; for the hackathon we'll implement a lightweight stand-in (simple scoring functions or Azure ML inference endpoint).
- Use AI Foundry synthetic-data guidance to generate reproducible demo sessions and to support offline demo mode.
- Use the MCP examples to model agent responsibilities and the interactions between agents (enricher, scorer, composer, compliance filter).

Azure service mapping (MVP-focused)

- Frontend: Static Web App (Azure Static Web Apps) or Vercel
  - Purpose: host the demo UI, Demo Mode controls, and visualizations.

- Orchestration Layer: Azure Functions (HTTP-triggered) or Azure App Service (Node/Express)
  - Purpose: single endpoint to trigger Demo Mode, orchestrate agent calls, persist results.

- Agent Workers: Azure Container Instances (ACI) for quick containers, or Azure Functions for small stateless agents
  - Purpose: run Enricher Agent, Scorer Agent, Composer Agent, Compliance Agent.

- Models / LLMs: Azure OpenAI (text generation) or Azure ML endpoints
  - Purpose: generate message variants, apply more advanced reasoning when available.
  - Fallback: deterministic templates + simple rule-based composer when OpenAI is unavailable.

- Storage: Azure Cosmos DB (JSON store) + Blob Storage (session recordings, exports)
  - Purpose: persist demo sessions, export JSON, host demo assets.

- Messaging / Replay: Azure Service Bus or Event Grid
  - Purpose: record events and allow replay for Demo Mode.

- Secrets: Azure Key Vault
  - Purpose: store API keys (Azure OpenAI, storage connection strings) securely.

- CI/CD: GitHub Actions -> Azure Static Web Apps / Azure Functions
  - Purpose: automatic build and deploy for quick demo iterations.

- Observability: Application Insights
  - Purpose: capture demo telemetry and simple health checks for judging.

Demo-mode and offline fallback

- Always include a "Demo Mode" which uses recorded synthetic sessions stored in Blob Storage. Demo Mode should not require live access to paid services.
- If Azure OpenAI is not available or a quota error occurs, the orchestrator will switch to a local template-based composer and log the substitution in telemetry.
- Provide a reproducible JSON export of the demo session (events + generated messages) so judges can reproduce results without cloud access.

Security, costs, and quick ops checklist

- Confirm Azure subscription and tenant access for at least one team member. If not available, we must prefer local-first solutions.
- Check Azure OpenAI access and any pre-approval requirements — if not pre-approved, use the fallback path.
- Create a Key Vault and store keys for storage, OpenAI (if used), and any other secrets.
- Use resource tagging and a strict cost budget. Limit live calls to paid APIs in the demo flow.
- For production-like runs, provision ACI or small App Service plans. For hackathon, prefer serverless (Functions + Static Web Apps) to minimize ops.

Compliance & IP notes (from hackathon rules)

- Document any third-party sample code used (eShopLite, Synapse accelerator). Include attribution and links in the repo.
- If you use datasets that contain PII, replace with synthetic data (see AI Foundry guidance) and document the transformation.

Actionable next steps (Azure path)

1. Verify Azure access / OpenAI approvals and add credentials to Key Vault. (Owner: Ops)
2. Add Demo Mode recorded session(s) to `docs/demo-sessions/` (JSON) and wire a replay endpoint. (Owner: Frontend)
3. Implement orchestrator endpoints in `api/` (Azure Functions) with a toggle for live vs recorded mode. (Owner: Backend)
4. Implement minimal agent workers (ACI-friendly container or Functions) that run simple deterministic scoring/composition and later wire Azure OpenAI for richer outputs. (Owner: Backend/ML)
5. Create GitHub Actions workflow for build and deploy to Azure Static Web Apps and Azure Functions. (Owner: DevOps)

References and quick links

- Synapse Retail Recommender: <https://github.com/microsoft/Azure-Synapse-Retail-Recommender-Solution-Accelerator>
- AI Foundry synthetic data guide: <https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/concept-synthetic-data?view=foundry-classic>
- eShopLite sample app: <https://github.com/Azure-Samples/eShopLite>
- MCP/agent examples: <https://github.com/microsoft/ai-tour-26-zava-diy-dataset-plus-mcp>

