<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const canvasRef = ref<HTMLCanvasElement | null>(null);
const isActive = ref(false);
let animationId = 0;

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  color: string;
  alpha: number;
  size: number;
  decay: number;
  gravity: number;
}

interface Rocket {
  x: number;
  y: number;
  vx: number;
  vy: number;
  color: string;
  trail: { x: number; y: number; alpha: number }[];
  exploded: boolean;
  explosionY: number;
}

let rockets: Rocket[] = [];
let particles: Particle[] = [];
let ctx: CanvasRenderingContext2D | null = null;
let canvasWidth = 0;
let canvasHeight = 0;

const colors = [
  '#ff6b6b', '#ffa94d', '#ffd43b', '#69db7c',
  '#4dabf7', '#da77f2', '#f783ac', '#ff8787',
  '#74c0fc', '#ff922b', '#20c997', '#f06595',
];

function randomColor(): string {
  return colors[Math.floor(Math.random() * colors.length)];
}

function createRocket(): Rocket {
  return {
    x: Math.random() * canvasWidth * 0.8 + canvasWidth * 0.1,
    y: canvasHeight,
    vx: (Math.random() - 0.5) * 2,
    vy: -(Math.random() * 6 + 10),
    color: randomColor(),
    trail: [],
    exploded: false,
    explosionY: Math.random() * canvasHeight * 0.35 + canvasHeight * 0.1,
  };
}

function explode(rocket: Rocket) {
  const count = Math.floor(Math.random() * 40 + 60);
  for (let i = 0; i < count; i++) {
    const angle = (Math.PI * 2 * i) / count + (Math.random() - 0.5) * 0.3;
    const speed = Math.random() * 5 + 2;
    particles.push({
      x: rocket.x,
      y: rocket.y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      color: Math.random() > 0.5 ? rocket.color : randomColor(),
      alpha: 1,
      size: Math.random() * 3 + 1.5,
      decay: Math.random() * 0.02 + 0.01,
      gravity: 0.05,
    });
  }
}

function resizeCanvas() {
  if (!canvasRef.value) return;
  canvasRef.value.width = window.innerWidth;
  canvasRef.value.height = window.innerHeight;
  canvasWidth = window.innerWidth;
  canvasHeight = window.innerHeight;
}

function animate() {
  if (!ctx || !canvasRef.value) return;
  ctx.clearRect(0, 0, canvasWidth, canvasHeight);

  // Draw and update rockets
  for (let i = rockets.length - 1; i >= 0; i--) {
    const r = rockets[i];
    if (!r.exploded) {
      // Add trail
      r.trail.push({ x: r.x, y: r.y, alpha: 1 });
      if (r.trail.length > 12) r.trail.shift();

      // Update position
      r.x += r.vx;
      r.y += r.vy;
      r.vy += 0.04; // slight gravity on rocket

      if (r.y <= r.explosionY) {
        r.exploded = true;
        explode(r);
        rockets.splice(i, 1);
        continue;
      }
    }

    // Draw trail
    for (let j = 0; j < r.trail.length; j++) {
      const t = r.trail[j];
      t.alpha -= 0.06;
      if (t.alpha <= 0) continue;
      ctx.beginPath();
      ctx.arc(t.x, t.y, 2, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 220, 100, ${t.alpha * 0.7})`;
      ctx.fill();
    }

    // Draw rocket head
    ctx.beginPath();
    ctx.arc(r.x, r.y, 3, 0, Math.PI * 2);
    ctx.fillStyle = '#fff';
    ctx.fill();
  }

  // Draw and update particles
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.x += p.vx;
    p.y += p.vy;
    p.vy += p.gravity;
    p.alpha -= p.decay;

    if (p.alpha <= 0) {
      particles.splice(i, 1);
      continue;
    }

    ctx.save();
    ctx.globalAlpha = p.alpha;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fillStyle = p.color;
    ctx.fill();
    // glow effect
    ctx.shadowColor = p.color;
    ctx.shadowBlur = 6;
    ctx.fill();
    ctx.restore();
  }

  if (rockets.length > 0 || particles.length > 0) {
    animationId = requestAnimationFrame(animate);
  } else {
    isActive.value = false;
    animationId = 0;
  }
}

function launchFireworks() {
  resizeCanvas();
  if (!isActive.value) {
    isActive.value = true;
    const count = Math.floor(Math.random() * 4) + 5;
    // Push first rocket synchronously so animate() has something to render
    rockets.push(createRocket());
    for (let i = 1; i < count; i++) {
      setTimeout(() => {
        rockets.push(createRocket());
      }, i * 200);
    }
  } else {
    const count2 = Math.floor(Math.random() * 3) + 3;
    for (let i = 0; i < count2; i++) {
      setTimeout(() => {
        rockets.push(createRocket());
      }, i * 150);
    }
  }
  if (!animationId) {
    animationId = requestAnimationFrame(animate);
  }
}

onMounted(() => {
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);
  ctx = canvasRef.value?.getContext('2d') ?? null;
});

onUnmounted(() => {
  window.removeEventListener('resize', resizeCanvas);
  if (animationId) cancelAnimationFrame(animationId);
});

defineExpose({ launchFireworks });
</script>

<template>
  <canvas
    v-show="isActive"
    ref="canvasRef"
    class="fireworks-canvas"
  />
</template>

<style scoped>
.fireworks-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 9999;
}
</style>
