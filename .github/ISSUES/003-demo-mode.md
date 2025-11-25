# MVP: Demo Mode (record & replay)

Description

Create a deterministic Demo Mode that plays back recorded sessions (synthetic data) so the demo is reproducible and does not require live cloud resources.

Acceptance criteria

- A stored JSON demo session can be replayed end-to-end.
- Demo Mode UI exposes a "Play" button to trigger the replay.
- The orchestrator supports a `mode` toggle: `live` vs `recorded`.

Estimate: 4 hours

Owner: @frontend
