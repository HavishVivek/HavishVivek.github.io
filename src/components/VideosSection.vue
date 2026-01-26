<script setup>
import { ref, computed, watch, nextTick } from 'vue';
import { videos, videoCategories } from '../data/videos.js';
import { siteConfig } from '../data/config.js';
import VideoExpandedView from './VideoExpandedView.vue';

const showExpandedView = ref(false);
const activeVideo = ref(null);
const activeFilter = ref('All');
const showAll = ref(false);

const filteredVideos = computed(() => {
  let filtered = videos;
  if (activeFilter.value !== 'All') {
    filtered = videos.filter(v => v.category === activeFilter.value);
  }
  // Show only first 6 unless "showAll" is true
  return showAll.value ? filtered : filtered.slice(0, 6);
});

const totalFilteredCount = computed(() => {
  if (activeFilter.value === 'All') return videos.length;
  return videos.filter(v => v.category === activeFilter.value).length;
});

const hasMoreVideos = computed(() => {
  return totalFilteredCount.value > 6 && !showAll.value;
});

const openVideo = (video) => {
  activeVideo.value = video;
  showExpandedView.value = true;
};

const closeVideo = () => {
  showExpandedView.value = false;
  activeVideo.value = null;
};

const toggleShowAll = () => {
  showAll.value = !showAll.value;
};

const openOnYouTube = (videoId) => {
  window.open(`https://www.youtube.com/watch?v=${videoId}`, '_blank');
};

const setFilter = (category) => {
  activeFilter.value = category;
  showAll.value = false;
};

// Re-observe elements when filter or showAll changes
const observeVideos = async () => {
  await nextTick();
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

  document.querySelectorAll('#videos .video-card:not(.visible)').forEach(el => {
    observer.observe(el);
  });
};

watch([showAll, activeFilter], observeVideos);
</script>

<template>
  <section id="videos" class="section videos-section">
    <div class="container">
      <div class="section-header animate-on-scroll">
        <span class="section-tag">Content</span>
        <h2 class="section-title">Video Tutorials</h2>
        <p class="section-subtitle">Deep dives into Electronics, IoT, and AI projects</p>
      </div>

      <div class="video-filters">
        <button
          v-for="category in videoCategories"
          :key="category"
          :class="{ active: activeFilter === category }"
          @click="setFilter(category)"
        >
          {{ category }}
        </button>
      </div>

      <div class="videos-grid">
        <article
          v-for="(video, index) in filteredVideos"
          :key="video.id"
          class="video-card visible"
          :style="{ animationDelay: (index * 0.05) + 's' }"
        >
          <div class="video-thumbnail" @click="openVideo(video)">
            <img :src="video.thumbnail" :alt="video.title">
            <div class="play-button">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z"/>
              </svg>
            </div>
          </div>
          <div class="video-content">
            <div class="video-meta">
              <span class="video-category">{{ video.category }}</span>
            </div>
            <h3 class="video-title">{{ video.title }}</h3>
            <p class="video-description">{{ video.description }}</p>
            <button class="video-link" @click="openOnYouTube(video.videoId)">
              Watch on YouTube
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                <polyline points="15 3 21 3 21 9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
            </button>
          </div>
        </article>
      </div>

      <div class="videos-actions">
        <button v-if="hasMoreVideos" @click="toggleShowAll" class="btn btn-secondary">
          <span>Show All {{ totalFilteredCount }} Videos</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </button>
        <button v-if="showAll && totalFilteredCount > 6" @click="toggleShowAll" class="btn btn-secondary">
          <span>Show Less</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="18 15 12 9 6 15"/>
          </svg>
        </button>
        <a :href="siteConfig.youtubeChannel" target="_blank" class="btn btn-primary">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
          <span>Subscribe on YouTube</span>
        </a>
      </div>
    </div>

    <VideoExpandedView
      v-if="showExpandedView && activeVideo"
      :video="activeVideo"
      @close="closeVideo"
    />
  </section>
</template>

<style scoped>
.video-filters {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 48px;
  flex-wrap: wrap;
}

.video-filters button {
  padding: 8px 16px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 50px;
  transition: var(--transition);
  cursor: pointer;
}

.video-filters button:hover,
.video-filters button.active {
  color: var(--text-primary);
  border-color: var(--secondary);
  background: rgba(6, 182, 212, 0.1);
}

.videos-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 48px;
  flex-wrap: wrap;
}

.video-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--secondary);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  transition: var(--transition);
}

.video-link:hover {
  color: var(--accent);
}

.video-link svg {
  transition: var(--transition);
}

.video-link:hover svg {
  transform: translateX(4px);
}

/* Make sure visible cards show properly */
.video-card.visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
