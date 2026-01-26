<script setup>
const particleStyle = (n) => {
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  const delay = Math.random() * 20;
  const duration = 15 + Math.random() * 10;
  const size = 2 + Math.random() * 4;
  return {
    left: `${x}%`,
    top: `${y}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  };
};
</script>

<template>
  <div class="bg-animation">
    <div
      v-for="n in 50"
      :key="n"
      class="particle"
      :style="particleStyle(n)"
    ></div>
  </div>
</template>
