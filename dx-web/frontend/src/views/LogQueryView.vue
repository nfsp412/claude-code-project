<template>
  <div class="p-6 flex flex-col gap-4">
    <!-- Breadcrumb + Title -->
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
        </svg>
        <span>/</span><span class="text-dx-accent">日志查询</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">日志查询</h1>
    </div>

    <!-- Search Bar -->
    <div class="bg-dx-card border border-dx-border rounded-lg p-4 flex flex-wrap items-end gap-3">
      <div class="flex flex-col gap-1.5">
        <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">任务 ID</label>
        <input
          v-model="filters.taskId"
          type="text"
          placeholder="例如: DX-20240512"
          class="w-44 h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"
          @keyup.enter="handleSearch"
        />
      </div>
      <div class="flex flex-col gap-1.5">
        <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">任务名称</label>
        <input
          v-model="filters.taskName"
          type="text"
          placeholder="输入任务名称"
          class="w-48 h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"
          @keyup.enter="handleSearch"
        />
      </div>
      <div class="flex flex-col gap-1.5">
        <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">日志 ID</label>
        <input
          v-model="filters.logId"
          type="text"
          placeholder="例如: LOG-20240512"
          class="w-44 h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"
          @keyup.enter="handleSearch"
        />
      </div>
      <div class="flex flex-col gap-1.5">
        <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">关键字搜索</label>
        <input
          v-model="filters.keyword"
          type="text"
          placeholder="关键字搜索"
          class="w-52 h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"
          @keyup.enter="handleSearch"
        />
      </div>
      <button
        class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5"
        @click="handleSearch"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8"/><path stroke-linecap="round" d="M21 21l-4.3-4.3"/>
        </svg>
        搜索
      </button>
      <button
        class="h-9 px-4 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
        @click="handleReset"
      >
        重置
      </button>
      <div class="ml-auto text-xs text-dx-text-muted">
        共 <span class="text-dx-text-primary font-semibold">{{ filteredTotal }}</span> 条日志记录
      </div>
    </div>

    <!-- Data Table -->
    <div class="bg-dx-card border border-dx-border rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-dx-input border-b border-dx-border">
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务 ID</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">日志 ID</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务名称</th>
              <th class="text-center py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap w-[90px]">执行结果</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务执行传参</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务开始时间</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务结束时间</th>
              <th class="text-right py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap w-[120px]">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="log in paginatedLogs"
              :key="log.logId"
              class="border-b border-dx-border/50 hover:bg-dx-card-hover transition-colors"
            >
              <td class="py-3 px-4 font-mono text-xs text-dx-accent whitespace-nowrap">{{ log.taskId }}</td>
              <td class="py-3 px-4 font-mono text-xs text-dx-text-secondary whitespace-nowrap">{{ log.logId }}</td>
              <td class="py-3 px-4 text-dx-text-primary font-medium whitespace-nowrap">{{ log.taskName }}</td>
              <td class="py-3 px-4 text-center">
                <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium" :class="statusBadgeClass(log.result)">
                  <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(log.result)" />
                  {{ statusLabel(log.result) }}
                </span>
              </td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary max-w-[200px]">
                <span class="font-mono text-2xs text-dx-text-muted truncate block" :title="log.params">{{ log.params }}</span>
              </td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary font-mono whitespace-nowrap">{{ log.startTime }}</td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary font-mono whitespace-nowrap">{{ log.endTime }}</td>
              <td class="py-3 px-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button
                    class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded text-xs font-medium bg-dx-accent/10 text-dx-accent hover:bg-dx-accent/20 transition-colors"
                    @click="handleViewLog(log)"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6M9 15h6"/>
                    </svg>
                    日志查询
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty state -->
      <div v-if="filteredTotal === 0" class="py-16 text-center">
        <svg class="w-12 h-12 mx-auto text-dx-text-muted/30 mb-3" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6"/>
        </svg>
        <p class="text-sm text-dx-text-muted">暂无日志记录</p>
      </div>

      <!-- Pagination -->
      <div class="flex items-center justify-between px-4 py-3 border-t border-dx-border bg-dx-card-hover/30">
        <span class="text-xs text-dx-text-muted">显示第 {{ pageStart }}-{{ pageEnd }} 条，共 {{ filteredTotal }} 条</span>
        <div class="flex items-center gap-1">
          <button
            class="inline-flex items-center justify-center w-8 h-8 rounded-md text-xs transition-colors"
            :class="currentPage === 1 ? 'text-dx-text-muted/40 cursor-not-allowed' : 'text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary'"
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
          </button>
          <button
            v-for="p in displayPages"
            :key="p"
            class="inline-flex items-center justify-center w-8 h-8 rounded-md text-xs font-medium transition-colors"
            :class="p === currentPage ? 'bg-dx-accent text-white' : 'text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary'"
            @click="goToPage(p)"
          >
            {{ p }}
          </button>
          <button
            class="inline-flex items-center justify-center w-8 h-8 rounded-md text-xs transition-colors"
            :class="currentPage === totalPages ? 'text-dx-text-muted/40 cursor-not-allowed' : 'text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary'"
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useAppStore } from '@/stores/app';

const store = useAppStore();

interface LogRecord {
  logId: string;
  taskId: string;
  taskName: string;
  result: 'success' | 'running' | 'failed';
  params: string;
  startTime: string;
  endTime: string;
}

const mockLogs: LogRecord[] = [
  { logId: 'LOG-20240512-001', taskId: 'DX-20240512-001', taskName: '用户行为数据同步', result: 'success', params: '--channel=3 --speed=5MB/s --where="dt=20240512"', startTime: '2024-05-12 10:00:00', endTime: '2024-05-12 10:03:42' },
  { logId: 'LOG-20240512-002', taskId: 'DX-20240512-002', taskName: '订单数据ETL', result: 'running', params: '--channel=2 --speed=10MB/s --splitPK=order_id', startTime: '2024-05-12 10:05:00', endTime: '—' },
  { logId: 'LOG-20240512-003', taskId: 'DX-20240512-003', taskName: '日志数据清洗', result: 'success', params: '--channel=3 --memory=8G --where="dt>=20240501"', startTime: '2024-05-12 09:45:00', endTime: '2024-05-12 09:53:05' },
  { logId: 'LOG-20240512-004', taskId: 'DX-20240512-004', taskName: '商品信息全量同步', result: 'failed', params: '--channel=2 --speed=8MB/s --queryTimeout=300', startTime: '2024-05-12 09:30:00', endTime: '2024-05-12 09:32:33' },
  { logId: 'LOG-20240512-005', taskId: 'DX-20240512-005', taskName: '用户画像更新', result: 'success', params: '--channel=1 --memory=4G --batchSize=2000', startTime: '2024-05-12 11:00:00', endTime: '2024-05-12 11:08:15' },
  { logId: 'LOG-20240512-006', taskId: 'DX-20240512-006', taskName: '库存数据增量同步', result: 'running', params: '--channel=2 --speed=5MB/s --where="updated_at>now()-3600"', startTime: '2024-05-12 10:15:00', endTime: '—' },
  { logId: 'LOG-20240512-007', taskId: 'DX-20240512-007', taskName: '广告投放数据汇总', result: 'success', params: '--channel=3 --memory=10G --preSql="ALTER TABLE ... DELETE"', startTime: '2024-05-12 10:10:00', endTime: '2024-05-12 10:15:50' },
  { logId: 'LOG-20240512-008', taskId: 'DX-20240512-008', taskName: '财务数据对账', result: 'failed', params: '--channel=2 --speed=3MB/s --retryCount=3', startTime: '2024-05-12 08:00:00', endTime: '2024-05-12 08:02:10' },
];

const filters = reactive({ taskId: '', taskName: '', logId: '', keyword: '' });

const filteredLogs = computed(() => {
  let list = [...mockLogs];
  if (filters.taskId) list = list.filter((l) => l.taskId.toLowerCase().includes(filters.taskId.toLowerCase()));
  if (filters.taskName) list = list.filter((l) => l.taskName.includes(filters.taskName));
  if (filters.logId) list = list.filter((l) => l.logId.toLowerCase().includes(filters.logId.toLowerCase()));
  if (filters.keyword) {
    const kw = filters.keyword.toLowerCase();
    list = list.filter((l) => l.taskId.includes(kw) || l.taskName.includes(kw) || l.params.includes(kw));
  }
  return list;
});
const filteredTotal = computed(() => filteredLogs.value.length);

const pageSize = 10;
const currentPage = ref(1);
const totalPages = computed(() => Math.max(1, Math.ceil(filteredTotal.value / pageSize)));
const pageStart = computed(() => Math.min((currentPage.value - 1) * pageSize + 1, filteredTotal.value));
const pageEnd = computed(() => Math.min(currentPage.value * pageSize, filteredTotal.value));

const paginatedLogs = computed(() =>
  filteredLogs.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
);

const displayPages = computed(() => {
  const pages: number[] = [];
  const tp = totalPages.value;
  const cp = currentPage.value;
  let start = Math.max(1, cp - 2);
  let end = Math.min(tp, cp + 2);
  if (end - start < 4) {
    if (start === 1) end = Math.min(tp, 5);
    else start = Math.max(1, tp - 4);
  }
  for (let i = start; i <= end; i++) pages.push(i);
  return pages;
});

function goToPage(p: number) {
  if (p >= 1 && p <= totalPages.value) currentPage.value = p;
}
function handleSearch() { currentPage.value = 1; }
function handleReset() { filters.taskId = ''; filters.taskName = ''; filters.logId = ''; filters.keyword = ''; currentPage.value = 1; }

function statusLabel(s: string) {
  return { running: '运行中', success: '成功', failed: '失败' }[s] ?? s;
}
function statusBadgeClass(s: string) {
  return { running: 'bg-cyan-500/10 text-cyan-400', success: 'bg-emerald-500/10 text-emerald-400', failed: 'bg-red-500/10 text-red-400' }[s] ?? '';
}
function statusDotClass(s: string) {
  return { running: 'bg-cyan-400 animate-pulse', success: 'bg-emerald-400', failed: 'bg-red-400' }[s] ?? '';
}

function handleViewLog(log: LogRecord) {
  store.openLogDialog({
    taskId: log.taskId,
    taskName: log.taskName,
    params: log.params,
  });
}
</script>
