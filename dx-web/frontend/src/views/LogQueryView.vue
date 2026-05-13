<template>
  <div class="p-6 flex flex-col gap-4">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span>/</span><span class="text-dx-accent">日志查询</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">日志查询</h1>
    </div>

    <!-- Search & Filter -->
    <div class="bg-dx-card border border-dx-border rounded-lg p-4">
      <div class="flex flex-wrap items-end gap-3 mb-3">
        <div class="flex flex-col gap-1.5"><label class="text-2xs font-medium text-dx-text-muted uppercase">任务 ID</label><input v-model="filters.taskId" type="text" placeholder="DX-20240512-001" class="w-44 h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"></div>
        <div class="flex flex-col gap-1.5"><label class="text-2xs font-medium text-dx-text-muted uppercase">关键字</label><input v-model="filters.keyword" type="text" placeholder="搜索日志内容..." class="w-48 h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"></div>
        <div class="flex flex-col gap-1.5"><label class="text-2xs font-medium text-dx-text-muted uppercase">时间范围</label><select v-model="filters.timeRange" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary focus:outline-none focus:border-dx-accent"><option>最近 1 小时</option><option>最近 6 小时</option><option>最近 24 小时</option><option>自定义...</option></select></div>
        <div class="flex flex-col gap-1.5"><label class="text-2xs font-medium text-dx-text-muted uppercase">日志级别</label><select v-model="filters.level" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary focus:outline-none focus:border-dx-accent"><option value="">全部级别</option><option>ERROR</option><option>WARN</option><option>INFO</option><option>DEBUG</option></select></div>
        <button class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5" @click="doSearch"><svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" d="M21 21l-4.3-4.3"/></svg>查询</button>
        <button class="h-9 px-4 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover transition-colors" @click="resetFilters">重置</button>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-2xs text-dx-text-muted">快速筛选:</span>
        <button v-for="lvl in quickLevels" :key="lvl" class="text-xs px-2.5 py-1 rounded-full transition-colors" :class="lvl === 'ERROR' ? 'bg-red-500/10 text-red-400 hover:bg-red-500/20' : lvl === 'WARN' ? 'bg-amber-500/10 text-amber-400 hover:bg-amber-500/20' : lvl === 'INFO' ? 'bg-cyan-500/10 text-cyan-400 hover:bg-cyan-500/20' : 'bg-dx-input text-dx-text-muted hover:bg-dx-card-hover'" @click="filters.level = filters.level === lvl ? '' : lvl; doSearch()">{{ lvl }}</button>
        <span class="text-xs text-dx-text-muted ml-auto">共 <span class="text-dx-text-primary font-semibold">{{ filteredTotal.toLocaleString() }}</span> 条日志</span>
      </div>
    </div>

    <!-- Log Stream -->
    <div class="bg-dx-card border border-dx-border rounded-lg overflow-hidden">
      <div class="flex items-center justify-between px-4 py-2.5 border-b border-dx-border bg-dx-input/50">
        <div class="flex items-center gap-4 text-xs"><button class="font-medium" :class="liveMode ? 'text-dx-accent' : 'text-dx-text-muted hover:text-dx-text-secondary'" @click="liveMode = !liveMode">{{ liveMode ? '● 实时跟踪' : '实时跟踪' }}</button><button class="text-dx-text-muted hover:text-dx-text-secondary" @click="liveMode = false">暂停</button></div>
        <div class="flex items-center gap-3 text-xs"><button class="text-dx-text-muted hover:text-dx-text-secondary">自动滚动</button><button class="text-dx-text-muted hover:text-dx-text-secondary">导出</button></div>
      </div>
      <div class="font-mono text-xs leading-relaxed overflow-x-auto" style="max-height: 600px; overflow-y: auto;" ref="logContainer">
        <div v-for="(log, i) in filteredLogs" :key="i" class="flex border-b border-dx-border/30 hover:bg-dx-card-hover/50 transition-colors">
          <span class="w-44 flex-shrink-0 px-4 py-2 text-dx-text-muted border-r border-dx-border/30">{{ log.time }}</span>
          <span class="w-16 flex-shrink-0 px-2 py-2 font-semibold" :class="levelStyle(log.level)">{{ log.level }}</span>
          <span class="w-32 flex-shrink-0 px-2 py-2 text-dx-text-muted">{{ log.taskId }}</span>
          <span class="px-2 py-2" :class="log.level === 'ERROR' ? 'text-dx-text-secondary bg-red-500/5' : log.level === 'WARN' ? 'text-dx-text-secondary bg-amber-500/5' : log.level === 'INFO' ? 'text-dx-text-secondary bg-cyan-500/5' : 'text-dx-text-muted'" v-html="highlightMsg(log.msg)" />
        </div>
      </div>
      <div class="flex items-center justify-between px-4 py-3 border-t border-dx-border bg-dx-card-hover/30">
        <span class="text-xs text-dx-text-muted">显示第 1-{{ filteredLogs.length }} 条 (共 {{ filteredTotal.toLocaleString() }} 条)</span>
        <div class="flex items-center gap-1"><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">‹</button><button class="w-8 h-8 rounded-md text-xs font-medium bg-dx-accent text-white">1</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">2</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">3</button><span class="text-xs text-dx-text-muted">···</span><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">1606</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">›</button></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';

const liveMode = ref(true);
const quickLevels = ['ERROR', 'WARN', 'INFO', 'DEBUG'];

const filters = reactive({ taskId: '', keyword: '', timeRange: '最近 1 小时', level: '' });

interface LogEntry { time: string; level: string; taskId: string; msg: string; }
const allLogs: LogEntry[] = [
  { time: '05-12 18:45:22.341', level: 'ERROR', taskId: 'DX-20240512-004', msg: 'Connection refused to 10.23.45.104:3306 — retry 3/3 exhausted' },
  { time: '05-12 18:45:22.180', level: 'WARN', taskId: 'DX-20240512-004', msg: 'Slow query detected: SELECT * FROM product_info WHERE... took 12.5s' },
  { time: '05-12 18:45:21.905', level: 'INFO', taskId: 'DX-20240512-003', msg: 'Reader task completed. Fetched 2,458,391 rows in 8m 05s' },
  { time: '05-12 18:45:21.672', level: 'DEBUG', taskId: 'DX-20240512-003', msg: '[Channel-3] Batch #847 committed, offset=12584000, latency=23ms' },
  { time: '05-12 18:45:19.004', level: 'INFO', taskId: 'DX-20240512-002', msg: 'Task started. Reader: mysqlreader → Writer: clickhousewriter. Channel: 3' },
  { time: '05-12 18:45:18.556', level: 'INFO', taskId: 'DX-20240512-001', msg: 'Task completed successfully. Total: 3,827,120 rows, Duration: 3m 42s, Speed: 17.2 MB/s' },
  { time: '05-12 18:45:17.231', level: 'WARN', taskId: 'DX-20240512-007', msg: 'Memory usage approaching limit. Current heap: 8.2G / 10G' },
  { time: '05-12 18:45:17.089', level: 'INFO', taskId: 'DX-20240512-007', msg: 'Writer initializing. Target table: dw_user_behavior_agg @ ClickHouse' },
];

const filteredLogs = computed(() => {
  let logs = [...allLogs];
  if (filters.taskId) logs = logs.filter((l) => l.taskId.includes(filters.taskId));
  if (filters.keyword) logs = logs.filter((l) => l.msg.includes(filters.keyword));
  if (filters.level) logs = logs.filter((l) => l.level === filters.level);
  return logs;
});
const filteredTotal = computed(() => allLogs.length);

function doSearch() { /* already reactive */ }
function resetFilters() { filters.taskId = ''; filters.keyword = ''; filters.level = ''; filters.timeRange = '最近 1 小时'; }

function levelStyle(level: string) {
  const m: Record<string, string> = { ERROR: 'text-red-400', WARN: 'text-amber-400', INFO: 'text-cyan-400', DEBUG: 'text-dx-text-muted' };
  return m[level] ?? '';
}

function highlightMsg(msg: string) {
  return msg
    .replace(/(\d+\.\d+\.\d+\.\d+:\d+)/g, '<span class="text-dx-accent">$1</span>')
    .replace(/(\d[\d,.]*(?:\s*(?:MB\/s|rows|s|ms|M|G)))/g, '<span class="text-dx-warning">$1</span>')
    .replace(/(completed successfully|success|Fetched)/gi, '<span class="text-dx-success">$1</span>')
    .replace(/(failed|refused|exhausted|error)/gi, '<span class="text-dx-danger">$1</span>');
}
</script>
