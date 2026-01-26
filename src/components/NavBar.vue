<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import { siteConfig } from '../data/config.js';

const route = useRoute();
const isScrolled = ref(false);
const mobileMenuOpen = ref(false);

const isHomePage = computed(() => route.path === '/');

const sections = ['home', 'projects', 'videos', 'blog', 'contact'];
const activeSection = ref('home');

const scrollTo = (sectionId) => {
  mobileMenuOpen.value = false;
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;

  if (isHomePage.value) {
    for (const section of sections) {
      const element = document.getElementById(section);
      if (element) {
        const rect = element.getBoundingClientRect();
        if (rect.top <= 150 && rect.bottom >= 150) {
          activeSection.value = section;
          break;
        }
      }
    }
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="nav-container">
      <RouterLink to="/" class="logo">
        <span class="logo-bracket">&lt;</span>
        <span class="logo-text">{{ siteConfig.name }}</span>
        <span class="logo-bracket">/&gt;</span>
      </RouterLink>

      <div class="nav-links" :class="{ 'active': mobileMenuOpen }">
        <template v-if="isHomePage">
          <a
            v-for="section in sections"
            :key="section"
            :href="`#${section}`"
            @click.prevent="scrollTo(section)"
            :class="{ active: activeSection === section }"
          >
            {{ section.charAt(0).toUpperCase() + section.slice(1) }}
          </a>
        </template>
        <template v-else>
          <RouterLink to="/">Home</RouterLink>
        </template>
      </div>

      <div class="nav-actions">
        <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
          <span :class="{ 'open': mobileMenuOpen }"></span>
        </button>
      </div>
    </div>
  </nav>

</template>

<style scoped>
.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

@media (max-width: 768px) {
  .nav-links {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: rgba(10, 10, 15, 0.98);
    backdrop-filter: blur(20px);
    flex-direction: column;
    padding: 24px;
    gap: 16px;
    border-bottom: 1px solid var(--border);
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: var(--transition);
    z-index: 100;
  }

  .nav-links.active {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }
}
</style>
