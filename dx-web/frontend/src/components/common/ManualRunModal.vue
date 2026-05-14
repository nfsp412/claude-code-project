<template>
  <Teleport to="body">
    <div
      v-if="visible"
      class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60"
      @click.self="$emit('close')"
    >
      <div class="bg-dx-card border border-dx-border rounded-xl shadow-2xl w-[540px] overflow-hidden">
        <div class="flex items-center justify-between px-5 py-4 border-b border-dx-border">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-md bg-dx-accent/10 flex items-center justify-center">
              <svg class="w-4 h-4 text-dx-accent" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            </div>
            <div>
              <h3 class="text-sm font-semibold text-dx-text-primary">手动执行任务</h3>
              <p class="text-xs text-dx-text-muted font-mono">{{ task?.id || '—' }} — {{ task?.name || '—' }}</p>
            </div>
          </div>
          <button class="w-7 h-7 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors" @click="$emit('close')">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>

        <div class="p-5 flex flex-col gap-4">
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">
              任务传参 <span class="text-dx-text-muted">(DataX)</span>
            </label>
            <input
              v-model="runParams"
              type="text"
              placeholder="例如: --channel=3 --speed=5MB/s --where=&quot;dt=20240512&quot;"
              class="w-full h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"
              @keyup.enter="$emit('confirm', runParams, runJvmArgs)"
            />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">
              JVM 参数
            </label>
            <input
              v-model="runJvmArgs"
              type="text"
              placeholder="例如: -Xms1g -Xmx4g -XX:+UseG1GC"
              class="w-full h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"
              @keyup.enter="$emit('confirm', runParams, runJvmArgs)"
            />
          </div>
        </div>

        <div class="flex items-center justify-between px-5 py-4 border-t border-dx-border bg-dx-card-hover/30">
          <span class="text-xs text-dx-text-muted">参数均为可选，确认后将立即触发任务执行</span>
          <div class="flex items-center gap-2">
            <button
              class="h-9 px-4 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
              @click="$emit('close')"
            >
              取消
            </button>
            <button
              class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5"
              @click="$emit('confirm', runParams, runJvmArgs)"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              执行
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  visible: boolean;
  task: { id: string; name: string } | null;
}>();

defineEmits<{
  close: [];
  confirm: [params: string, jvmArgs: string];
}>();

const runParams = ref('--channel=3 --speed=5MB/s');
const runJvmArgs = ref('-Xms1g -Xmx4g -XX:+UseG1GC');

watch(() => props.visible, (val) => {
  if (val) {
    runParams.value = '--channel=3 --speed=5MB/s';
    runJvmArgs.value = '-Xms1g -Xmx4g -XX:+UseG1GC';
  }
});
</script>
