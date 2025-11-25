# Agents Directory

This directory contains the agent modules for the PulseCraft Customer Personalization Orchestrator.

## Agent Architecture

The system uses a multi-agent architecture where specialized agents work together to deliver personalized customer experiences:

### 1. **Enricher Agent** (`enricher.js`)
- **Purpose**: Enriches customer profiles with behavioral, transactional, and contextual data
- **Data Sources**: 
  - Azure Synapse Retail Recommender (purchase history, browsing patterns)
  - Azure Cosmos DB (customer profiles, preferences)
  - Azure Blob Storage (historical data)
- **Output**: Enhanced customer profile with attributes like loyalty tier, purchase frequency, preferred categories

### 2. **Scorer Agent** (`scorer.js`)
- **Purpose**: Scores personalization opportunities using AI and business rules
- **Inputs**: Enriched customer profile from Enricher Agent
- **Processing**:
  - Azure OpenAI for intelligent scoring based on customer intent and context
  - Business rules for promotions, stock availability, margin optimization
- **Output**: Ranked personalization opportunities (product recommendations, offers, content)

### 3. **Composer Agent** (`composer.js`)
- **Purpose**: Composes the final personalized message/experience
- **Inputs**: Scored opportunities from Scorer Agent
- **Processing**:
  - Selects top recommendations based on scores and constraints
  - Generates personalized messaging using Azure OpenAI
  - Assembles multi-channel content (email, web, mobile)
- **Output**: Formatted personalization payload ready for delivery

### 4. **Compliance Agent** (`compliance.js`)
- **Purpose**: Validates all outputs against compliance and business rules
- **Checks**:
  - GDPR/privacy compliance (consent, data usage)
  - Brand safety and content guidelines
  - Regulatory requirements (financial services, healthcare)
  - A/B testing constraints
- **Output**: Approved payload or rejection with reasons

## Communication Pattern

Agents communicate through Azure Service Bus queues:

```
Customer Request → Enricher Agent → Scorer Agent → Composer Agent → Compliance Agent → Response
```

## Running Agents

### Development Mode
Each agent can run as a standalone Node.js process for testing:

```bash
# Run individual agent
node agents/enricher.js

# With environment variables
node -r dotenv/config agents/enricher.js
```

### Production Mode
Agents are deployed as Azure Functions or Azure Container Instances and triggered via Service Bus messages.

## Agent Communication

Agents use a standard message format:

```javascript
{
  sessionId: "uuid",
  customerId: "customer_id",
  timestamp: "ISO8601",
  data: {
    // Agent-specific payload
  },
  metadata: {
    source: "enricher|scorer|composer|compliance",
    version: "1.0.0"
  }
}
```

## Future Enhancements

- [ ] Add agent monitoring and health checks
- [ ] Implement circuit breakers for external service calls
- [ ] Add distributed tracing with Application Insights
- [ ] Implement agent versioning and A/B testing
- [ ] Add retry logic and dead-letter queue handling

## References

- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure Service Bus](https://learn.microsoft.com/en-us/azure/service-bus-messaging/)
- [Azure Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
