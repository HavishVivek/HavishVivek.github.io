<script setup>
import { ref } from 'vue';
import { siteConfig } from '../data/config.js';

const isSubmitting = ref(false);
const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
});

const submitForm = async () => {
  isSubmitting.value = true;
  // Simulate form submission - replace with your actual form handling
  await new Promise(resolve => setTimeout(resolve, 1500));
  alert('Thank you for your message! I\'ll get back to you soon.');
  form.value = { name: '', email: '', subject: '', message: '' };
  isSubmitting.value = false;
};
</script>

<template>
  <section id="contact" class="section contact-section">
    <div class="container">
      <div class="contact-wrapper">
        <div class="contact-info animate-on-scroll">
          <span class="section-tag">Get In Touch</span>
          <h2 class="section-title">Let's Build Something Amazing</h2>
          <p class="contact-description">{{ siteConfig.contactDescription }}</p>

          <div class="contact-details">
            <a :href="'mailto:' + siteConfig.email" class="contact-item">
              <div class="contact-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
              </div>
              <div>
                <span class="label">Email</span>
                <span class="value">{{ siteConfig.email }}</span>
              </div>
            </a>
            <a :href="siteConfig.github" target="_blank" class="contact-item">
              <div class="contact-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </div>
              <div>
                <span class="label">GitHub</span>
                <span class="value">{{ siteConfig.githubUsername }}</span>
              </div>
            </a>
            <a :href="siteConfig.twitter" target="_blank" class="contact-item">
              <div class="contact-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
              </div>
              <div>
                <span class="label">Twitter/X</span>
                <span class="value">{{ siteConfig.twitterHandle }}</span>
              </div>
            </a>
            <a :href="siteConfig.linkedin" target="_blank" class="contact-item">
              <div class="contact-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </div>
              <div>
                <span class="label">LinkedIn</span>
                <span class="value">Connect</span>
              </div>
            </a>
          </div>
        </div>

        <form class="contact-form animate-on-scroll" @submit.prevent="submitForm">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" v-model="form.name" required placeholder="Your name">
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="form.email" required placeholder="your@email.com">
          </div>
          <div class="form-group">
            <label for="subject">Subject</label>
            <input type="text" id="subject" v-model="form.subject" required placeholder="What's this about?">
          </div>
          <div class="form-group">
            <label for="message">Message</label>
            <textarea id="message" v-model="form.message" required rows="5" placeholder="Tell me about your project..."></textarea>
          </div>
          <button type="submit" class="btn btn-primary btn-full" :disabled="isSubmitting">
            <span v-if="!isSubmitting">Send Message</span>
            <span v-else>Sending...</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </form>
      </div>
    </div>
  </section>
</template>
