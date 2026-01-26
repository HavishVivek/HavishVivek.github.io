<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getProjectById } from '../data/projects.js';
import { videos } from '../data/videos.js';
import ProjectComponents from '../components/ProjectComponents.vue';
import ProjectAIChat from '../components/ProjectAIChat.vue';

const route = useRoute();
const router = useRouter();

const project = computed(() => getProjectById(route.params.id));
const activeTab = ref('project');

// Get video if project has one
const projectVideo = computed(() => {
  if (!project.value?.videoId) return null;
  return videos.find(v => v.videoId === project.value.videoId);
});

// Check which tabs are available
const availableTabs = computed(() => {
  const tabs = [{ id: 'project', label: 'Project Details', icon: 'folder' }];

  if (project.value?.components?.length > 0) {
    tabs.push({ id: 'components', label: 'Components', icon: 'cpu' });
  }

  if (project.value?.videoId) {
    tabs.push({ id: 'video', label: 'Video Demo', icon: 'play' });
  }

  if (project.value?.blogPost) {
    tabs.push({ id: 'blog', label: 'Blog Post', icon: 'file-text' });
  }

  return tabs;
});

const goBack = () => {
  router.push('/#projects');
};

// Simple markdown-like rendering for content
const renderContent = (content) => {
  if (!content) return '';

  return content
    // Headers
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Code blocks
    .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Lists
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>')
    // Wrap consecutive li elements in ul
    .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
    // Paragraphs (lines that aren't already wrapped)
    .replace(/^(?!<[huplo]|$)(.+)$/gm, '<p>$1</p>')
    // Clean up extra whitespace
    .replace(/\n{3,}/g, '\n\n');
};

onMounted(() => {
  if (!project.value) {
    router.push('/');
  }
});
</script>

<template>
  <div class="project-page" v-if="project">
    <!-- Header -->
    <header class="project-header">
      <div class="container">
        <button class="back-btn" @click="goBack">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          <span>Back to Projects</span>
        </button>

        <div class="project-hero">
          <div class="project-hero-content">
            <span class="project-category">{{ project.category }}</span>
            <h1 class="project-title">{{ project.title }}</h1>
            <p class="project-description">{{ project.description }}</p>

            <div class="project-tech">
              <span v-for="tech in project.tech" :key="tech">{{ tech }}</span>
            </div>

            <div class="project-links">
              <a :href="project.demo" target="_blank" class="btn btn-primary">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polygon points="10 8 16 12 10 16 10 8"/>
                </svg>
                Live Demo
              </a>
              <a :href="project.github" target="_blank" class="btn btn-secondary">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                GitHub
              </a>
            </div>
          </div>

          <div class="project-hero-image">
            <img :src="project.image" :alt="project.title">
          </div>
        </div>
      </div>
    </header>

    <!-- Tabs -->
    <nav class="project-tabs">
      <div class="container">
        <div class="tabs-list">
          <button
            v-for="tab in availableTabs"
            :key="tab.id"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            <svg v-if="tab.icon === 'folder'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
            </svg>
            <svg v-if="tab.icon === 'cpu'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="4" y="4" width="16" height="16" rx="2" ry="2"/>
              <rect x="9" y="9" width="6" height="6"/>
              <line x1="9" y1="1" x2="9" y2="4"/>
              <line x1="15" y1="1" x2="15" y2="4"/>
              <line x1="9" y1="20" x2="9" y2="23"/>
              <line x1="15" y1="20" x2="15" y2="23"/>
              <line x1="20" y1="9" x2="23" y2="9"/>
              <line x1="20" y1="14" x2="23" y2="14"/>
              <line x1="1" y1="9" x2="4" y2="9"/>
              <line x1="1" y1="14" x2="4" y2="14"/>
            </svg>
            <svg v-if="tab.icon === 'play'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
            <svg v-if="tab.icon === 'file-text'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
            <span>{{ tab.label }}</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Tab Content -->
    <main class="project-content">
      <div class="container">
        <!-- Project Details Tab -->
        <div v-show="activeTab === 'project'" class="tab-panel">
          <article class="content-article" v-html="renderContent(project.content)"></article>
        </div>

        <!-- Components Tab -->
        <div v-show="activeTab === 'components'" class="tab-panel tab-panel-full">
          <ProjectComponents
            :components="project.components"
            :schematic="project.schematic"
          />
        </div>

        <!-- Video Demo Tab -->
        <div v-show="activeTab === 'video'" class="tab-panel">
          <div class="video-demo-section" v-if="projectVideo">
            <div class="video-player-large">
              <iframe
                :src="`https://www.youtube.com/embed/${project.videoId}`"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              ></iframe>
            </div>
            <div class="video-info">
              <h2>{{ projectVideo.title }}</h2>
              <p>{{ projectVideo.description }}</p>
              <a
                :href="`https://www.youtube.com/watch?v=${project.videoId}`"
                target="_blank"
                class="youtube-link"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
                Watch on YouTube
              </a>
            </div>
          </div>
          <div v-else class="no-content">
            <p>No video demo available for this project.</p>
          </div>
        </div>

        <!-- Blog Post Tab -->
        <div v-show="activeTab === 'blog'" class="tab-panel">
          <article v-if="project.blogPost" class="blog-article">
            <header class="blog-header">
              <h1>{{ project.blogPost.title }}</h1>
            </header>
            <div class="content-article" v-html="renderContent(project.blogPost.content)"></div>
          </article>
          <div v-else class="no-content">
            <p>No blog post available for this project.</p>
          </div>
        </div>
      </div>
    </main>

    <!-- AI Chat Assistant -->
    <ProjectAIChat :project="project" />
  </div>
</template>

<style scoped>
.project-page {
  min-height: 100vh;
  padding-top: 80px;
}

/* Header */
.project-header {
  padding: 40px 0 60px;
  background: linear-gradient(180deg, rgba(99, 102, 241, 0.05) 0%, transparent 100%);
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 0.9rem;
  cursor: pointer;
  transition: var(--transition);
  margin-bottom: 32px;
}

.back-btn:hover {
  border-color: var(--primary);
  color: var(--text-primary);
}

.project-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}

.project-hero-content .project-category {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--primary-light);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.project-hero-content .project-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 16px;
  line-height: 1.2;
}

.project-hero-content .project-description {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 24px;
  line-height: 1.6;
}

.project-hero-content .project-tech {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 32px;
}

.project-hero-content .project-tech span {
  padding: 6px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-secondary);
}

.project-links {
  display: flex;
  gap: 16px;
}

.project-hero-image {
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border);
}

.project-hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Tabs */
.project-tabs {
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 70px;
  z-index: 100;
}

.tabs-list {
  display: flex;
  gap: 8px;
  padding: 12px 0;
}

.tabs-list button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.tabs-list button:hover {
  color: var(--text-primary);
  background: rgba(99, 102, 241, 0.05);
}

.tabs-list button.active {
  color: var(--primary-light);
  background: rgba(99, 102, 241, 0.1);
  border-color: rgba(99, 102, 241, 0.3);
}

.tabs-list button svg {
  opacity: 0.7;
}

.tabs-list button.active svg {
  opacity: 1;
}

/* Content */
.project-content {
  padding: 60px 0 120px;
}

.tab-panel {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Article Styles */
.content-article {
  max-width: 800px;
}

.content-article :deep(h1) {
  font-size: 2rem;
  font-weight: 700;
  margin: 40px 0 20px;
  color: var(--text-primary);
}

.content-article :deep(h2) {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 32px 0 16px;
  color: var(--text-primary);
}

.content-article :deep(h3) {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 24px 0 12px;
  color: var(--text-primary);
}

.content-article :deep(p) {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.8;
  margin-bottom: 16px;
}

.content-article :deep(ul) {
  margin: 16px 0;
  padding-left: 24px;
}

.content-article :deep(li) {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.8;
  margin-bottom: 8px;
}

.content-article :deep(li)::marker {
  color: var(--primary);
}

.content-article :deep(strong) {
  color: var(--text-primary);
  font-weight: 600;
}

.content-article :deep(code) {
  padding: 2px 8px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9em;
  color: var(--accent);
}

.content-article :deep(pre) {
  margin: 24px 0;
  padding: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  overflow-x: auto;
}

.content-article :deep(pre code) {
  padding: 0;
  background: none;
  border: none;
  font-size: 0.85rem;
  line-height: 1.6;
  color: var(--text-secondary);
}

/* Video Demo Section */
.video-demo-section {
  max-width: 900px;
}

.video-player-large {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border);
  margin-bottom: 24px;
}

.video-player-large iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.video-info h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 12px;
}

.video-info p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 20px;
}

.youtube-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: #ff0000;
  border-radius: var(--radius-sm);
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  transition: var(--transition);
}

.youtube-link:hover {
  background: #cc0000;
  transform: translateY(-2px);
}

/* Blog Article */
.blog-article {
  max-width: 800px;
}

.blog-header {
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
}

.blog-header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.2;
}

/* No Content */
.no-content {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

/* Full-width tab panel for components */
.tab-panel-full {
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
  width: 100vw;
  max-width: 100vw;
  padding: 0 24px;
}

/* Responsive */
@media (max-width: 1024px) {
  .project-hero {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .project-hero-content .project-title {
    font-size: 2rem;
  }

  .project-hero-image {
    order: -1;
  }
}

@media (max-width: 768px) {
  .project-header {
    padding: 24px 0 40px;
  }

  .project-hero-content .project-title {
    font-size: 1.75rem;
  }

  .project-links {
    flex-direction: column;
  }

  .tabs-list {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .tabs-list button {
    padding: 10px 16px;
    white-space: nowrap;
  }

  .tabs-list button span {
    display: none;
  }

  .project-content {
    padding: 40px 0 80px;
  }

  .blog-header h1 {
    font-size: 1.75rem;
  }
}
</style>
