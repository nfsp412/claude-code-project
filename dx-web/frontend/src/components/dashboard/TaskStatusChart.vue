<template>
  <div class="bg-dx-card border border-dx-border rounded-lg p-5">
    <h3 class="text-[15px] font-semibold text-dx-text-primary mb-4">任务状态分布</h3>
    <!-- CSS-only donut chart -->
    <div class="flex items-center gap-6">
      <div class="relative w-40 h-40 flex-shrink-0">
        <svg viewBox="0 0 160 160" class="w-full h-full -rotate-90">
          <circle cx="80" cy="80" r="60" fill="none" stroke="#1E293B" stroke-width="24" />
          <circle
            v-for="(seg, i) in segments"
            :key="i"
            cx="80" cy="80" r="60"
            fill="none"
            :stroke="seg.color"
            stroke-width="24"
            :stroke-dasharray="seg.dashArray"
            :stroke-dashoffset="seg.dashOffset"
            stroke-linecap="butt"
          />
        </svg>
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <span class="text-2xl font-bold text-dx-text-primary">{{ total }}</span>
          <span class="text-2xs text-dx-text-muted">总任务数</span>
        </div>
      </div>
      <div class="flex flex-col gap-3">
        <div v-for="seg in segments" :key="seg.label" class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-sm flex-shrink-0" :style="{ backgroundColor: seg.color }" />
          <span class="text-xs text-dx-text-secondary">{{ seg.label }}</span>
          <span class="text-xs font-semibold text-dx-text-primary ml-auto">{{ seg.value }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const total = 4048;
const data = [
  { label: '运行中', value: 142, color: '#06B6D4' },
  { label: '成功', value: 3827, color: '#10B981' },
  { label: '失败', value: 23, color: '#EF4444' },
  { label: '等待中', value: 56, color: '#F59E0B' },
];

const circumference = 2 * Math.PI * 60;
const segments = (() => {
  let offset = 0;
  return data.map((d) => {
    const pct = d.value / total;
    const dashArray = `${pct * circumference} ${(1 - pct) * circumference}`;
    const dashOffset = -offset * circumference;
    offset += pct;
    return { ...d, dashArray, dashOffset };
  });
})();
</script>
