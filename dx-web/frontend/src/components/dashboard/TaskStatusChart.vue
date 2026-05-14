<template>
  <div class="bg-dx-card border border-dx-border rounded-lg p-5">
    <h3 class="text-[15px] font-semibold text-dx-text-primary mb-4">任务状态分布</h3>
    <div class="flex items-center gap-6">
      <VChart :option="chartOption" autoresize class="w-40 h-40 flex-shrink-0" />
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
import { computed } from 'vue';
import VChart from 'vue-echarts';
import 'echarts';
import { DX_CHART_COLORS } from '@/composables/useEchartsTheme';

const total = 4048;
const segments = [
  { label: '运行中', value: 142, color: DX_CHART_COLORS.accent },
  { label: '成功', value: 3827, color: DX_CHART_COLORS.success },
  { label: '失败', value: 23, color: DX_CHART_COLORS.danger },
  { label: '等待中', value: 56, color: DX_CHART_COLORS.warning },
];

const chartOption = computed(() => ({
  backgroundColor: 'transparent',

  tooltip: {
    trigger: 'item' as const,
    formatter: (params: { name: string; value: number; percent: number }) =>
      `${params.name}: ${params.value.toLocaleString()} (${params.percent}%)`,
    backgroundColor: DX_CHART_COLORS.cardBg,
    borderColor: DX_CHART_COLORS.border,
    textStyle: { color: DX_CHART_COLORS.textPrimary, fontSize: 12 },
  },

  series: [
    {
      type: 'pie',
      radius: ['55%', '75%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      label: { show: false },
      emphasis: {
        label: { show: true },
        scale: false,
      },
      data: segments.map((s) => ({
        value: s.value,
        name: s.label,
        itemStyle: { color: s.color },
      })),
    },
  ],

  graphic: [
    {
      type: 'text',
      left: 'center',
      top: '38%',
      style: {
        text: String(total),
        textAlign: 'center' as const,
        fill: DX_CHART_COLORS.textPrimary,
        fontSize: 26,
        fontWeight: 'bold' as const,
      },
      z: 100,
    },
    {
      type: 'text',
      left: 'center',
      top: '54%',
      style: {
        text: '总任务数',
        textAlign: 'center' as const,
        fill: DX_CHART_COLORS.textMuted,
        fontSize: 11,
      },
      z: 100,
    },
  ],
}));
</script>
