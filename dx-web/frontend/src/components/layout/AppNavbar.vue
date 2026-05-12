<template>
  <nav class="fixed top-0 left-0 right-0 z-50 h-14 bg-dx-navbar border-b border-dx-border flex items-center justify-between px-6">
    <!-- Left: Logo + Brand -->
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-md bg-dx-accent flex items-center justify-center flex-shrink-0">
        <span class="text-white text-xs font-bold">DX</span>
      </div>
      <div class="flex flex-col leading-tight">
        <span class="text-sm font-semibold text-dx-text-primary">DataX</span>
        <span class="text-2xs text-dx-text-muted">监控调度平台</span>
      </div>
    </div>

    <!-- Right: HDFS + User -->
    <div class="flex items-center gap-5">
      <div class="flex items-center gap-2 px-3 py-1.5 rounded-md bg-dx-input text-xs text-dx-text-secondary">
        <svg class="w-3.5 h-3.5 text-dx-text-muted" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
        <span class="text-dx-text-muted">HDFS:</span>
        <span class="text-dx-text-primary font-medium">{{ store.userInfo.hdfsAccount }}</span>
      </div>

      <div class="flex items-center gap-2.5">
        <div class="w-7 h-7 rounded-full bg-dx-accent-secondary flex items-center justify-center">
          <span class="text-white text-xs font-semibold">{{ store.userInfo.name.charAt(0) }}</span>
        </div>
        <span class="text-sm text-dx-text-primary font-medium">{{ store.userInfo.name }}</span>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app';

const store = useAppStore();
</script>
