// API base URL - update if backend is on different port/host
const API_URL = 'http://localhost:3001';

// DOM elements
const customerNameInput = document.getElementById('customerName');
const runDemoBtn = document.getElementById('runDemo');
const replayLastBtn = document.getElementById('replayLast');
const listSessionsBtn = document.getElementById('listSessions');
const output = document.getElementById('output');

// Store last session ID for replay
let lastSessionId = null;

// Helper function to display output
function displayOutput(data, error = false) {
  if (error) {
    output.textContent = `❌ ERROR:\n${JSON.stringify(data, null, 2)}`;
    output.style.color = '#d13438';
  } else {
    output.textContent = JSON.stringify(data, null, 2);
    output.style.color = '#000';
  }
}

// Run Demo endpoint
runDemoBtn.addEventListener('click', async () => {
  const customerName = customerNameInput.value.trim();
  
  if (!customerName) {
    displayOutput({ message: 'Please enter a customer name' }, true);
    return;
  }

  try {
    output.textContent = 'Running demo...';
    
    const response = await fetch(`${API_URL}/api/demo/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customerName })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      displayOutput(data, true);
      return;
    }
    
    // Save session ID for replay
    lastSessionId = data.sessionId;
    displayOutput(data);
    
  } catch (error) {
    displayOutput({ message: error.message }, true);
  }
});

// Replay Last Session
replayLastBtn.addEventListener('click', async () => {
  if (!lastSessionId) {
    displayOutput({ message: 'No session to replay. Run demo first.' }, true);
    return;
  }

  try {
    output.textContent = 'Loading session...';
    
    const response = await fetch(`${API_URL}/api/demo/replay/${lastSessionId}`);
    const data = await response.json();
    
    if (!response.ok) {
      displayOutput(data, true);
      return;
    }
    
    displayOutput(data);
    
  } catch (error) {
    displayOutput({ message: error.message }, true);
  }
});

// List All Sessions
listSessionsBtn.addEventListener('click', async () => {
  try {
    output.textContent = 'Loading sessions...';
    
    const response = await fetch(`${API_URL}/api/demo/list`);
    const data = await response.json();
    
    if (!response.ok) {
      displayOutput(data, true);
      return;
    }
    
    displayOutput(data);
    
  } catch (error) {
    displayOutput({ message: error.message }, true);
  }
});
