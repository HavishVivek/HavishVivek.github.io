<script setup>
import { onMounted } from 'vue';
import HeroSection from '../components/HeroSection.vue';
import ProjectsSection from '../components/ProjectsSection.vue';
import VideosSection from '../components/VideosSection.vue';
import BlogSection from '../components/BlogSection.vue';
import ContactSection from '../components/ContactSection.vue';

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    },
    { threshold: 0.1 }
  );

  setTimeout(() => {
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
      observer.observe(el);
    });
  }, 100);
});
</script>

<template>
  <main>
    <HeroSection />
    <ProjectsSection />
    <VideosSection />
    <BlogSection />
    <ContactSection />
  </main>
</template>
