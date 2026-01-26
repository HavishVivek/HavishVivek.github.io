import { onMounted, onUnmounted } from 'vue';

export function useScrollAnimation() {
  let observer = null;

  const setupObserver = () => {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.1 }
    );

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
      observer.observe(el);
    });
  };

  const cleanup = () => {
    if (observer) {
      observer.disconnect();
    }
  };

  onMounted(() => {
    // Delay to ensure DOM is ready
    setTimeout(setupObserver, 100);
  });

  onUnmounted(() => {
    cleanup();
  });

  return {
    setupObserver,
    cleanup
  };
}
