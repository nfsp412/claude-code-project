<template>
  <div class="bg-dx-card border border-dx-border rounded-lg p-5">
    <h3 class="text-[15px] font-semibold text-dx-text-primary mb-4">任务执行趋势</h3>
    <VChart :option="chartOption" autoresize class="h-52" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import VChart from 'vue-echarts';
import 'echarts';
import { useEchartsTheme, DX_CHART_COLORS } from '@/composables/useEchartsTheme';

const rawBars = [
  { label: '一', run: 68, fail: 3 },
  { label: '二', run: 75, fail: 2 },
  { label: '三', run: 81, fail: 5 },
  { label: '四', run: 72, fail: 1 },
  { label: '五', run: 88, fail: 4 },
  { label: '六', run: 63, fail: 2 },
  { label: '日', run: 55, fail: 6 },
];

const { baseOption } = useEchartsTheme();

const chartOption = computed(() => ({
  ...baseOption.value,

  tooltip: {
    ...baseOption.value.tooltip,
    trigger: 'axis' as const,
    axisPointer: { type: 'shadow' as const },
  },

  legend: {
    data: ['运行成功', '运行失败'],
    top: 0,
    right: 0,
    textStyle: { color: DX_CHART_COLORS.textSecondary, fontSize: 12 },
    icon: 'roundRect',
    itemWidth: 10,
    itemHeight: 10,
  },

  grid: {
    left: 4,
    right: 4,
    top: 36,
    bottom: 20,
  },

  xAxis: {
    type: 'category' as const,
    data: rawBars.map((b) => b.label),
    axisLabel: { color: DX_CHART_COLORS.textMuted, fontSize: 11 },
    axisLine: { lineStyle: { color: DX_CHART_COLORS.border } },
    axisTick: { show: false },
  },

  yAxis: {
    type: 'value' as const,
    minInterval: 10,
    axisLabel: { color: DX_CHART_COLORS.textMuted, fontSize: 10 },
    splitLine: { lineStyle: { color: DX_CHART_COLORS.border, type: 'dashed' as const } },
  },

  series: [
    {
      name: '运行成功',
      type: 'bar',
      stack: 'total',
      data: rawBars.map((b) => b.run),
      itemStyle: {
        color: DX_CHART_COLORS.accent,
        borderRadius: [2, 2, 0, 0],
      },
      barWidth: 24,
    },
    {
      name: '运行失败',
      type: 'bar',
      stack: 'total',
      data: rawBars.map((b) => b.fail),
      itemStyle: {
        color: DX_CHART_COLORS.danger,
        borderRadius: [2, 2, 0, 0],
      },
      barWidth: 24,
    },
  ],
}));
</script>
