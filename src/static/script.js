// src/static/script.js

const API_URL = "/predict_intent";

const messagesEl     = document.getElementById("messages");
const quickRepliesEl = document.getElementById("quick-replies");
const inputEl        = document.getElementById("user-input");
const sendBtn        = document.getElementById("send-btn");

// Map of intent → friendly reply (underscore only keys)
const intentResponses = {
  Order_Status:    "Sure—please share your Order ID, and I’ll check its status right away.",
  Return_Policy:   "Our return policy allows returns within 30 days in the original packaging.",
  Technical_Issue: "I’m sorry you’re having trouble. Could you describe the problem in more detail?",
};

// Fallback if unmapped
const defaultReply = "Thanks for your message! Let me look into that and get back to you.";

// Quick-reply button labels (free-text)
const quickReplies = ["Order Status", "Return Policy", "Technical Issue"];

function currentTime() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function appendMessage(text, sender="bot", meta="") {
  const msgEl = document.createElement("div");
  msgEl.className = `message ${sender}`;
  const avatar = document.createElement("div");
  avatar.className = `avatar ${sender}`;
  avatar.textContent = sender === "user" ? "👤" : "🤖";
  msgEl.appendChild(avatar);
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  msgEl.appendChild(bubble);
  if (meta) {
    const stamp = document.createElement("div");
    stamp.className = "timestamp";
    stamp.textContent = meta;
    msgEl.appendChild(stamp);
  }
  messagesEl.appendChild(msgEl);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function showTyping() {
  appendMessage("", "bot");
  const last = messagesEl.lastChild;
  last.classList.add("typing");
  last.querySelector(".avatar").textContent = "🤖";
  last.querySelector(".bubble").innerHTML =
    '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
}

function hideTyping() {
  const tip = messagesEl.querySelector(".typing");
  if (tip) tip.remove();
}

function renderQuickReplies() {
  quickRepliesEl.innerHTML = "";
  quickReplies.forEach(text => {
    const btn = document.createElement("button");
    btn.className = "quick-reply-button";
    btn.textContent = text;
    btn.onclick = () => sendMessage(text);
    quickRepliesEl.appendChild(btn);
  });
}

async function sendMessage(prefill = null) {
  const msg = prefill !== null ? prefill : inputEl.value.trim();
  if (!msg) return;

  // 1. Show user message
  appendMessage(msg, "user", currentTime());
  inputEl.value = "";
  sendBtn.disabled = true;
  quickRepliesEl.innerHTML = "";

  // 2. If it’s a quick-reply, bypass the API and use the mapping directly
  if (prefill !== null && quickReplies.includes(prefill)) {
    // Normalize "Order Status" → "Order_Status"
    const key = prefill.replace(/\s+/g, "_");
    const reply = intentResponses[key] || defaultReply;
    appendMessage(reply, "bot", `— • ${currentTime()}`);
    renderQuickReplies();
    sendBtn.disabled = false;
    return;
  }

  // 3. Otherwise, call the API
  showTyping();
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });
    const { intent, confidence } = await res.json();
    hideTyping();

    // Normalize and lookup
    const key = intent.replace(/\s+/g, "_");
    const reply = intentResponses[key] || defaultReply;
    appendMessage(
      reply,
      "bot",
      `confidence ${(confidence * 100).toFixed(0)}% • ${currentTime()}`
    );

    renderQuickReplies();
  } catch (e) {
    hideTyping();
    appendMessage("❌ Server error. Please try again later.", "bot", currentTime());
    console.error(e);
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

// Event listeners
sendBtn.addEventListener("click", () => sendMessage());
inputEl.addEventListener("keypress", e => { if (e.key === "Enter") sendMessage(); });

// Initial greeting
appendMessage("Hello! How can I assist you today?", "bot", currentTime());
renderQuickReplies();
