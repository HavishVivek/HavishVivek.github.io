// ===== SITE CONFIGURATION =====
// Edit this file to customize your portfolio

export const siteConfig = {
  name: "YourName",
  badge: "Electronics | IoT | ML | AI",
  heroTitle: [
    "Building the Future",
    "One Circuit at a Time"
  ],
  description: "I create innovative projects at the intersection of hardware and intelligence. From smart IoT devices to machine learning systems, I turn complex ideas into working solutions.",
  techStack: ["Arduino", "ESP32", "Raspberry Pi", "Python", "TensorFlow", "MQTT", "Node.js", "KiCad"],
  email: "hello@yourdomain.com",
  github: "https://github.com/yourusername",
  githubUsername: "@yourusername",
  twitter: "https://twitter.com/yourusername",
  twitterHandle: "@yourusername",
  linkedin: "https://linkedin.com/in/yourusername",
  youtubeChannel: "https://youtube.com/@HavishStudio",
  contactDescription: "Whether you have a project in mind, want to collaborate, or just want to chat about the latest in IoT and AI, I'd love to hear from you. Let's create something amazing together!",
  footerTagline: "Crafting intelligent hardware solutions and sharing knowledge with the maker community."
};

export const codeSnippet = `const portfolio = {
  name: "${siteConfig.name}",
  skills: ["IoT", "ML", "AI"],
  passion: "Building smart things",

  createProject(idea) {
    return this.skills
      .map(skill => apply(skill, idea))
      .filter(result => result.isAwesome)
      .reduce(combine, innovation);
  }
};

// Let's build something amazing!
portfolio.createProject(yourIdea);`;
