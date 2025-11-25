# PulseCraft

PulseCraft is a modular agent-based platform that personalizes outbound customer experiences for subscription and consumer brands by turning behavioral signals and model-driven propensities into safe, on-brand messages with traceable content provenance and measurable uplift.

This repository contains the hackathon-ready code, documentation, and demo assets for the PulseCraft MVP. See the `PRODUCT_REQUIREMENTS.md` for the full PRD.

## Repository Structure

```text
PulseCraft/
├── backend/              # Backend API server (Node.js + Express)
│   ├── routes/          # API route handlers
│   ├── server.js        # Main server entry point
│   ├── package.json     # Backend dependencies
│   └── .env.example     # Environment variables template
├── frontend/            # Frontend web application
│   ├── public/          # Static assets (HTML, CSS, JS)
│   ├── package.json     # Frontend dependencies
│   └── .env.example     # Frontend environment template
├── agents/              # AI agent modules
│   ├── enricher.js      # Customer data enrichment agent
│   ├── scorer.js        # Opportunity scoring agent
│   ├── composer.js      # Message composition agent
│   └── compliance.js    # Compliance validation agent
├── docs/                # Project documentation
│   ├── ROADMAP.md       # Sprint-level roadmap
│   ├── SPRINT_PLAN.md   # Sprint-by-sprint tasks
│   ├── TEST_PLAN.md     # Test matrix and QA checklist
│   ├── INSTALL.md       # Installation instructions
│   └── CONTRIBUTING.md  # Contribution guidelines
├── .github/             # GitHub workflows and issue templates
├── PRODUCT_REQUIREMENTS.md  # Complete Product Requirements Document
└── README.md            # This file
```

## Quick Links

1. `PRODUCT_REQUIREMENTS.md` — Product Requirements Document and acceptance criteria
1. `docs/ROADMAP.md` — sprint-level roadmap and deliverables
1. `docs/SPRINT_PLAN.md` — short sprint-by-sprint tasks for the hackathon
1. `docs/TEST_PLAN.md` — test matrix and QA checklist
1. `docs/INSTALL.md` — quick start and run instructions
1. `docs/CONTRIBUTING.md` — how to contribute during the hackathon

## Quick Start (Local Demo)

### Prerequisites

1. Node.js 16+ installed
1. Git installed

### Installation

1. Clone the repository:

   ```powershell
   git clone <repository-url>
   cd PulseCraft
   ```

1. Install all dependencies (root, backend, and frontend):

   ```powershell
   npm run install:all
   ```

1. Set up environment variables:

   ```powershell
   # Backend
   cd backend
   Copy-Item .env.example .env
   # Edit .env and add your Azure credentials

   # Frontend
   cd ../frontend
   Copy-Item .env.example .env
   # Edit .env if needed (default API URL is http://localhost:3001)
   ```

### Running the Application

1. Start both backend and frontend servers:

   ```powershell
   npm run dev
   ```

   This will start:

   1. Backend API server on <http://localhost:3001>
   1. Frontend web server on <http://localhost:8080>

1. Open your browser to <http://localhost:8080>

1. Use the Demo Mode to test the core personalization flow

### Alternative: Run Servers Separately

```powershell
# Terminal 1 - Backend
npm run start:backend

# Terminal 2 - Frontend
npm run start:frontend
```

## Azure Architecture

PulseCraft leverages the following Azure services:

1. **Azure Static Web Apps** — Frontend hosting
1. **Azure Functions** — Serverless agent execution
1. **Azure Container Instances** — Long-running agent processes
1. **Azure OpenAI Service** — AI-powered scoring and message generation
1. **Azure Cosmos DB** — Customer profile and session storage
1. **Azure Blob Storage** — Historical data and analytics
1. **Azure Service Bus** — Agent-to-agent messaging
1. **Azure Key Vault** — Secure credential management
1. **Application Insights** — Monitoring and telemetry

See `PRODUCT_REQUIREMENTS.md` section 15 for detailed architecture mapping.

## Contact / Team

Add team contacts & roles here (owner, frontend, backend, designer) so judges and team members can see responsibilities.

## License

See `LICENSE` in the repository root.
