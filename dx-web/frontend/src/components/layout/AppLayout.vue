<template>
  <div class="min-h-screen bg-dx-page">
    <AppNavbar />
    <div class="flex pt-14">
      <AppSidebar />
      <main
        class="flex-1 overflow-auto transition-all duration-200"
        :class="store.sidebarCollapsed ? 'ml-16' : 'ml-60'"
      >
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app';
import AppNavbar from './AppNavbar.vue';
import AppSidebar from './AppSidebar.vue';

const store = useAppStore();
</script>
