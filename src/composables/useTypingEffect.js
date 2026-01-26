import { ref, onMounted, onUnmounted } from 'vue';

export function useTypingEffect(text, speed = 30) {
  const typedText = ref('');
  let intervalId = null;

  const startTyping = () => {
    let i = 0;
    intervalId = setInterval(() => {
      if (i < text.length) {
        typedText.value = text.substring(0, i + 1);
        i++;
      } else {
        clearInterval(intervalId);
      }
    }, speed);
  };

  const reset = () => {
    if (intervalId) {
      clearInterval(intervalId);
    }
    typedText.value = '';
  };

  onMounted(() => {
    startTyping();
  });

  onUnmounted(() => {
    if (intervalId) {
      clearInterval(intervalId);
    }
  });

  return {
    typedText,
    reset,
    startTyping
  };
}
