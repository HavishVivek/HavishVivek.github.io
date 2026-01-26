<script setup>
import { ref, computed } from 'vue';
import { RouterLink } from 'vue-router';
import { projects, projectFilters } from '../data/projects.js';

const activeFilter = ref('All');

const filteredProjects = computed(() => {
  if (activeFilter.value === 'All') return projects;
  return projects.filter(p => p.category === activeFilter.value);
});
</script>

<template>
  <section id="projects" class="section projects-section">
    <div class="container">
      <div class="section-header animate-on-scroll">
        <span class="section-tag">Portfolio</span>
        <h2 class="section-title">Featured Projects</h2>
        <p class="section-subtitle">Exploring the intersection of hardware and intelligence</p>
      </div>

      <div class="project-filters">
        <button
          v-for="filter in projectFilters"
          :key="filter"
          :class="{ active: activeFilter === filter }"
          @click="activeFilter = filter"
        >
          {{ filter }}
        </button>
      </div>

      <div class="projects-grid">
        <article
          v-for="(project, index) in filteredProjects"
          :key="project.id"
          class="project-card animate-on-scroll"
          :style="{ animationDelay: (index * 0.1) + 's' }"
        >
          <div class="project-image">
            <img :src="project.image" :alt="project.title">
            <div class="project-overlay">
              <RouterLink :to="`/project/${project.id}`" class="project-link primary">View Details</RouterLink>
              <a :href="project.demo" target="_blank" class="project-link" @click.stop>Live Demo</a>
              <a :href="project.github" target="_blank" class="project-link" @click.stop>GitHub</a>
            </div>
          </div>
          <div class="project-content">
            <RouterLink :to="`/project/${project.id}`" class="project-card-link">
              <div class="project-category">{{ project.category }}</div>
              <h3 class="project-title">{{ project.title }}</h3>
              <p class="project-description">{{ project.description }}</p>
            </RouterLink>
            <div class="project-tech">
              <span v-for="tech in project.tech" :key="tech">{{ tech }}</span>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.project-card-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.project-card-link:hover .project-title {
  color: var(--primary-light);
}

.project-link.primary {
  background: var(--gradient-1);
  box-shadow: var(--shadow-glow);
}

.project-link.primary:hover {
  transform: scale(1.05);
}

.project-overlay {
  flex-wrap: wrap;
  justify-content: center;
}
</style>
