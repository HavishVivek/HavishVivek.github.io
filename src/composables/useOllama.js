import { ref } from 'vue';

const OLLAMA_API_URL = 'http://localhost:11434/api';
const OLLAMA_MODEL = 'llama3.2:3b'; // Options: 'llama3.2:3b', 'llama3.1:8b', 'phi3:mini'

export function useOllama() {
  const isLoading = ref(false);
  const error = ref(null);

  const generateResponse = async (prompt, context = '', onStream = null) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${OLLAMA_API_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: OLLAMA_MODEL,
          prompt: prompt,
          system: context,
          stream: !!onStream,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to connect to Ollama. Make sure Ollama is running.');
      }

      if (onStream) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n').filter(line => line.trim());

          for (const line of lines) {
            try {
              const parsed = JSON.parse(line);
              if (parsed.response) {
                fullResponse += parsed.response;
                onStream(fullResponse);
              }
            } catch (e) {
              // Skip invalid JSON lines
            }
          }
        }

        return fullResponse;
      } else {
        const data = await response.json();
        return data.response;
      }
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const generateVideoSummary = async (video, onStream = null) => {
    const systemPrompt = `You are a helpful assistant that provides concise summaries of YouTube videos about electronics, IoT, and maker projects.
Keep your summaries informative but brief (2-3 paragraphs max).
Focus on: what the project does, key components used, and what viewers will learn.
Use a friendly, technical tone appropriate for makers and hobbyists.`;

    const prompt = `Please provide a summary for this video:

Title: ${video.title}
Category: ${video.category}
Description: ${video.description}

Generate a helpful summary that explains what this video covers and what viewers will learn from it.`;

    return generateResponse(prompt, systemPrompt, onStream);
  };

  const chatAboutVideo = async (video, userMessage, chatHistory = [], onStream = null) => {
    const systemPrompt = `You are a helpful assistant discussing a YouTube video about electronics/IoT/maker projects.

Video Context:
- Title: ${video.title}
- Category: ${video.category}
- Description: ${video.description}

Answer questions about this video's topic. If the question is outside the video's scope, you can still help with related electronics/maker topics but mention it's beyond the specific video content.
Keep responses concise and helpful. Use technical terminology appropriate for hobbyists.`;

    let conversationContext = '';
    if (chatHistory.length > 0) {
      conversationContext = '\n\nPrevious conversation:\n' +
        chatHistory.map(msg => `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`).join('\n');
    }

    const prompt = `${conversationContext}\n\nUser: ${userMessage}\n\nAssistant:`;

    return generateResponse(prompt, systemPrompt, onStream);
  };

  const checkOllamaStatus = async () => {
    try {
      const response = await fetch(`${OLLAMA_API_URL}/tags`);
      return response.ok;
    } catch {
      return false;
    }
  };

  return {
    isLoading,
    error,
    generateResponse,
    generateVideoSummary,
    chatAboutVideo,
    checkOllamaStatus,
  };
}
