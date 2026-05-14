<template>
  <aside
    class="fixed top-14 left-0 bottom-0 z-40 bg-dx-sidebar border-r border-dx-border flex flex-col overflow-y-auto"
    :class="store.sidebarCollapsed ? 'w-16' : 'w-60'"
  >
    <nav class="flex-1 py-4 flex flex-col gap-0.5">
      <template v-for="item in store.menuItems" :key="item.key">
        <!-- Divider before json-tool -->
        <div
          v-if="item.key === 'json-tool'"
          class="mx-4 my-2 border-t border-dx-border"
        />

        <router-link
          :to="item.path!"
          class="sidebar-item no-underline"
          :class="{ 'sidebar-item-active': store.activeMenu === item.key }"
          @click="store.setActiveMenu(item.key)"
        >
          <svg class="w-[18px] h-[18px] flex-shrink-0" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
            <component :is="iconPaths[item.icon]" />
          </svg>
          <span v-if="!store.sidebarCollapsed" class="truncate">{{ item.label }}</span>
        </router-link>
      </template>
    </nav>

    <!-- Collapse toggle -->
    <div class="p-3 border-t border-dx-border">
      <button
        class="w-full flex items-center justify-center gap-2 p-2 rounded-lg text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
        @click="store.toggleSidebar()"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path v-if="!store.sidebarCollapsed" stroke-linecap="round" stroke-linejoin="round" d="M11 19l-7-7 7-7M18 19l-7-7 7-7"/>
          <path v-else stroke-linecap="round" stroke-linejoin="round" d="M13 5l7 7-7 7M6 5l7 7-7 7"/>
        </svg>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { h } from 'vue';
import type { VNode } from 'vue';
import { useAppStore } from '@/stores/app';
const store = useAppStore();

// Inline SVG icon paths as simple VNodes
const iconPaths: Record<string, () => VNode> = {
  LayoutDashboard: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M3 3h7v7H3V3zm11 0h7v7h-7V3zM3 14h7v7H3v-7zm11 0h7v7h-7v-7z' }),
  ListChecks: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 012-2h2a2 2 0 012 2M9 12l2 2 4-4' }),
  List: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M4 6h16M4 12h16M4 18h16' }),
  Hammer: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M14.7 6.3a1 1 0 000-2.8L13.3 2l-3 3 1.4 1.4a1 1 0 002.8 0L14.7 6.3zM9.5 9.5L2 17l3 3 7.5-7.5-3-3z' }),
  Calendar: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M8 2v4M16 2v4M3 10h18M21 10V8a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2h14a2 2 0 002-2v-4M12 14v4M9 16h6' }),
  Clock: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zM12 6v6l4 2' }),
  FileText: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6M16 13H8M16 17H8M10 9H8' }),
  Database: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M4 6c0 1.657 3.582 3 8 3s8-1.343 8-3-3.582-3-8-3-8 1.343-8 3zm16 6c0 1.657-3.582 3-8 3s-8-1.343-8-3m16 6c0 1.657-3.582 3-8 3s-8-1.343-8-3' }),
  FileSearch: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6M9 15h6' }),
  Server: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2M11 17h2M11 7h2' }),
  Activity: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M22 12h-4l-3 9L9 3l-3 9H2' }),
  Braces: () =>
    h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M8 3H7a2 2 0 00-2 2v2.5c0 1.5-1 2-1 2s1 .5 1 2V14a2 2 0 002 2h1m8-14h1a2 2 0 012 2v2.5c0 1.5 1 2 1 2s-1 .5-1 2V14a2 2 0 01-2 2h-1' }),
};
</script>
