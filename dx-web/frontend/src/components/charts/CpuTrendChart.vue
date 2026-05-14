<template>
  <div class="bg-dx-card border border-dx-border rounded-lg p-5 col-span-2">
    <h3 class="text-sm font-semibold text-dx-text-primary mb-4">CPU 使用趋势</h3>
    <VChart :option="chartOption" autoresize class="h-52" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import VChart from 'vue-echarts';
import 'echarts';
import { graphic } from 'echarts';
import { useEchartsTheme, DX_CHART_COLORS } from '@/composables/useEchartsTheme';

const dataCount = 24;
const points = Array.from({ length: dataCount }, () => ({
  avg: 30 + Math.random() * 50,
  peak: 45 + Math.random() * 40,
}));

const timeLabels = Array.from({ length: dataCount }, (_, i) => {
  const totalMinutes = 14 * 60 + i * 15;
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
});

const { baseOption } = useEchartsTheme();

const chartOption = computed(() => ({
  ...baseOption.value,

  tooltip: {
    ...baseOption.value.tooltip,
    trigger: 'axis' as const,
  },

  legend: {
    data: ['平均使用率', '峰值使用率'],
    top: 0,
    right: 0,
    textStyle: { color: DX_CHART_COLORS.textSecondary, fontSize: 12 },
    icon: 'roundRect',
    itemWidth: 10,
    itemHeight: 10,
  },

  grid: {
    left: 4,
    right: 12,
    top: 36,
    bottom: 24,
  },

  xAxis: {
    type: 'category' as const,
    data: timeLabels,
    boundaryGap: false,
    axisLabel: {
      color: DX_CHART_COLORS.textMuted,
      fontSize: 10,
      interval: 3,
      formatter: (_value: string, index: number) => {
        if (index === dataCount - 1) return '现在';
        return timeLabels[index];
      },
    },
    axisLine: { lineStyle: { color: DX_CHART_COLORS.border } },
    axisTick: { show: false },
  },

  yAxis: {
    type: 'value' as const,
    max: 100,
    axisLabel: {
      color: DX_CHART_COLORS.textMuted,
      fontSize: 10,
      formatter: '{value}%',
    },
    splitLine: { lineStyle: { color: DX_CHART_COLORS.border, type: 'dashed' as const } },
  },

  series: [
    {
      name: '峰值使用率',
      type: 'line',
      smooth: true,
      symbol: 'none',
      data: points.map((p) => p.peak),
      lineStyle: { color: DX_CHART_COLORS.warning, width: 1.5 },
      areaStyle: {
        color: new graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(245, 158, 11, 0.25)' },
          { offset: 1, color: 'rgba(245, 158, 11, 0.02)' },
        ]),
      },
    },
    {
      name: '平均使用率',
      type: 'line',
      smooth: true,
      symbol: 'none',
      data: points.map((p) => p.avg),
      lineStyle: { color: DX_CHART_COLORS.accent, width: 1.5 },
      areaStyle: {
        color: new graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(6, 182, 212, 0.4)' },
          { offset: 1, color: 'rgba(6, 182, 212, 0.02)' },
        ]),
      },
    },
  ],
}));
</script>
