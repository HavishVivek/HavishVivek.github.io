<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  components: {
    type: Array,
    default: () => []
  },
  schematic: {
    type: Object,
    default: null
  }
});

const activeIndex = ref(0);
const showSchematic = ref(false);
const sectionRef = ref(null);
const componentRefs = ref([]);
const schematicRef = ref(null);

const setComponentRef = (el, index) => {
  if (el) componentRefs.value[index] = el;
};

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const index = componentRefs.value.indexOf(entry.target);
          if (index !== -1) {
            activeIndex.value = index;
          }
          entry.target.classList.add('visible');
        }
      });
    },
    {
      threshold: 0.5,
      rootMargin: '-10% 0px -10% 0px'
    }
  );

  componentRefs.value.forEach(el => {
    if (el) observer.observe(el);
  });

  // Schematic observer
  if (schematicRef.value) {
    const schematicObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            showSchematic.value = true;
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.3 }
    );
    schematicObserver.observe(schematicRef.value);
  }
});
</script>

<template>
  <div class="project-components" ref="sectionRef" v-if="components?.length > 0">
    <!-- Section Header -->
    <div class="components-header">
      <span class="section-tag">Hardware</span>
      <h2>Components Used</h2>
      <p>Scroll to explore each component</p>
    </div>

    <!-- Progress Indicator -->
    <div class="progress-indicator">
      <div class="progress-track">
        <div
          class="progress-fill"
          :style="{ height: `${((activeIndex + 1) / components.length) * 100}%` }"
        ></div>
      </div>
      <div class="progress-dots">
        <button
          v-for="(comp, index) in components"
          :key="index"
          :class="{ active: index <= activeIndex }"
          @click="componentRefs[index]?.scrollIntoView({ behavior: 'smooth', block: 'center' })"
        >
          <span class="dot"></span>
          <span class="label">{{ comp.name }}</span>
        </button>
      </div>
    </div>

    <!-- Components List -->
    <div class="components-list">
      <div
        v-for="(component, index) in components"
        :key="index"
        :ref="el => setComponentRef(el, index)"
        class="component-item"
        :class="{ active: index === activeIndex }"
      >
        <div class="component-content">
          <div class="component-number">{{ String(index + 1).padStart(2, '0') }}</div>
          <h3 class="component-name">{{ component.name }}</h3>
          <p class="component-description">{{ component.description }}</p>

          <div class="component-specs" v-if="component.specs">
            <h4>Specifications</h4>
            <ul>
              <li v-for="(spec, i) in component.specs" :key="i">{{ spec }}</li>
            </ul>
          </div>

          <div class="component-role" v-if="component.role">
            <h4>Role in Project</h4>
            <p>{{ component.role }}</p>
          </div>
        </div>

        <div class="component-image">
          <div class="image-frame">
            <img :src="component.image" :alt="component.name">
            <div class="image-glow"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Schematic Section -->
    <div
      v-if="schematic"
      ref="schematicRef"
      class="schematic-section"
      :class="{ visible: showSchematic }"
    >
      <div class="schematic-transition">
        <div class="transition-line"></div>
        <div class="transition-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6v6l4 2"/>
          </svg>
        </div>
        <span>Circuit Design</span>
      </div>

      <div class="schematic-content">
        <div class="schematic-header">
          <span class="section-tag">Schematic</span>
          <h2>{{ schematic.title || 'Circuit Schematic' }}</h2>
          <p>{{ schematic.description || 'Complete circuit diagram and connections' }}</p>
        </div>

        <div class="schematic-images">
          <div
            v-for="(image, index) in (Array.isArray(schematic.images) ? schematic.images : [schematic.image])"
            :key="index"
            class="schematic-image"
            :style="{ animationDelay: `${index * 0.2}s` }"
          >
            <img :src="image" :alt="`Schematic ${index + 1}`">
            <div class="schematic-overlay">
              <button class="zoom-btn">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                  <line x1="11" y1="8" x2="11" y2="14"/>
                  <line x1="8" y1="11" x2="14" y2="11"/>
                </svg>
                View Full Size
              </button>
            </div>
          </div>
        </div>

        <div class="schematic-notes" v-if="schematic.notes">
          <h4>Notes</h4>
          <ul>
            <li v-for="(note, i) in schematic.notes" :key="i">{{ note }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.project-components {
  padding: 80px 0;
  position: relative;
}

.components-header {
  text-align: center;
  margin-bottom: 60px;
}

.components-header .section-tag {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(6, 182, 212, 0.1);
  border: 1px solid rgba(6, 182, 212, 0.3);
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.components-header h2 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 12px;
}

.components-header p {
  color: var(--text-muted);
  font-size: 1rem;
}

/* Progress Indicator */
.progress-indicator {
  position: fixed;
  left: 40px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 100;
  display: flex;
  gap: 12px;
}

.progress-track {
  width: 3px;
  height: 200px;
  background: var(--border);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  width: 100%;
  background: var(--gradient-1);
  border-radius: 3px;
  transition: height 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-dots {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 200px;
}

.progress-dots button {
  display: flex;
  align-items: center;
  gap: 12px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.progress-dots .dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 2px solid var(--border);
  transition: var(--transition);
}

.progress-dots button.active .dot {
  background: var(--primary);
  border-color: var(--primary);
  box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
}

.progress-dots .label {
  font-size: 0.75rem;
  color: var(--text-muted);
  opacity: 0;
  transform: translateX(-10px);
  transition: var(--transition);
  white-space: nowrap;
}

.progress-dots button:hover .label,
.progress-dots button.active .label {
  opacity: 1;
  transform: translateX(0);
  color: var(--text-primary);
}

/* Components List */
.components-list {
  display: flex;
  flex-direction: column;
  gap: 120px;
  padding-left: 100px;
}

.component-item {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  min-height: 70vh;
  opacity: 0;
  transform: translateY(60px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.component-item.visible {
  opacity: 1;
  transform: translateY(0);
}

.component-item:nth-child(even) {
  direction: rtl;
}

.component-item:nth-child(even) > * {
  direction: ltr;
}

/* Component Content */
.component-content {
  padding: 20px 0;
}

.component-number {
  font-size: 4rem;
  font-weight: 800;
  background: var(--gradient-1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  opacity: 0.3;
  line-height: 1;
  margin-bottom: 16px;
}

.component-name {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.component-description {
  font-size: 1.1rem;
  color: var(--text-secondary);
  line-height: 1.8;
  margin-bottom: 24px;
}

.component-specs h4,
.component-role h4 {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

.component-specs ul {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
}

.component-specs li {
  padding: 8px 0;
  padding-left: 20px;
  position: relative;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.component-specs li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 6px;
  height: 6px;
  background: var(--primary);
  border-radius: 50%;
}

.component-role p {
  color: var(--text-secondary);
  line-height: 1.7;
}

/* Component Image */
.component-image {
  position: relative;
}

.image-frame {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border);
  background: var(--bg-card);
}

.image-frame img {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.component-item.active .image-frame img {
  transform: scale(1.05);
}

.image-glow {
  position: absolute;
  inset: -50%;
  background: radial-gradient(circle at center, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.6s ease;
  pointer-events: none;
}

.component-item.active .image-glow {
  opacity: 1;
}

/* Schematic Section */
.schematic-section {
  margin-top: 120px;
  padding-top: 80px;
  opacity: 0;
  transform: translateY(80px);
  transition: all 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.schematic-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.schematic-transition {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 60px;
}

.transition-line {
  width: 2px;
  height: 100px;
  background: linear-gradient(to bottom, transparent, var(--primary), var(--secondary));
  animation: lineGrow 1s ease forwards;
}

@keyframes lineGrow {
  from {
    transform: scaleY(0);
    transform-origin: top;
  }
  to {
    transform: scaleY(1);
    transform-origin: top;
  }
}

.transition-icon {
  width: 64px;
  height: 64px;
  background: var(--gradient-1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: var(--shadow-glow);
  animation: iconPulse 2s ease infinite;
}

@keyframes iconPulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
  }
  50% {
    box-shadow: 0 0 40px rgba(99, 102, 241, 0.6);
  }
}

.schematic-transition span {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.schematic-header {
  text-align: center;
  margin-bottom: 48px;
}

.schematic-header .section-tag {
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

.schematic-header h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 12px;
}

.schematic-header p {
  color: var(--text-secondary);
}

.schematic-images {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.schematic-image {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border);
  background: var(--bg-card);
  opacity: 0;
  transform: scale(0.9);
  animation: schematicReveal 0.8s ease forwards;
}

.schematic-section.visible .schematic-image {
  opacity: 1;
  transform: scale(1);
}

@keyframes schematicReveal {
  from {
    opacity: 0;
    transform: scale(0.9) rotateX(10deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotateX(0);
  }
}

.schematic-image img {
  width: 100%;
  height: auto;
  display: block;
}

.schematic-overlay {
  position: absolute;
  inset: 0;
  background: rgba(10, 10, 15, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: var(--transition);
}

.schematic-image:hover .schematic-overlay {
  opacity: 1;
}

.zoom-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--gradient-1);
  border: none;
  border-radius: var(--radius-sm);
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: var(--transition);
}

.zoom-btn:hover {
  transform: scale(1.05);
}

.schematic-notes {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 24px;
}

.schematic-notes h4 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.schematic-notes ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.schematic-notes li {
  padding: 8px 0;
  padding-left: 24px;
  position: relative;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.schematic-notes li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--secondary);
}

/* Responsive */
@media (max-width: 1200px) {
  .progress-indicator {
    display: none;
  }

  .components-list {
    padding-left: 0;
  }
}

@media (max-width: 768px) {
  .component-item {
    grid-template-columns: 1fr;
    gap: 32px;
    min-height: auto;
    padding: 40px 0;
  }

  .component-item:nth-child(even) {
    direction: ltr;
  }

  .component-image {
    order: -1;
  }

  .component-number {
    font-size: 3rem;
  }

  .component-name {
    font-size: 1.5rem;
  }

  .schematic-images {
    grid-template-columns: 1fr;
  }

  .components-header h2 {
    font-size: 2rem;
  }
}
</style>
