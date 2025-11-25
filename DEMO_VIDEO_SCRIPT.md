# PulseCraft Demo Video Script

## Demo Video Outline (3-4 minutes)

This script provides a suggested flow for recording the hackathon demo video.

---

## 1. Introduction (30 seconds)

**[Screen: Title card with "PulseCraft" logo]**

> "Hi, I'm [Your Name] from Team [Team Name], and we're excited to present **PulseCraft** - a Customer Personalization Orchestrator built for the [Hackathon Name].
>
> Today's brands send generic messages that don't resonate with customers. PulseCraft solves this by using an **agent-based AI system** to deliver personalized experiences at scale, with full compliance and measurable impact."

**[Screen: Transition to problem slide showing generic vs personalized messages]**

---

## 2. Architecture Overview (45 seconds)

**[Screen: Architecture diagram showing multi-agent system]**

> "PulseCraft uses a **multi-agent architecture** powered by Azure services.
>
> Here's how it works:
>
> 1. The **Enricher Agent** pulls customer data from Azure Cosmos DB and Synapse Analytics
> 2. The **Scorer Agent** uses Azure OpenAI to rank personalization opportunities
> 3. The **Composer Agent** generates the final message using AI
> 4. The **Compliance Agent** validates everything against GDPR and brand guidelines
>
> All agents communicate through **Azure Service Bus**, making the system scalable and resilient."

**[Screen: Show Azure services icons/logos]**

---

## 3. Live Demo (2 minutes)

**[Screen: Switch to browser with frontend at localhost:8080]**

> "Let me show you PulseCraft in action. I'm running the demo locally, but this is designed to deploy on Azure Static Web Apps.
>
> **[Type customer name: "Sarah Johnson"]**
>
> I'll enter a customer name and click 'Run Demo'."

**[Click "Run Demo" button]**

**[Screen: Show loading state, then results appear]**

> "In real-time, PulseCraft has:
>
> 1. **Enriched** Sarah's profile with her purchase history and preferences
> 2. **Scored** personalization opportunities - notice she gets a 92% match score for wireless headphones based on her electronics affinity
> 3. **Composed** a personalized message with product recommendations
> 4. **Validated** compliance - all GDPR checks passed
>
> Here's the session ID generated, and you can see the full personalization payload with multi-channel content ready for email, web, and mobile."

**[Screen: Scroll through the JSON output highlighting key sections]**

> "Now let me show session management. Click 'List Sessions'."

**[Click "List Sessions" button]**

**[Screen: Show list of all sessions]**

> "We can see all previous sessions here. Let's replay the last one."

**[Click "Replay Last" button]**

**[Screen: Show replayed session data]**

> "Perfect - we can retrieve any session for auditing or A/B testing."

---

## 4. Azure Integration Highlights (30 seconds)

**[Screen: Show code or configuration highlighting Azure services]**

> "Under the hood, PulseCraft leverages several Azure services:
>
> - **Azure OpenAI** for intelligent scoring and message generation
> - **Azure Cosmos DB** for scalable customer profile storage
> - **Azure Service Bus** for reliable agent communication
> - **Application Insights** for monitoring and telemetry
> - **Azure Key Vault** for secure credential management
>
> The architecture is production-ready and designed for Azure deployment."

**[Screen: Show environment variables or Azure portal (optional)]**

---

## 5. Impact & Next Steps (30 seconds)

**[Screen: Slide showing metrics/impact]**

> "PulseCraft delivers real business value:
>
> - **Measurable uplift** in customer engagement through personalized messaging
> - **Traceable content provenance** - every recommendation is auditable
> - **Compliance-first** approach with automated GDPR validation
> - **Scalable architecture** ready for millions of customers
>
> Our next steps include:
> - Full Azure Functions deployment for production
> - Real-time personalization using Synapse Retail Recommender
> - A/B testing framework for continuous optimization"

**[Screen: Final slide with GitHub repo link and team contact]**

> "Thank you for watching! Check out our GitHub repository for the full code and documentation.
>
> We'd love to hear your feedback!"

**[End screen: PulseCraft logo, GitHub URL, team names]**

---

## Recording Tips

### Technical Setup

1. **Screen Resolution**: Record at 1920x1080 (1080p minimum)
1. **Audio**: Use a good quality microphone, quiet room
1. **Recording Software**: OBS Studio, Loom, or Camtasia
1. **Browser**: Use Chrome in Incognito mode (clean, no extensions)
1. **Preparation**:
   - Clear browser cache
   - Close unnecessary tabs and applications
   - Test microphone levels before recording
   - Have backend and frontend running and tested

### Visual Tips

1. Zoom browser to 110-125% for better readability
1. Use cursor highlighting (OBS plugin or system setting)
1. Slow down cursor movements
1. Pause briefly between sections (easier for editing)
1. Keep slides simple with minimal text
1. Use consistent branding/colors

### Speaking Tips

1. Speak clearly and at moderate pace
1. Show enthusiasm but stay professional
1. Practice the script 2-3 times before recording
1. Don't worry about minor mistakes - keep going
1. Emphasize key technical terms (Azure OpenAI, agents, etc.)
1. Smile - it comes through in your voice!

### Demo Flow Preparation

Before recording, run through this checklist:

- [ ] Backend server is running (`npm run start:backend`)
- [ ] Frontend is running (`npm run start:frontend`)
- [ ] Test a full demo flow to ensure it works
- [ ] Clear previous session data for clean demo
- [ ] Have customer names ready: "Sarah Johnson", "John Doe"
- [ ] Have slides ready in separate window/screen
- [ ] Recording software is configured and tested

---

## Editing Checklist

After recording:

- [ ] Trim dead air at beginning and end
- [ ] Add title card with PulseCraft branding
- [ ] Add captions/subtitles (recommended)
- [ ] Add music (optional, low volume)
- [ ] Add transitions between sections
- [ ] Add end screen with GitHub link and team info
- [ ] Export at 1080p, H.264 codec
- [ ] Keep final video between 3-4 minutes
- [ ] Upload to YouTube as Unlisted
- [ ] Test playback before submitting

---

## Backup Plan

If live demo fails during recording:

1. Have pre-recorded screen capture of working demo
1. Or use screenshots with voiceover
1. Explain: "Here's what the system does when working correctly..."

---

Good luck with your recording! 🎬
