<template>
  <div class="mt-5 flex flex-col gap-2">
    <div class="flex items-center justify-between">
      <label class="text-xs font-medium text-dx-text-secondary">
        表字段信息 <span class="text-dx-text-muted">(选填 — 选择需要{{ side === 'reader' ? '同步' : '写入' }}的字段)</span>
      </label>
      <label class="flex items-center gap-2 text-xs text-dx-text-muted cursor-pointer select-none">
        <input type="checkbox" class="checkbox-custom" :checked="allSelected" @change="$emit('update:modelValue', allSelected ? [] : fieldNames)" />
        全选
      </label>
    </div>
    <div class="bg-dx-input border border-dx-border rounded-md p-3 grid grid-cols-4 gap-x-4 gap-y-2">
      <label
        v-for="f in fields"
        :key="f.name"
        class="flex items-center gap-2 text-xs text-dx-text-secondary cursor-pointer hover:text-dx-text-primary transition-colors"
      >
        <input
          type="checkbox"
          class="checkbox-custom"
          :checked="modelValue.includes(f.name)"
          @change="toggleField(f.name)"
        />
        {{ f.name }}
        <span class="text-dx-text-muted ml-auto">{{ f.type }}</span>
      </label>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface FieldDef {
  name: string;
  type: string;
}

const props = defineProps<{
  fields: FieldDef[];
  modelValue: string[];
  side?: string;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: string[]];
}>();

const fieldNames = computed(() => props.fields.map((f) => f.name));
const allSelected = computed(() => props.modelValue.length === props.fields.length);

function toggleField(name: string) {
  const arr = [...props.modelValue];
  const idx = arr.indexOf(name);
  if (idx > -1) arr.splice(idx, 1);
  else arr.push(name);
  emit('update:modelValue', arr);
}
</script>

<style scoped>
.checkbox-custom {
  appearance: none;
  width: 16px;
  height: 16px;
  border: 1.5px solid #64748b;
  border-radius: 3px;
  background: transparent;
  cursor: pointer;
  transition: 0.15s;
  position: relative;
  flex-shrink: 0;
}
.checkbox-custom:checked {
  background: #06b6d4;
  border-color: #06b6d4;
}
.checkbox-custom:checked::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 5px;
  height: 9px;
  border: solid #fff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
</style>
