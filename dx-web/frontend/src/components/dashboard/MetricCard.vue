<template>
  <div class="bg-dx-card border border-dx-border rounded-lg p-5 hover:bg-dx-card-hover hover:border-dx-border-active/30 transition-all duration-200 cursor-default">
    <div class="flex items-start justify-between mb-3">
      <span class="text-xs font-medium text-dx-text-muted tracking-wide uppercase">{{ title }}</span>
      <div
        class="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0"
        :class="iconBgClass"
      >
        <svg class="w-5 h-5" :class="iconColorClass" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
          <component :is="iconPath" />
        </svg>
      </div>
    </div>
    <div class="text-[28px] font-bold text-dx-text-primary mb-1.5 leading-none">{{ formattedValue }}</div>
    <div class="flex items-center gap-1.5">
      <span
        class="inline-flex items-center gap-0.5 text-xs font-medium px-1.5 py-0.5 rounded"
        :class="changeColorClass"
      >
        <svg v-if="change !== 0" class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path v-if="change > 0" stroke-linecap="round" stroke-linejoin="round" d="M12 19V5M5 12l7-7 7 7"/>
          <path v-else stroke-linecap="round" stroke-linejoin="round" d="M12 5v14M5 12l7 7 7-7"/>
        </svg>
        <span>{{ changeLabel }}</span>
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, h } from 'vue';

const props = defineProps<{
  title: string;
  value: number | string;
  change: number;
  changeLabel: string;
  color: 'accent' | 'success' | 'warning' | 'danger';
}>();

const iconMap: Record<string, () => ReturnType<typeof h>> = {
  accent: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M13 10V3L4 14h7v7l9-11h-7z' }),
  success: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' }),
  warning: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 8v4m0 4h.01M12 2a10 10 0 100 20 10 10 0 000-20z' }),
  danger: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 9v2m0 4h.01M12 3a9 9 0 100 18 9 9 0 000-18z' }),
};

const iconPath = computed(() => iconMap[props.color]);

const formattedValue = computed(() => {
  if (typeof props.value === 'number' && props.value >= 1000) {
    return props.value.toLocaleString('zh-CN');
  }
  return String(props.value);
});

const iconBgClass = computed(() => {
  const map: Record<string, string> = {
    accent: 'bg-cyan-500/10',
    success: 'bg-emerald-500/10',
    warning: 'bg-amber-500/10',
    danger: 'bg-red-500/10',
  };
  return map[props.color];
});

const iconColorClass = computed(() => {
  const map: Record<string, string> = {
    accent: 'text-cyan-400',
    success: 'text-emerald-400',
    warning: 'text-amber-400',
    danger: 'text-red-400',
  };
  return map[props.color];
});

const changeColorClass = computed(() => {
  if (props.change > 0) return 'text-emerald-400 bg-emerald-500/10';
  if (props.change < 0) return 'text-red-400 bg-red-500/10';
  return 'text-dx-text-muted bg-dx-input';
});
</script>
