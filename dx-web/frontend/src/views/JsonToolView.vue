<template>
  <div class="p-6 flex flex-col gap-4">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span>/</span><span class="text-dx-accent">JSON 格式化小工具</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">JSON 格式化小工具</h1>
    </div>

    <!-- Toolbar -->
    <div class="bg-dx-card border border-dx-border rounded-lg p-3 flex items-center gap-2 flex-wrap">
      <div class="flex items-center gap-0.5 bg-dx-input rounded-md p-0.5">
        <button class="px-3.5 py-1.5 rounded text-xs font-medium transition-colors" :class="mode === 'format' ? 'bg-dx-accent text-white' : 'text-dx-text-secondary hover:text-dx-text-primary'" @click="mode = 'format'; doFormat()">格式化</button>
        <button class="px-3.5 py-1.5 rounded text-xs font-medium transition-colors" :class="mode === 'minify' ? 'bg-dx-accent text-white' : 'text-dx-text-secondary hover:text-dx-text-primary'" @click="mode = 'minify'; doMinify()">压缩</button>
        <button class="px-3.5 py-1.5 rounded text-xs font-medium transition-colors" :class="mode === 'validate' ? 'bg-dx-accent text-white' : 'text-dx-text-secondary hover:text-dx-text-primary'" @click="mode = 'validate'; doValidate()">验证</button>
      </div>
      <div class="w-px h-6 bg-dx-border mx-1" />
      <select v-model="indent" class="h-8 px-2.5 rounded-md bg-dx-input border border-dx-border text-xs text-dx-text-secondary focus:outline-none focus:border-dx-accent" @change="doFormat">
        <option :value="2">缩进: 2 空格</option>
        <option :value="4">缩进: 4 空格</option>
        <option :value="1">缩进: 1 空格</option>
        <option value="tab">缩进: Tab</option>
      </select>
      <div class="w-px h-6 bg-dx-border mx-1" />
      <button class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded text-xs text-dx-text-secondary hover:text-dx-text-primary border border-dx-border transition-colors" @click="copyOutput"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg> 复制</button>
      <button class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded text-xs text-dx-text-secondary hover:text-dx-danger border border-dx-border transition-colors" @click="clearAll"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg> 清空</button>
      <div class="ml-auto flex items-center gap-4 text-xs text-dx-text-muted">
        <span v-if="output">大小: <span class="text-dx-text-primary font-mono">{{ byteSize }}</span></span>
        <span v-if="output">行数: <span class="text-dx-text-primary font-mono">{{ lineCount }}</span></span>
        <span v-if="validationResult" class="flex items-center gap-1.5" :class="validationResult.valid ? 'text-dx-success' : 'text-dx-danger'">
          <span class="w-2 h-2 rounded-full" :class="validationResult.valid ? 'bg-dx-success' : 'bg-dx-danger'" />
          {{ validationResult.valid ? '有效的 JSON' : `无效: ${validationResult.error}` }}
        </span>
      </div>
      <select class="h-8 px-2.5 rounded-md bg-dx-input border border-dx-border text-xs text-dx-text-secondary focus:outline-none focus:border-dx-accent" @change="loadSample(($event.target as HTMLSelectElement).value)">
        <option value="">示例数据...</option>
        <option value="user">示例: 用户数据</option>
        <option value="order">示例: 订单数据</option>
        <option value="config">示例: DataX 任务配置</option>
      </select>
    </div>

    <!-- Editor Panels -->
    <div class="grid grid-cols-2 gap-4" style="min-height: calc(100vh - 250px);">
      <div class="bg-dx-card border border-dx-border rounded-lg flex flex-col overflow-hidden">
        <div class="flex items-center justify-between px-4 py-2.5 border-b border-dx-border flex-shrink-0">
          <span class="text-xs font-medium text-dx-text-secondary">输入 JSON</span>
          <button class="text-xs text-dx-accent hover:text-cyan-300 transition-colors" @click="loadSample('config')">加载示例</button>
        </div>
        <textarea v-model="input" class="flex-1 bg-[#0c1222] border-0 p-4 font-mono text-[13px] leading-relaxed text-dx-text-secondary resize-none focus:outline-none" placeholder='粘贴或输入 JSON...&#10;&#10;{"name": "example", "value": 42}' spellcheck="false" @input="autoValidate" />
      </div>
      <div class="bg-dx-card border border-dx-border rounded-lg flex flex-col overflow-hidden">
        <div class="flex items-center justify-between px-4 py-2.5 border-b border-dx-border flex-shrink-0">
          <div class="flex items-center gap-2">
            <span class="text-xs font-medium text-dx-text-secondary">{{ outputLabel }}</span>
            <span v-if="mode" class="text-[10px] px-1.5 py-0.5 rounded" :class="mode === 'validate' && validationResult?.valid ? 'bg-emerald-500/10 text-emerald-400' : 'bg-dx-accent/10 text-dx-accent'">{{ modeLabel }}</span>
          </div>
          <span class="text-xs text-dx-text-muted">{{ outputLineCount }}</span>
        </div>
        <div class="flex-1 bg-[#0c1222] p-4 font-mono text-[13px] leading-relaxed overflow-auto">
          <pre v-if="output" class="whitespace-pre-wrap" v-html="highlightedOutput" />
          <p v-else class="text-dx-text-muted">等待输入...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const input = ref('');
const output = ref('');
const mode = ref<'format' | 'minify' | 'validate' | ''>('format');
const indent = ref<number | 'tab'>(2);
const validationResult = ref<{ valid: boolean; error?: string } | null>(null);

const samples: Record<string, string> = {
  user: '{\n  "users": [\n    {"id": 1, "name": "张三", "role": "admin"},\n    {"id": 2, "name": "李四", "role": "editor"}\n  ]\n}',
  order: '{\n  "orderId": "ORD-20240512-001",\n  "customer": "张三",\n  "total": 1280.50,\n  "items": [\n    {"sku": "SKU-001", "qty": 2, "price": 320.25},\n    {"sku": "SKU-002", "qty": 1, "price": 640.00}\n  ]\n}',
  config: '{\n  "reader": {\n    "name": "mysqlreader",\n    "parameter": {\n      "username": "root",\n      "password": "***",\n      "column": ["id","user_id","event_type"],\n      "connection": [{\n        "table": ["user_behavior_log"],\n        "jdbcUrl": ["jdbc:mysql://10.23.45.101:3306/analytics"]\n      }]\n    }\n  },\n  "writer": {\n    "name": "clickhousewriter",\n    "parameter": {\n      "username": "default",\n      "password": "***",\n      "column": ["id","user_id","event_type"],\n      "connection": [{\n        "table": ["dw_user_behavior_agg"],\n        "jdbcUrl": ["jdbc:clickhouse://10.23.45.201:8123/ads"]\n      }]\n    }\n  }\n}',
};

function tryParse(json: string): object | string {
  try { return JSON.parse(json); } catch { return json; }
}

function doFormat() {
  const parsed = tryParse(input.value);
  if (typeof parsed === 'string') { output.value = parsed; return; }
  const space = indent.value === 'tab' ? '\t' : indent.value;
  output.value = JSON.stringify(parsed, null, space);
  mode.value = 'format';
}

function doMinify() {
  const parsed = tryParse(input.value);
  if (typeof parsed === 'string') { output.value = parsed; return; }
  output.value = JSON.stringify(parsed);
  mode.value = 'minify';
}

function doValidate() {
  mode.value = 'validate';
  try {
    JSON.parse(input.value);
    validationResult.value = { valid: true };
    output.value = JSON.stringify(JSON.parse(input.value), null, indent.value === 'tab' ? '\t' : indent.value);
  } catch (e) {
    validationResult.value = { valid: false, error: (e as Error).message };
    output.value = '';
  }
}

function autoValidate() {
  if (mode.value === 'validate') doValidate();
  else doFormat();
}

function copyOutput() { navigator.clipboard.writeText(output.value); }
function clearAll() { input.value = ''; output.value = ''; validationResult.value = null; mode.value = 'format'; }
function loadSample(key: string) { if (samples[key]) { input.value = samples[key]; doFormat(); } }

const byteSize = computed(() => {
  const bytes = new Blob([output.value]).size;
  return bytes >= 1024 ? `${(bytes / 1024).toFixed(1)} KB` : `${bytes} B`;
});
const lineCount = computed(() => input.value ? input.value.split('\n').length : 0);
const outputLineCount = computed(() => output.value ? `${output.value.split('\n').length} 行` : '');
const outputLabel = computed(() => mode.value === 'format' ? '格式化输出' : mode.value === 'minify' ? '压缩输出' : mode.value === 'validate' ? '验证结果' : '输出');
const modeLabel = computed(() => mode.value === 'format' ? '格式化' : mode.value === 'minify' ? '压缩' : '验证');

const highlightedOutput = computed(() => {
  if (!output.value) return '';
  const escaped = output.value
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"([^"\\]*(\\.[^"\\]*)*)"/g, (_m, content) => `<span style="color:#67e8f9">"</span><span style="color:#a5d6a7">${content}</span><span style="color:#67e8f9">"</span>`)
    .replace(/\b(\d+\.?\d*)\b/g, '<span style="color:#f59e0b">$1</span>')
    .replace(/\b(true|false|null)\b/g, '<span style="color:#ef4444">$1</span>');
  return escaped;
});
</script>
