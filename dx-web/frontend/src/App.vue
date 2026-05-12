<template>
  <AppLayout />
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import AppLayout from '@/components/layout/AppLayout.vue';

onMounted(() => {
  document.documentElement.classList.add('dark');
});
</script>
