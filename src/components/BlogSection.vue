<script setup>
import { blogPosts, mediumProfileUrl } from '../data/blog.js';

const openPost = (url) => {
  window.open(url, '_blank');
};
</script>

<template>
  <section id="blog" class="section blog-section">
    <div class="container">
      <div class="section-header animate-on-scroll">
        <span class="section-tag">Articles</span>
        <h2 class="section-title">Latest Blog Posts</h2>
        <p class="section-subtitle">Tutorials and insights on IoT, Electronics, and Embedded Systems</p>
      </div>

      <div class="blog-grid">
        <article
          v-for="(post, index) in blogPosts"
          :key="post.id"
          class="blog-card animate-on-scroll"
          :class="{ 'featured': post.featured }"
          :style="{ animationDelay: (index * 0.1) + 's' }"
          @click="openPost(post.url)"
        >
          <div class="blog-image">
            <img :src="post.image" :alt="post.title">
            <span class="blog-category">{{ post.category }}</span>
          </div>
          <div class="blog-content">
            <div class="blog-meta">
              <span class="blog-date">{{ post.date }}</span>
              <span class="blog-read-time">{{ post.readTime }} min read</span>
            </div>
            <h3 class="blog-title">{{ post.title }}</h3>
            <p class="blog-excerpt">{{ post.excerpt }}</p>
            <div class="blog-tags">
              <span v-for="tag in post.tags" :key="tag">#{{ tag }}</span>
            </div>
            <a :href="post.url" target="_blank" class="blog-link" @click.stop>
              Read on Medium
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                <polyline points="15 3 21 3 21 9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
            </a>
          </div>
        </article>
      </div>

      <div class="blog-cta">
        <a :href="mediumProfileUrl" target="_blank" class="btn btn-primary">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z"/>
          </svg>
          <span>View All on Medium</span>
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.blog-card {
  cursor: pointer;
}

.blog-cta {
  text-align: center;
  margin-top: 48px;
}
</style>
