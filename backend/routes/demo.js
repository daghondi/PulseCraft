const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

const SESSIONS_DIR = path.join(__dirname, '../data/sessions');
if (!fs.existsSync(SESSIONS_DIR)) fs.mkdirSync(SESSIONS_DIR, { recursive: true });

// POST /api/demo/run - Create and run a demo session
router.post('/run', (req, res) => {
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

  fs.writeFileSync(path.join(SESSIONS_DIR, `${sessionId}.json`), JSON.stringify(result, null, 2));
  res.json(result);
});

// GET /api/demo/replay/:id - Replay saved session
router.get('/replay/:id', (req, res) => {
  const id = req.params.id;
  const filePath = path.join(SESSIONS_DIR, `${id}.json`);
  if (!fs.existsSync(filePath)) return res.status(404).json({ error: 'session not found' });
  const data = JSON.parse(fs.readFileSync(filePath));
  res.json(data);
});

// GET /api/demo/list - List all sessions
router.get('/list', (req, res) => {
  const files = fs.readdirSync(SESSIONS_DIR).filter(f => f.endsWith('.json'));
  const sessions = files.map(f => {
    const s = JSON.parse(fs.readFileSync(path.join(SESSIONS_DIR, f)));
    return { sessionId: s.sessionId, timestamp: s.timestamp };
  });
  res.json(sessions);
});

module.exports = router;
