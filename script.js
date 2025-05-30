

const chatArea = document.querySelector('.chat-area');
const input = document.querySelector('.chat-input input');
const sendBtn = document.querySelector('.chat-input button');
const cards = document.querySelectorAll('.card');


function appendMessage(message, sender = 'user', citations = [], options = {}) {
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${sender}`;
  if (options.thinking) bubble.classList.add('thinking');
  if (options.typing) {
    // Typing indicator (animated dots)
    bubble.innerHTML = `<div class="bubble-content"><span class="typing-indicator"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></span></div>`;
  } else {
    bubble.innerHTML = `<div class="bubble-content">${message}</div>`;
  }
  if (sender === 'bot' && citations.length > 0) {
    const citeDiv = document.createElement('div');
    citeDiv.className = 'citations';
    citeDiv.innerHTML = citations.map(c => `<span class="citation">${c}</span>`).join(' ');
    bubble.appendChild(citeDiv);
  }
  chatArea.appendChild(bubble);
  chatArea.scrollTop = chatArea.scrollHeight;
  return bubble;
}




function sendMessage(message) {
  if (!message.trim()) return;
  // Show bot's typing indicator bubble while user is typing
  const botTypingBubble = appendMessage('', 'bot', [], { typing: true });
  // Show user's message bubble after a short delay (simulate send)
  setTimeout(() => {
    appendMessage(message, 'user');
    input.value = '';
    // Remove bot's typing indicator
    chatArea.removeChild(botTypingBubble);
    // Show bot's "received" bubble (bot sees the question)
    const botReceivedBubble = appendMessage(message, 'bot', [], { });
    // Show bot's thinking indicator for 2 seconds
    const botThinkingBubble = appendMessage('', 'bot', [], { thinking: true, typing: true });
    setTimeout(() => {
      chatArea.removeChild(botThinkingBubble);
      fetchBotResponse(message, botReceivedBubble);
    }, 2000);
  }, 500);
}



async function fetchBotResponse(message, botReceivedBubble) {
  // After the 2s delay, fetch the bot's answer and update the bot's bubble
  try {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    // Debug: Log the raw response for troubleshooting
    console.log('fetchBotResponse: response', response);
    // If streaming, handle as stream; else, as JSON
    if (response.body && response.body.getReader) {
      // Streaming response
      let botMsg = '';
      let citations = [];
      const reader = response.body.getReader();
      let done = false;
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          const chunk = new TextDecoder().decode(value);
          // Expect chunk to be JSON lines or plain text
          try {
            const data = JSON.parse(chunk);
            if (data.citations) citations = data.citations;
            if (data.text) botMsg += data.text;
          } catch {
            botMsg += chunk;
          }
          // Update the bot received bubble with the current message
          botReceivedBubble.innerHTML = `<div class="bubble-content">${botMsg}</div>`;
        }
      }
      // Add citations if any
      if (citations.length > 0) {
        const citeDiv = document.createElement('div');
        citeDiv.className = 'citations';
        citeDiv.innerHTML = citations.map(c => `<span class="citation">${c}</span>`).join(' ');
        botReceivedBubble.appendChild(citeDiv);
      }
    } else {
      // Non-streaming JSON response
      const data = await response.json();
      console.log('fetchBotResponse: data', data);
      botReceivedBubble.innerHTML = `<div class="bubble-content">${data.text || 'Sorry, no response.'}</div>`;
      if (data.citations && data.citations.length > 0) {
        const citeDiv = document.createElement('div');
        citeDiv.className = 'citations';
        citeDiv.innerHTML = data.citations.map(c => `<span class="citation">${c}</span>`).join(' ');
        botReceivedBubble.appendChild(citeDiv);
      }
    }
  } catch (err) {
    botReceivedBubble.innerHTML = `<div class="bubble-content">Sorry, there was an error connecting to the server.</div>`;
  }
}

// Send on button click
sendBtn.addEventListener('click', () => {
  sendMessage(input.value);
});

// Send on Enter key
input.addEventListener('keydown', e => {
  if (e.key === 'Enter') sendMessage(input.value);
});

// Card click sends question
cards.forEach(card => {
  card.addEventListener('click', () => {
    const question = card.querySelector('p').innerText;
    sendMessage(question);
  });
});
