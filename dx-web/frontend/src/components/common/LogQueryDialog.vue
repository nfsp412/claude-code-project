<template>
  <Teleport to="body">
    <!-- Normal: centered modal -->
    <div
      v-if="store.logDialogVisible && !isFullscreen"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60"
      @click.self="store.closeLogDialog()"
    >
      <div class="bg-dx-card border border-dx-border rounded-xl shadow-2xl w-[800px] max-h-[85vh] overflow-hidden flex flex-col">
        <div class="flex items-center justify-between px-5 py-4 border-b border-dx-border flex-shrink-0">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-md bg-dx-accent/10 flex items-center justify-center">
              <svg class="w-4 h-4 text-dx-accent" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6M9 15h6"/>
              </svg>
            </div>
            <div>
              <h3 class="text-sm font-semibold text-dx-text-primary">日志详情</h3>
              <p class="text-xs text-dx-text-muted font-mono">{{ store.logDialogData.taskId }} — {{ store.logDialogData.taskName }}</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button
              class="w-7 h-7 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
              title="全屏展示"
              @click="isFullscreen = true"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 3H5a2 2 0 00-2 2v3m18 0V5a2 2 0 00-2-2h-3m0 18h3a2 2 0 002-2v-3M3 16v3a2 2 0 002 2h3"/>
              </svg>
            </button>
            <button class="w-7 h-7 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors" @click="store.closeLogDialog()">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>
        </div>
        <div class="flex-1 overflow-y-auto px-5 py-4" style="min-height: 0;">
          <div class="flex flex-col gap-4">
            <div class="bg-dx-input border border-dx-border rounded-lg p-4">
              <div class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                <div class="flex gap-2">
                  <span class="text-dx-text-muted flex-shrink-0">任务 ID:</span>
                  <span class="text-dx-accent font-mono">{{ store.logDialogData.taskId }}</span>
                </div>
                <div class="flex gap-2">
                  <span class="text-dx-text-muted flex-shrink-0">任务名称:</span>
                  <span class="text-dx-text-primary">{{ store.logDialogData.taskName }}</span>
                </div>
              </div>
              <div class="flex gap-2 mt-2 text-sm">
                <span class="text-dx-text-muted flex-shrink-0">任务传参:</span>
                <code class="text-dx-text-secondary font-mono text-xs">{{ store.logDialogData.params || '—' }}</code>
              </div>
            </div>
            <div class="bg-[#0c1222] border border-dx-border rounded-lg p-4 font-mono text-xs leading-relaxed overflow-auto max-h-[400px]">
              <div v-for="(line, i) in store.logDialogData.logLines" :key="i" class="flex gap-3 py-0.5">
                <span class="text-dx-text-muted flex-shrink-0 w-[95px]">{{ line.time }}</span>
                <span class="flex-shrink-0 w-[48px] font-semibold" :class="logLevelColor(line.level)">{{ line.level }}</span>
                <span class="text-dx-text-secondary break-all">{{ line.msg }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Fullscreen: content area only -->
    <div
      v-if="store.logDialogVisible && isFullscreen"
      class="fixed z-[90] bg-dx-card border-l border-dx-border shadow-2xl overflow-hidden flex flex-col"
      :style="{ top: '56px', left: store.sidebarCollapsed ? '64px' : '240px', right: '0', bottom: '0' }"
    >
      <div class="flex items-center justify-between px-5 py-4 border-b border-dx-border flex-shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-md bg-dx-accent/10 flex items-center justify-center">
            <svg class="w-4 h-4 text-dx-accent" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6M9 15h6"/>
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-dx-text-primary">日志详情</h3>
            <p class="text-xs text-dx-text-muted font-mono">{{ store.logDialogData.taskId }} — {{ store.logDialogData.taskName }}</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button
            class="w-7 h-7 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
            title="退出全屏"
            @click="isFullscreen = false"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 9V4.5M9 9H4.5M15 9h4.5M15 9V4.5M9 15v4.5M9 15H4.5M15 15h4.5M15 15v4.5"/>
            </svg>
          </button>
          <button class="w-7 h-7 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors" @click="store.closeLogDialog()">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>
      <div class="flex-1 overflow-y-auto px-5 py-4" style="min-height: 0;">
        <div class="flex flex-col gap-4">
          <div class="bg-dx-input border border-dx-border rounded-lg p-4">
            <div class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
              <div class="flex gap-2">
                <span class="text-dx-text-muted flex-shrink-0">任务 ID:</span>
                <span class="text-dx-accent font-mono">{{ store.logDialogData.taskId }}</span>
              </div>
              <div class="flex gap-2">
                <span class="text-dx-text-muted flex-shrink-0">任务名称:</span>
                <span class="text-dx-text-primary">{{ store.logDialogData.taskName }}</span>
              </div>
            </div>
            <div class="flex gap-2 mt-2 text-sm">
              <span class="text-dx-text-muted flex-shrink-0">任务传参:</span>
              <code class="text-dx-text-secondary font-mono text-xs">{{ store.logDialogData.params || '—' }}</code>
            </div>
          </div>
          <div class="bg-[#0c1222] border border-dx-border rounded-lg p-4 font-mono text-xs leading-relaxed overflow-auto flex-1">
            <div v-for="(line, i) in store.logDialogData.logLines" :key="i" class="flex gap-3 py-0.5">
              <span class="text-dx-text-muted flex-shrink-0 w-[95px]">{{ line.time }}</span>
              <span class="flex-shrink-0 w-[48px] font-semibold" :class="logLevelColor(line.level)">{{ line.level }}</span>
              <span class="text-dx-text-secondary break-all">{{ line.msg }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAppStore } from '@/stores/app';

const store = useAppStore();
const isFullscreen = ref(false);

function logLevelColor(level: string) {
  return { ERROR: 'text-red-400', WARN: 'text-amber-400', INFO: 'text-cyan-400', DEBUG: 'text-dx-text-muted' }[level] ?? 'text-dx-text-muted';
}
</script>
