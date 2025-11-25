const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const path = require('path');
const fs = require('fs');

const app = express();
app.use(cors());
app.use(bodyParser.json());

const PORT = process.env.PORT || 3000;

// Serve static frontend
app.use(express.static(path.join(__dirname, 'public')));

// Simple in-memory store for demo sessions (persist to disk)
const SESSIONS_DIR = path.join(__dirname, 'data');
if (!fs.existsSync(SESSIONS_DIR)) fs.mkdirSync(SESSIONS_DIR);

app.post('/api/demo/run', (req, res) => {
  // Simulate pipeline: accept input events, return generated messages
  const sessionId = uuidv4();
  const input = req.body || { simulated: true };

  const result = {
    sessionId,
    timestamp: new Date().toISOString(),
    input,
    messages: [
      { channel: 'email', text: `Hello ${input.customerName || 'Customer'}, here's an offer for you.` },
      { channel: 'sms', text: `Hi ${input.customerName || 'Friend'} — special offer!` }
    ]
  };

  // persist to disk
  fs.writeFileSync(path.join(SESSIONS_DIR, `${sessionId}.json`), JSON.stringify(result, null, 2));

  res.json(result);
});

app.get('/api/demo/replay/:id', (req, res) => {
  const id = req.params.id;
  const p = path.join(SESSIONS_DIR, `${id}.json`);
  if (!fs.existsSync(p)) return res.status(404).json({ error: 'session not found' });
  const data = JSON.parse(fs.readFileSync(p));
  res.json(data);
});

app.get('/api/demo/list', (req, res) => {
  const files = fs.readdirSync(SESSIONS_DIR).filter(f => f.endsWith('.json'));
  const sessions = files.map(f => {
    const s = JSON.parse(fs.readFileSync(path.join(SESSIONS_DIR, f)));
    return { sessionId: s.sessionId, timestamp: s.timestamp };
  });
  res.json(sessions);
});

app.listen(PORT, () => console.log(`PulseCraft demo server listening on http://localhost:${PORT}`));
