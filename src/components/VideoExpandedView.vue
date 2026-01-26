<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';
import { useOllama } from '../composables/useOllama.js';

const props = defineProps({
  video: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['close']);

const { isLoading, error, generateVideoSummary, chatAboutVideo, checkOllamaStatus } = useOllama();

const summary = ref('');
const summaryLoading = ref(false);
const chatMessages = ref([]);
const userInput = ref('');
const chatLoading = ref(false);
const ollamaAvailable = ref(false);
const chatContainer = ref(null);

const close = () => {
  emit('close');
};

const handleKeydown = (e) => {
  if (e.key === 'Escape') {
    close();
  }
};

const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

const loadSummary = async () => {
  if (!ollamaAvailable.value) return;

  summaryLoading.value = true;
  summary.value = '';

  try {
    await generateVideoSummary(props.video, (text) => {
      summary.value = text;
    });
  } catch (err) {
    summary.value = 'Unable to generate summary. Please check if Ollama is running.';
  } finally {
    summaryLoading.value = false;
  }
};

const sendMessage = async () => {
  const message = userInput.value.trim();
  if (!message || chatLoading.value) return;

  chatMessages.value.push({ role: 'user', content: message });
  userInput.value = '';
  chatLoading.value = true;

  // Add placeholder for assistant response
  const assistantIndex = chatMessages.value.length;
  chatMessages.value.push({ role: 'assistant', content: '' });

  await scrollToBottom();

  try {
    const history = chatMessages.value.slice(0, -1); // Exclude the empty placeholder
    await chatAboutVideo(props.video, message, history, (text) => {
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

onMounted(async () => {
  window.addEventListener('keydown', handleKeydown);
  document.body.style.overflow = 'hidden';

  ollamaAvailable.value = await checkOllamaStatus();
  if (ollamaAvailable.value) {
    loadSummary();
  }
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
  document.body.style.overflow = '';
});

watch(() => props.video, async () => {
  summary.value = '';
  chatMessages.value = [];
  if (ollamaAvailable.value) {
    loadSummary();
  }
});
</script>

<template>
  <div class="expanded-view-overlay" @click.self="close">
    <div class="expanded-view">
      <button class="close-btn" @click="close">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>

      <div class="expanded-content">
        <!-- Left: Video Player -->
        <div class="video-section">
          <div class="video-player">
            <iframe
              :src="`${video.embedUrl}?autoplay=1`"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
          <div class="video-info">
            <span class="video-category">{{ video.category }}</span>
            <h2 class="video-title">{{ video.title }}</h2>
            <p class="video-description">{{ video.description }}</p>
          </div>
        </div>

        <!-- Right: AI Summary & Chat -->
        <div class="ai-section">
          <!-- Ollama Status Warning -->
          <div v-if="!ollamaAvailable" class="ollama-warning">
            <div class="warning-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
            </div>
            <div class="warning-content">
              <h4>Ollama Not Connected</h4>
              <p>Start Ollama to enable AI features:</p>
              <code>ollama serve</code>
            </div>
          </div>

          <!-- AI Summary -->
          <div class="summary-section">
            <div class="section-header">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
              <h3>AI Summary</h3>
              <button
                v-if="ollamaAvailable && !summaryLoading"
                class="refresh-btn"
                @click="loadSummary"
                title="Regenerate summary"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="23 4 23 10 17 10"/>
                  <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                </svg>
              </button>
            </div>
            <div class="summary-content">
              <div v-if="summaryLoading" class="loading-indicator">
                <div class="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span>Generating summary...</span>
              </div>
              <p v-else-if="summary" class="summary-text">{{ summary }}</p>
              <p v-else class="summary-placeholder">
                {{ ollamaAvailable ? 'Click refresh to generate a summary' : 'Connect Ollama to generate AI summaries' }}
              </p>
            </div>
          </div>

          <!-- Chat Section -->
          <div class="chat-section">
            <div class="section-header">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              <h3>Ask About This Video</h3>
            </div>

            <div class="chat-container" ref="chatContainer">
              <div v-if="chatMessages.length === 0" class="chat-placeholder">
                <p>Ask any question about this video or related topics</p>
                <div class="suggested-questions">
                  <button
                    v-for="question in [
                      'What components are used?',
                      'How does this project work?',
                      'What skills do I need?'
                    ]"
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
                  <svg v-if="msg.role === 'user'" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                  </svg>
                  <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
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

            <div class="chat-input-container">
              <input
                v-model="userInput"
                type="text"
                placeholder="Ask a question about this video..."
                @keydown="handleInputKeydown"
                :disabled="!ollamaAvailable || chatLoading"
              />
              <button
                class="send-btn"
                @click="sendMessage"
                :disabled="!userInput.trim() || !ollamaAvailable || chatLoading"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.expanded-view-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.95);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  animation: fadeIn 0.3s ease;
}

.expanded-view {
  position: relative;
  width: 100%;
  max-width: 1400px;
  max-height: 90vh;
  background: var(--bg-dark);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  animation: slideUp 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 40px;
  height: 40px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition);
  z-index: 10;
}

.close-btn:hover {
  background: var(--primary);
  border-color: var(--primary);
}

.expanded-content {
  display: grid;
  grid-template-columns: 1fr 400px;
  height: 90vh;
  max-height: 800px;
}

/* Video Section */
.video-section {
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border);
}

.video-player {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;
  background: #000;
}

.video-player iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.video-info {
  padding: 24px;
  flex: 1;
  overflow-y: auto;
}

.video-info .video-category {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.video-info .video-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 12px;
  line-height: 1.3;
}

.video-info .video-description {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* AI Section */
.ai-section {
  display: flex;
  flex-direction: column;
  background: var(--bg-card);
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-dark);
}

.section-header svg {
  color: var(--secondary);
}

.section-header h3 {
  font-size: 0.95rem;
  font-weight: 600;
  flex: 1;
}

.refresh-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
}

.refresh-btn:hover {
  border-color: var(--secondary);
  color: var(--secondary);
}

/* Ollama Warning */
.ollama-warning {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: rgba(239, 68, 68, 0.1);
  border-bottom: 1px solid rgba(239, 68, 68, 0.3);
}

.warning-icon {
  color: #ef4444;
  flex-shrink: 0;
}

.warning-content h4 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #ef4444;
  margin-bottom: 4px;
}

.warning-content p {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.warning-content code {
  display: inline-block;
  padding: 4px 12px;
  background: var(--bg-dark);
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: var(--accent);
}

/* Summary Section */
.summary-section {
  border-bottom: 1px solid var(--border);
}

.summary-content {
  padding: 20px;
  max-height: 200px;
  overflow-y: auto;
}

.summary-text {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.7;
  white-space: pre-wrap;
}

.summary-placeholder {
  font-size: 0.9rem;
  color: var(--text-muted);
  font-style: italic;
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-muted);
  font-size: 0.9rem;
}

/* Chat Section */
.chat-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
}

.chat-placeholder {
  text-align: center;
  padding: 20px;
}

.chat-placeholder p {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 16px;
}

.suggested-questions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.suggested-questions button {
  padding: 10px 16px;
  background: var(--bg-dark);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 0.85rem;
  text-align: left;
  cursor: pointer;
  transition: var(--transition);
}

.suggested-questions button:hover:not(:disabled) {
  border-color: var(--secondary);
  color: var(--text-primary);
}

.suggested-questions button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.chat-message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 32px;
  height: 32px;
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
  max-width: 85%;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 0.9rem;
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

/* Typing dots animation */
.typing-dots {
  display: flex;
  gap: 4px;
  align-items: center;
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
.chat-input-container {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  background: var(--bg-dark);
  border-top: 1px solid var(--border);
}

.chat-input-container input {
  flex: 1;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-family: inherit;
  font-size: 0.9rem;
  color: var(--text-primary);
  transition: var(--transition);
}

.chat-input-container input:focus {
  outline: none;
  border-color: var(--secondary);
}

.chat-input-container input::placeholder {
  color: var(--text-muted);
}

.chat-input-container input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn {
  width: 44px;
  height: 44px;
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
@media (max-width: 1024px) {
  .expanded-content {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
  }

  .video-section {
    border-right: none;
    border-bottom: 1px solid var(--border);
  }

  .video-info {
    padding: 16px;
  }

  .video-info .video-title {
    font-size: 1.2rem;
  }

  .expanded-view {
    max-height: 95vh;
  }

  .expanded-content {
    height: 95vh;
    max-height: none;
  }
}

@media (max-width: 768px) {
  .expanded-view-overlay {
    padding: 0;
  }

  .expanded-view {
    border-radius: 0;
    max-height: 100vh;
  }

  .expanded-content {
    height: 100vh;
  }

  .close-btn {
    top: 8px;
    right: 8px;
  }
}
</style>
