<template>
  <div class="bg-dx-card border border-dx-border rounded-lg p-5">
    <h3 class="text-[15px] font-semibold text-dx-text-primary mb-4">任务执行趋势</h3>
    <!-- CSS-only chart placeholder: bar chart -->
    <div class="flex items-end gap-2 h-48 px-2">
      <div v-for="(bar, i) in bars" :key="i" class="flex-1 flex flex-col items-center gap-2">
        <div
          class="w-full rounded-sm transition-all duration-500"
          :style="{ height: bar.runHeight + 'px', backgroundColor: '#06B6D4' }"
        />
        <div
          class="w-full rounded-sm transition-all duration-500"
          :style="{ height: bar.failHeight + 'px', backgroundColor: '#EF4444' }"
        />
        <span class="text-2xs text-dx-text-muted mt-1">{{ bar.label }}</span>
      </div>
    </div>
    <div class="flex items-center justify-center gap-5 mt-4 pt-3 border-t border-dx-border">
      <div class="flex items-center gap-1.5">
        <span class="w-2.5 h-2.5 rounded-sm bg-cyan-400" />
        <span class="text-xs text-dx-text-muted">运行成功</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-2.5 h-2.5 rounded-sm bg-red-400" />
        <span class="text-xs text-dx-text-muted">运行失败</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const maxHeight = 140;
const bars = [
  { label: '一', run: 68, fail: 3 },
  { label: '二', run: 75, fail: 2 },
  { label: '三', run: 81, fail: 5 },
  { label: '四', run: 72, fail: 1 },
  { label: '五', run: 88, fail: 4 },
  { label: '六', run: 63, fail: 2 },
  { label: '日', run: 55, fail: 6 },
].map((d) => ({
  ...d,
  runHeight: (d.run / 100) * maxHeight,
  failHeight: (d.fail / 10) * maxHeight,
}));
</script>
