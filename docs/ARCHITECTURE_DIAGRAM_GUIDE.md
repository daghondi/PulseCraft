# PulseCraft Architecture Diagram - Draw.io Guide

## Quick Import Instructions

1. Go to <https://app.diagrams.net/> (draw.io)
2. Click **File → Open From → Device**
3. Select the `pulsecraft-architecture.drawio` file (created below)
4. Or copy the XML code at the bottom and use **File → Import From → XML**

---

## Architecture Overview

This diagram shows the PulseCraft Customer Personalization Orchestrator with its multi-agent architecture and Azure services integration.

### Components to Include

#### 1. **Frontend Layer**
- User Interface (Browser)
- Azure Static Web Apps (hosting)
- HTML/CSS/JavaScript

#### 2. **API Gateway Layer**
- Express.js Backend
- Azure App Service / Azure Functions
- Port 3001 (local) or HTTPS (Azure)

#### 3. **Agent Layer** (Core Intelligence)
- **Enricher Agent**
  - Input: Customer ID
  - Data sources: Cosmos DB, Synapse, Blob Storage
  - Output: Enriched Profile
  
- **Scorer Agent**
  - Input: Enriched Profile
  - Processing: Azure OpenAI GPT-4
  - Output: Ranked Opportunities
  
- **Composer Agent**
  - Input: Ranked Opportunities
  - Processing: Azure OpenAI (message generation)
  - Output: Multi-channel Messages
  
- **Compliance Agent**
  - Input: Composed Messages
  - Validation: GDPR, Brand Safety, Regulations
  - Output: Approved/Rejected Payload

#### 4. **Azure Services Layer**
- **Azure OpenAI Service** - AI scoring and generation
- **Azure Cosmos DB** - Customer profiles and sessions
- **Azure Synapse Analytics** - Retail recommender data
- **Azure Blob Storage** - Historical data
- **Azure Service Bus** - Agent-to-agent messaging
- **Azure Key Vault** - Secrets management
- **Application Insights** - Monitoring and telemetry

#### 5. **Data Flow**
```
User Request → Frontend → API Gateway → Agent Pipeline → Response
                                           ↓
                                    Service Bus Queue
                                           ↓
              Enricher → Scorer → Composer → Compliance → Final Output
                 ↓         ↓         ↓            ↓
            [Data Sources] [Azure OpenAI] [Azure OpenAI] [Rules Engine]
```

---

## Manual Drawing Instructions (if not using XML)

### Step 1: Create Layers (Top to Bottom)

1. **User/Client Layer** (Top)
   - Rectangle: "User Browser"
   - Arrow down to Frontend

2. **Frontend Layer**
   - Rectangle: "Frontend UI (React/HTML)"
   - Cloud icon: "Azure Static Web Apps"
   - Arrow down labeled "HTTP/HTTPS"

3. **Backend/API Layer**
   - Rectangle: "Express.js API Server"
   - Cloud icon: "Azure App Service / Functions"
   - Arrows down to Agent Layer

4. **Agent Orchestration Layer**
   - Container/Swimlane with 4 agents
   - Connect with Service Bus

5. **Azure Services Layer** (Bottom)
   - Multiple cloud icons for each service

### Step 2: Add Agents (Left to Right)

For each agent, create a process box with:
- Name (e.g., "Enricher Agent")
- Input/Output labels
- Connection to Azure service below

```
┌─────────────────┐
│ Enricher Agent  │
├─────────────────┤
│ Input: Customer │
│ Output: Profile │
└────────┬────────┘
         │
    ┌────▼────┐
    │Cosmos DB│
    └─────────┘
```

### Step 3: Add Data Flow Arrows

1. User → Frontend (Request)
2. Frontend → Backend API (HTTP POST)
3. Backend → Service Bus (Queue message)
4. Service Bus → Enricher Agent
5. Enricher → Scorer (via Service Bus)
6. Scorer → Composer (via Service Bus)
7. Composer → Compliance (via Service Bus)
8. Compliance → Backend API (Result)
9. Backend → Frontend (Response)
10. Frontend → User (Display)

### Step 4: Color Coding

- **Frontend**: Light Blue (#E3F2FD)
- **Backend**: Light Green (#E8F5E9)
- **Agents**: Light Orange (#FFF3E0)
- **Azure Services**: Azure Blue (#0078D4)
- **Data Stores**: Light Purple (#F3E5F5)

---

## Draw.io Shapes to Use

| Component | Shape | Style |
|-----------|-------|-------|
| User | Actor/Person icon | Default |
| Frontend UI | Rectangle with rounded corners | Blue fill |
| Backend API | Rectangle | Green fill |
| Agents | Process/Rectangle | Orange fill |
| Azure Services | Cloud shape | Azure blue |
| Databases | Cylinder | Purple fill |
| Service Bus | Queue icon / Rectangle | Yellow fill |
| Arrows | Solid arrows | Black with labels |

---

## Recommended Layout

```
                    [User Browser]
                          |
                    [Frontend UI]
                 [Azure Static Web Apps]
                          |
                  [Express.js API]
               [Azure App Service/Functions]
                          |
                  [Service Bus Queue]
                          |
        ┌─────────┬───────┴────────┬─────────┐
        ▼         ▼                ▼         ▼
   [Enricher] [Scorer]        [Composer] [Compliance]
        |         |                |         |
        ▼         ▼                ▼         ▼
   [Cosmos DB] [OpenAI]        [OpenAI]  [Rules]
        |         |                |
        └─────────┴────────────────┘
                  |
           [Application Insights]
```

---

## Alternative: Simplified Version

For presentations, you can create a simplified version:

```
┌──────────────────────────────────────────┐
│           USER INTERFACE                 │
│        (Azure Static Web Apps)           │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│         API GATEWAY                      │
│    (Azure App Service/Functions)         │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│      AGENT ORCHESTRATION LAYER           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │Enricher │→│ Scorer  │→│Composer │   │
│  └─────────┘ └─────────┘ └─────────┘   │
│                    ↓                     │
│             ┌─────────────┐              │
│             │ Compliance  │              │
│             └─────────────┘              │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│         AZURE SERVICES                   │
│  [OpenAI] [Cosmos DB] [Service Bus]     │
│  [Synapse] [Blob Storage] [Key Vault]   │
└──────────────────────────────────────────┘
```

---

## Labels to Add

### On Arrows
- "1. Customer Request"
- "2. API Call (POST /api/demo/run)"
- "3. Enqueue Message"
- "4. Enrich Profile"
- "5. Score Opportunities (AI)"
- "6. Compose Message (AI)"
- "7. Validate Compliance"
- "8. Return Personalized Content"

### Technology Stack Labels
- Frontend: "HTML/CSS/JavaScript"
- Backend: "Node.js + Express"
- Agents: "JavaScript Classes"
- AI: "Azure OpenAI GPT-4"
- Database: "Cosmos DB (NoSQL)"
- Queue: "Service Bus"

---

## Export Instructions

After creating the diagram:

1. **For Documentation**: 
   - File → Export As → PNG (300 DPI, transparent background)
   - Save as `architecture-diagram.png`

2. **For Presentation**:
   - File → Export As → PDF
   - Save as `architecture-diagram.pdf`

3. **For Editing Later**:
   - File → Save As → `pulsecraft-architecture.drawio`

4. **For README**:
   - Export PNG and add to repository
   - Reference in README.md:
     ```markdown
     ![PulseCraft Architecture](./docs/architecture-diagram.png)
     ```

---

## Advanced: Add Metrics/Numbers

You can add performance indicators:

- **Enricher**: "~50ms avg latency"
- **Scorer**: "~200ms (OpenAI call)"
- **Composer**: "~150ms (OpenAI call)"
- **Compliance**: "~10ms (rule validation)"
- **Total**: "~410ms end-to-end"

---

## Tips for Professional Look

1. **Alignment**: Use draw.io's alignment tools (Arrange → Align)
2. **Spacing**: Keep consistent spacing between components
3. **Font**: Use Arial or Helvetica, 12pt for labels, 14pt for titles
4. **Arrows**: Use solid arrows for data flow, dashed for optional/async
5. **Legend**: Add a legend box explaining colors and symbols
6. **Title**: Add title "PulseCraft - Customer Personalization Orchestrator Architecture"
7. **Version**: Add version/date in corner (v1.0 - Nov 2025)

---

## For Video Demo

When showing the architecture in your demo video:

1. Start with the full diagram
2. Zoom into each layer and explain
3. Trace a sample request flow with animation/pointer
4. Highlight Azure services being used
5. End with the complete view showing all connections

---

Good luck creating your architecture diagram! 🎨
