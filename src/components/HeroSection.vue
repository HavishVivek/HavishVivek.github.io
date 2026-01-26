<script setup>
import { siteConfig, codeSnippet } from '../data/config.js';
import { useTypingEffect } from '../composables/useTypingEffect.js';

const { typedText } = useTypingEffect(codeSnippet, 30);

const scrollTo = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};
</script>

<template>
  <section id="home" class="hero">
    <div class="hero-content">
      <div class="hero-badge">{{ siteConfig.badge }}</div>
      <h1 class="hero-title">
        <span
          v-for="(line, index) in siteConfig.heroTitle"
          :key="index"
          class="line"
          :style="{ animationDelay: (index * 0.2) + 's' }"
        >
          {{ line }}
        </span>
      </h1>
      <p class="hero-description">{{ siteConfig.description }}</p>
      <div class="hero-cta">
        <a href="#projects" @click.prevent="scrollTo('projects')" class="btn btn-primary">
          <span>View My Work</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </a>
        <a href="#contact" @click.prevent="scrollTo('contact')" class="btn btn-secondary">Get In Touch</a>
      </div>
      <div class="tech-stack">
        <span class="tech-label">Tech Stack:</span>
        <div class="tech-icons">
          <span v-for="tech in siteConfig.techStack" :key="tech" class="tech-badge">{{ tech }}</span>
        </div>
      </div>
    </div>
    <div class="hero-visual">
      <div class="code-window">
        <div class="window-header">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
          <span class="file-name">portfolio.js</span>
        </div>
        <pre class="code-content"><code>{{ typedText }}</code><span class="cursor">|</span></pre>
      </div>
    </div>
    <div class="scroll-indicator" @click="scrollTo('projects')">
      <span>Scroll</span>
      <div class="mouse">
        <div class="wheel"></div>
      </div>
    </div>
  </section>
</template>
