<template>
  <div class="bg-dx-card border border-dx-border rounded-lg p-5">
    <h3 class="text-sm font-semibold text-dx-text-primary mb-4">内存分布</h3>
    <VChart :option="chartOption" autoresize class="w-32 h-32 mx-auto mb-4" />
    <div class="flex flex-col gap-2 text-xs">
      <div v-for="seg in segments" :key="seg.label" class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-sm flex-shrink-0" :style="{ background: seg.color }" />
        <span class="text-dx-text-secondary">{{ seg.label }}</span>
        <span class="ml-auto text-dx-text-primary font-mono">{{ seg.value }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import VChart from 'vue-echarts';
import 'echarts';
import { DX_CHART_COLORS } from '@/composables/useEchartsTheme';

const segments = [
  { label: 'DataX Worker', value: '38 GB', rawValue: 38, color: DX_CHART_COLORS.accent },
  { label: '系统缓存', value: '28 GB', rawValue: 28, color: DX_CHART_COLORS.success },
  { label: 'JVM Heap', value: '12 GB', rawValue: 12, color: DX_CHART_COLORS.warning },
  { label: '其他', value: '8 GB', rawValue: 8, color: DX_CHART_COLORS.danger },
];

const totalPct = '78%';

const chartOption = computed(() => ({
  backgroundColor: 'transparent',

  tooltip: {
    trigger: 'item' as const,
    formatter: (params: { name: string; value: number }) => `${params.name}: ${params.value} GB`,
    backgroundColor: DX_CHART_COLORS.cardBg,
    borderColor: DX_CHART_COLORS.border,
    textStyle: { color: DX_CHART_COLORS.textPrimary, fontSize: 12 },
  },

  series: [
    {
      type: 'pie',
      radius: ['60%', '80%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      label: { show: false },
      emphasis: { scale: false },
      data: segments.map((s) => ({
        value: s.rawValue,
        name: s.label,
        itemStyle: { color: s.color },
      })),
    },
  ],

  graphic: [
    {
      type: 'text',
      left: 'center',
      top: 'center',
      style: {
        text: totalPct,
        textAlign: 'center' as const,
        fill: DX_CHART_COLORS.textPrimary,
        fontSize: 20,
        fontWeight: 'bold' as const,
      },
      z: 100,
    },
  ],
}));
</script>
