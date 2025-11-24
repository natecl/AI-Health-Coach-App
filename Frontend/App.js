const API_DEFAULT = "http://127.0.0.1:5000";

const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("coach-form");
const textareaEl = document.getElementById("message");
const apiUrlEl = document.getElementById("api-url");
const statusDotEl = document.getElementById("status-dot");
const statusTextEl = document.getElementById("status-text");
const submitBtn = document.getElementById("submit-btn");

function setStatus(text, ok = true) {
  statusTextEl.textContent = text;
  statusDotEl.style.background = ok ? "var(--accent)" : "#f27d52";
  statusDotEl.style.boxShadow = ok
    ? "0 0 0 4px rgba(30, 200, 165, 0.2)"
    : "0 0 0 4px rgba(242, 125, 82, 0.2)";
}

function appendMessage(sender, text) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${sender}`;
  bubble.textContent = text;
  messagesEl.appendChild(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function handleSubmit(event) {
  event.preventDefault();
  const message = textareaEl.value.trim();
  if (!message) return;

  const apiBase = (apiUrlEl.value || API_DEFAULT).replace(/\/+$/, "");
  appendMessage("user", message);
  textareaEl.value = "";

  submitBtn.disabled = true;
  setStatus("Thinking...", true);

  try {
    const res = await axios.post(`${apiBase}/api/coach`, { message });
    appendMessage("ai", res.data.reply || "I had trouble generating a reply.");
    setStatus("Ready", true);
  } catch (error) {
    console.error(error);
    appendMessage("ai", "Unable to reach the backend. Check the URL and that the server is running.");
    setStatus("Backend unreachable", false);
  } finally {
    submitBtn.disabled = false;
    textareaEl.focus();
  }
}

function init() {
  appendMessage(
    "ai",
    "Hey! I'm your health coach. Ask me about stress, sleep, nutrition, or quick habits to try this week."
  );
  formEl.addEventListener("submit", handleSubmit);
  textareaEl.focus();
}

document.addEventListener("DOMContentLoaded", init);
