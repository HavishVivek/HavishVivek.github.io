<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import { useOllama } from '../composables/useOllama.js';

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
});

const { isLoading, error, chatAboutVideo, checkOllamaStatus, generateResponse } = useOllama();

const isOpen = ref(false);
const chatMessages = ref([]);
const userInput = ref('');
const chatLoading = ref(false);
const ollamaAvailable = ref(false);
const chatContainer = ref(null);

const toggleChat = () => {
  isOpen.value = !isOpen.value;
};

const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

const chatAboutProject = async (userMessage, chatHistory = [], onStream = null) => {
  const componentsList = props.project.components?.map(c => `- ${c.name}: ${c.description}`).join('\n') || 'No components listed';

  const systemPrompt = `You are a helpful assistant discussing a maker/electronics project.

Project Context:
- Title: ${props.project.title}
- Category: ${props.project.category}
- Description: ${props.project.description}
- Technologies: ${props.project.tech?.join(', ')}

Components Used:
${componentsList}

Answer questions about this project, its components, how it works, and related topics.
If asked about building something similar, provide helpful guidance.
Keep responses concise and helpful. Use technical terminology appropriate for hobbyists.
If you don't know something specific about this project, you can provide general information about similar projects or technologies.`;

  let conversationContext = '';
  if (chatHistory.length > 0) {
    conversationContext = '\n\nPrevious conversation:\n' +
      chatHistory.slice(-6).map(msg => `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`).join('\n');
  }

  const prompt = `${conversationContext}\n\nUser: ${userMessage}\n\nAssistant:`;

  return generateResponse(prompt, systemPrompt, onStream);
};

const sendMessage = async () => {
  const message = userInput.value.trim();
  if (!message || chatLoading.value) return;

  chatMessages.value.push({ role: 'user', content: message });
  userInput.value = '';
  chatLoading.value = true;

  const assistantIndex = chatMessages.value.length;
  chatMessages.value.push({ role: 'assistant', content: '' });

  await scrollToBottom();

  try {
    const history = chatMessages.value.slice(0, -1);
    await chatAboutProject(message, history, (text) => {
      chatMessages.value[assistantIndex].content = text;
      scrollToBottom();
    });
  } catch (err) {
    chatMessages.value[assistantIndex].content = 'Sorry, I encountered an error. Please check if Ollama is running.';
  } finally {
    chatLoading.value = false;
    scrollToBottom();
  }
};

const handleInputKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
};

const suggestedQuestions = [
  'How does this project work?',
  'What components do I need?',
  'How do I get started?',
  'What are common issues?'
];

onMounted(async () => {
  ollamaAvailable.value = await checkOllamaStatus();
});

watch(isOpen, async (newVal) => {
  if (newVal) {
    await nextTick();
    scrollToBottom();
  }
});
</script>

<template>
  <div class="project-ai-chat" :class="{ open: isOpen }">
    <!-- Chat Toggle Button -->
    <button class="chat-toggle" @click="toggleChat" :class="{ active: isOpen }">
      <div class="toggle-icon">
        <svg v-if="!isOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </div>
      <span class="toggle-label">Ask AI</span>
      <span class="toggle-pulse"></span>
    </button>

    <!-- Chat Panel -->
    <div class="chat-panel">
      <div class="chat-header">
        <div class="header-info">
          <div class="ai-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
            </svg>
          </div>
          <div>
            <h3>Project Assistant</h3>
            <span class="status" :class="{ online: ollamaAvailable }">
              {{ ollamaAvailable ? 'Online' : 'Offline' }}
            </span>
          </div>
        </div>
        <button class="close-chat" @click="isOpen = false">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </button>
      </div>

      <!-- Ollama Warning -->
      <div v-if="!ollamaAvailable" class="ollama-warning">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <div>
          <strong>Ollama not running</strong>
          <p>Run <code>ollama serve</code> to enable AI</p>
        </div>
      </div>

      <!-- Chat Messages -->
      <div class="chat-messages" ref="chatContainer">
        <div v-if="chatMessages.length === 0" class="chat-welcome">
          <div class="welcome-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
            </svg>
          </div>
          <h4>Ask me anything!</h4>
          <p>I can help with questions about this project, its components, or how to build something similar.</p>

          <div class="suggested-questions">
            <button
              v-for="question in suggestedQuestions"
              :key="question"
              @click="userInput = question; sendMessage()"
              :disabled="!ollamaAvailable || chatLoading"
            >
              {{ question }}
            </button>
          </div>
        </div>

        <div
          v-for="(msg, index) in chatMessages"
          :key="index"
          class="chat-message"
          :class="msg.role"
        >
          <div class="message-avatar">
            <svg v-if="msg.role === 'user'" width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
            </svg>
          </div>
          <div class="message-content">
            <span v-if="msg.content">{{ msg.content }}</span>
            <div v-else class="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Input -->
      <div class="chat-input-area">
        <input
          v-model="userInput"
          type="text"
          placeholder="Ask about this project..."
          @keydown="handleInputKeydown"
          :disabled="!ollamaAvailable || chatLoading"
        />
        <button
          class="send-btn"
          @click="sendMessage"
          :disabled="!userInput.trim() || !ollamaAvailable || chatLoading"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.project-ai-chat {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
}

/* Toggle Button */
.chat-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  background: var(--gradient-1);
  border: none;
  border-radius: 50px;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  box-shadow: var(--shadow-glow);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.chat-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 50px rgba(99, 102, 241, 0.5);
}

.chat-toggle.active {
  border-radius: 12px;
}

.toggle-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-pulse {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s ease infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.project-ai-chat.open .chat-toggle {
  display: none;
}

/* Chat Panel */
.chat-panel {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 380px;
  height: 500px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px) scale(0.95);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.project-ai-chat.open .chat-panel {
  opacity: 1;
  visibility: visible;
  transform: translateY(0) scale(1);
}

/* Chat Header */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: var(--bg-dark);
  border-bottom: 1px solid var(--border);
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-avatar {
  width: 40px;
  height: 40px;
  background: var(--gradient-1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.header-info h3 {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 2px;
}

.header-info .status {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.header-info .status.online {
  color: #22c55e;
}

.header-info .status.online::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  background: #22c55e;
  border-radius: 50%;
  margin-right: 6px;
}

.close-chat {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
}

.close-chat:hover {
  border-color: var(--primary);
  color: var(--text-primary);
}

/* Ollama Warning */
.ollama-warning {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(239, 68, 68, 0.1);
  border-bottom: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.ollama-warning svg {
  flex-shrink: 0;
  margin-top: 2px;
}

.ollama-warning strong {
  font-size: 0.85rem;
  display: block;
  margin-bottom: 4px;
}

.ollama-warning p {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin: 0;
}

.ollama-warning code {
  padding: 2px 6px;
  background: var(--bg-dark);
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--accent);
}

/* Chat Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.chat-welcome {
  text-align: center;
  padding: 20px;
}

.welcome-icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-light);
}

.chat-welcome h4 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.chat-welcome p {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 20px;
  line-height: 1.5;
}

.suggested-questions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.suggested-questions button {
  padding: 10px 14px;
  background: var(--bg-dark);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 0.8rem;
  text-align: left;
  cursor: pointer;
  transition: var(--transition);
}

.suggested-questions button:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--text-primary);
}

.suggested-questions button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Chat Message */
.chat-message {
  display: flex;
  gap: 10px;
  margin-bottom: 14px;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.chat-message.user .message-avatar {
  background: var(--gradient-1);
  color: white;
}

.chat-message.assistant .message-avatar {
  background: rgba(6, 182, 212, 0.2);
  color: var(--secondary);
}

.message-content {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 0.85rem;
  line-height: 1.5;
}

.chat-message.user .message-content {
  background: var(--gradient-1);
  color: white;
  border-bottom-right-radius: 4px;
}

.chat-message.assistant .message-content {
  background: var(--bg-dark);
  border: 1px solid var(--border);
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
}

/* Typing dots */
.typing-dots {
  display: flex;
  gap: 4px;
  align-items: center;
  padding: 4px 0;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: var(--secondary);
  border-radius: 50%;
  animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: 0s; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Chat Input */
.chat-input-area {
  display: flex;
  gap: 10px;
  padding: 16px;
  background: var(--bg-dark);
  border-top: 1px solid var(--border);
}

.chat-input-area input {
  flex: 1;
  padding: 10px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.9rem;
  color: var(--text-primary);
  transition: var(--transition);
}

.chat-input-area input:focus {
  outline: none;
  border-color: var(--primary);
}

.chat-input-area input::placeholder {
  color: var(--text-muted);
}

.chat-input-area input:disabled {
  opacity: 0.5;
}

.send-btn {
  width: 40px;
  height: 40px;
  background: var(--gradient-1);
  border: none;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: var(--transition);
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 480px) {
  .project-ai-chat {
    bottom: 16px;
    right: 16px;
  }

  .chat-panel {
    width: calc(100vw - 32px);
    height: calc(100vh - 100px);
    max-height: 500px;
  }

  .toggle-label {
    display: none;
  }

  .chat-toggle {
    padding: 14px;
    border-radius: 50%;
  }
}
</style>
