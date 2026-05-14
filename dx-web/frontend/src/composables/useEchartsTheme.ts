import { computed } from 'vue';
import type { EChartsOption } from 'echarts';

export const DX_CHART_COLORS = {
  accent: '#06B6D4',
  success: '#10B981',
  warning: '#F59E0B',
  danger: '#EF4444',
  blue: '#3B82F6',
  textPrimary: '#E2E8F0',
  textSecondary: '#94A3B8',
  textMuted: '#64748B',
  border: '#1E293B',
  cardBg: '#1A2236',
} as const;

export function useEchartsTheme() {
  const baseOption = computed<Partial<EChartsOption>>(() => ({
    backgroundColor: 'transparent',
    textStyle: { color: DX_CHART_COLORS.textPrimary },

    tooltip: {
      backgroundColor: DX_CHART_COLORS.cardBg,
      borderColor: DX_CHART_COLORS.border,
      textStyle: { color: DX_CHART_COLORS.textPrimary, fontSize: 12 },
      confine: true,
    },

    legend: {
      textStyle: { color: DX_CHART_COLORS.textSecondary, fontSize: 12 },
      icon: 'roundRect',
      itemWidth: 10,
      itemHeight: 10,
    },

    grid: {
      containLabel: true,
      borderColor: 'transparent',
      left: 8,
      right: 8,
      top: 36,
      bottom: 8,
    },

    xAxis: {
      axisLine: { lineStyle: { color: DX_CHART_COLORS.border } },
      axisTick: { lineStyle: { color: DX_CHART_COLORS.border } },
      axisLabel: { color: DX_CHART_COLORS.textMuted, fontSize: 10 },
      splitLine: { show: false },
    },

    yAxis: {
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: DX_CHART_COLORS.textMuted, fontSize: 10 },
      splitLine: { lineStyle: { color: DX_CHART_COLORS.border, type: 'dashed' as const } },
    },
  }));

  return { baseOption, DX_CHART_COLORS };
}
