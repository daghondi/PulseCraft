const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(bodyParser.json());

const PORT = process.env.PORT || 3001;

// Import routes
const demoRoutes = require('./routes/demo');

// Mount routes
app.use('/api/demo', demoRoutes);

// Health check
app.get('/health', (req, res) => res.json({ status: 'ok' }));

app.listen(PORT, () => console.log(`PulseCraft API listening on http://localhost:${PORT}`));
