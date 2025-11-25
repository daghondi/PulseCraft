# MVP: Primary Flow — capture -> process -> visualize

Description

Implement the core end-to-end flow that demonstrates PulseCraft's value: capture an input event, run the processing pipeline (enrichment -> scoring -> message composition), and show the result in the UI.

Acceptance criteria

- User can trigger the flow from the UI within 60s.
- The system returns a generated message and stores the session to `data/`.
- Demo Mode can replay the session using the replay endpoint.

Estimate: 6 hours

Owner: @frontend
