<script setup>
import { RouterView } from 'vue-router';
import ParticleBackground from './components/ParticleBackground.vue';
import NavBar from './components/NavBar.vue';
import FooterSection from './components/FooterSection.vue';
</script>

<template>
  <div id="app">
    <ParticleBackground />
    <NavBar />
    <RouterView />
    <FooterSection />
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
@import './assets/styles/main.css';
</style>
