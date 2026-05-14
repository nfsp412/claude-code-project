<template>
  <Teleport to="body">
    <div
      v-if="visible"
      class="fixed inset-0 z-[110] flex items-center justify-center bg-black/60"
      @click.self="$emit('cancel')"
    >
      <div class="bg-dx-card border border-dx-border rounded-xl shadow-2xl w-[440px] overflow-hidden">
        <div class="flex items-center gap-3 px-5 py-4 border-b border-dx-border">
          <div class="w-8 h-8 rounded-md flex items-center justify-center" :class="iconBgClass">
            <svg class="w-4 h-4" :class="iconColorClass" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10"/>
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4M12 16h.01"/>
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-dx-text-primary">{{ title }}</h3>
          </div>
        </div>
        <div class="px-5 py-4">
          <p class="text-sm text-dx-text-secondary leading-relaxed">{{ message }}</p>
        </div>
        <div class="flex items-center justify-end gap-2 px-5 py-4 border-t border-dx-border bg-dx-card-hover/30">
          <button
            class="h-9 px-4 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
            @click="$emit('cancel')"
          >
            {{ cancelText }}
          </button>
          <button
            class="h-9 px-5 rounded-md text-white text-sm font-medium transition-colors flex items-center gap-1.5"
            :class="confirmBtnClass"
            @click="$emit('confirm')"
          >
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  visible: boolean;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  type?: 'danger' | 'warning';
}>(), {
  confirmText: '确定',
  cancelText: '取消',
  type: 'danger',
});

defineEmits<{
  confirm: [];
  cancel: [];
}>();

const iconBgClass = computed(() => ({
  danger: 'bg-red-500/10',
  warning: 'bg-amber-500/10',
}[props.type]));

const iconColorClass = computed(() => ({
  danger: 'text-red-400',
  warning: 'text-amber-400',
}[props.type]));

const confirmBtnClass = computed(() => ({
  danger: 'bg-dx-danger hover:bg-red-600',
  warning: 'bg-dx-warning hover:bg-amber-600',
}[props.type]));
</script>
