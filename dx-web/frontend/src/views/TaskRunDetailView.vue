<template>
  <div class="p-6 flex flex-col gap-4">
    <!-- Breadcrumb + Title -->
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
        </svg>
        <span>/</span><span class="text-dx-accent">任务运行明细</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">任务运行明细</h1>
    </div>

    <!-- Highlighted Task Banner -->
    <div v-if="store.highlightedTask" class="bg-dx-accent/10 border border-dx-accent/30 rounded-lg px-4 py-3 flex items-center gap-3">
      <svg class="w-5 h-5 text-dx-accent flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <span class="text-sm text-dx-text-primary">
        已从任务列表执行任务：<span class="font-semibold text-dx-accent">{{ store.highlightedTask.name }}</span>
        <span class="text-dx-text-muted font-mono">({{ store.highlightedTask.id }})</span>，正在此页面显示运行明细。
      </span>
      <button class="ml-auto text-xs text-dx-text-muted hover:text-dx-text-primary transition-colors" @click="store.setHighlightedTask(null)">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    </div>

    <!-- Search / Filter Bar -->
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
        <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">执行结果</label>
        <select
          v-model="filters.status"
          class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary focus:outline-none focus:border-dx-accent"
        >
          <option value="">全部</option>
          <option value="success">成功</option>
          <option value="running">运行中</option>
          <option value="failed">失败</option>
        </select>
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
        共 <span class="text-dx-text-primary font-semibold">{{ filteredTotal }}</span> 条记录
      </div>
    </div>

    <!-- Data Table -->
    <div class="bg-dx-card border border-dx-border rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-dx-input border-b border-dx-border">
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务 ID</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务名称</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">数据源名称</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务开始时间</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务结束时间</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">运行时长</th>
              <th class="text-center py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap w-[90px]">执行结果</th>
              <th class="text-right py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap w-[220px]">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="run in paginatedRuns"
              :key="run.id"
              class="border-b border-dx-border/50 hover:bg-dx-card-hover transition-colors"
            >
              <td class="py-3 px-4 font-mono text-xs text-dx-accent whitespace-nowrap">{{ run.taskId }}</td>
              <td class="py-3 px-4 text-dx-text-primary font-medium whitespace-nowrap">{{ run.taskName }}</td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary whitespace-nowrap">{{ run.dataSource }}</td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary font-mono whitespace-nowrap">{{ run.startTime }}</td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary font-mono whitespace-nowrap">{{ run.endTime }}</td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary font-mono whitespace-nowrap">{{ run.duration }}</td>
              <td class="py-3 px-4 text-center">
                <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium" :class="statusBadgeClass(run.status)">
                  <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(run.status)" />
                  {{ statusLabel(run.status) }}
                </span>
              </td>
              <td class="py-3 px-4 text-right">
                <div class="flex items-center justify-end gap-1.5">
                  <button
                    class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded text-xs font-medium bg-dx-accent/10 text-dx-accent hover:bg-dx-accent/20 transition-colors"
                    @click="handleQueryLog(run)"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6M9 15h6"/>
                    </svg>
                    日志查询
                  </button>
                  <button
                    v-if="run.status === 'running'"
                    class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded text-xs font-medium bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-colors"
                    @click="handleTerminate(run)"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="1"/></svg>
                    终止任务
                  </button>
                  <button
                    v-if="run.status === 'failed'"
                    class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded text-xs font-medium bg-amber-500/10 text-amber-400 hover:bg-amber-500/20 transition-colors"
                    @click="handleRetry(run)"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                    重试任务
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
          <path stroke-linecap="round" stroke-linejoin="round" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
        </svg>
        <p class="text-sm text-dx-text-muted">暂无运行记录</p>
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

  <!-- Confirm Dialog -->
  <ConfirmDialog
    :visible="confirmVisible"
    :title="confirmTitle"
    :message="confirmMessage"
    :type="confirmType"
    @confirm="handleConfirmAction"
    @cancel="confirmVisible = false"
  />
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useAppStore } from '@/stores/app';
import ConfirmDialog from '@/components/common/ConfirmDialog.vue';

const store = useAppStore();

interface TaskRun {
  id: string;
  taskId: string;
  taskName: string;
  dataSource: string;
  startTime: string;
  endTime: string;
  duration: string;
  status: 'success' | 'running' | 'failed';
}

const mockRuns = ref<TaskRun[]>([
  { id: '1', taskId: 'DX-20240512-001', taskName: '用户行为数据同步', dataSource: 'mysql_analytics', startTime: '2024-05-12 10:00:00', endTime: '2024-05-12 10:03:42', duration: '3m 42s', status: 'success' },
  { id: '2', taskId: 'DX-20240512-002', taskName: '订单数据ETL', dataSource: 'pg_orders', startTime: '2024-05-12 10:05:00', endTime: '—', duration: '12m 18s', status: 'running' },
  { id: '3', taskId: 'DX-20240512-003', taskName: '日志数据清洗', dataSource: 'hdfs_logs', startTime: '2024-05-12 09:45:00', endTime: '2024-05-12 09:53:05', duration: '8m 05s', status: 'success' },
  { id: '4', taskId: 'DX-20240512-004', taskName: '商品信息全量同步', dataSource: 'mongo_products', startTime: '2024-05-12 09:30:00', endTime: '2024-05-12 09:32:33', duration: '2m 33s', status: 'failed' },
  { id: '5', taskId: 'DX-20240512-005', taskName: '用户画像更新', dataSource: 'hive_user_profile', startTime: '2024-05-12 11:00:00', endTime: '2024-05-12 11:08:15', duration: '8m 15s', status: 'success' },
  { id: '6', taskId: 'DX-20240512-006', taskName: '库存数据增量同步', dataSource: 'mysql_inventory', startTime: '2024-05-12 10:15:00', endTime: '—', duration: '1m 15s', status: 'running' },
  { id: '7', taskId: 'DX-20240512-007', taskName: '广告投放数据汇总', dataSource: 'clickhouse_ads', startTime: '2024-05-12 10:10:00', endTime: '2024-05-12 10:15:50', duration: '5m 50s', status: 'success' },
  { id: '8', taskId: 'DX-20240512-008', taskName: '财务数据对账', dataSource: 'mysql_finance', startTime: '2024-05-12 08:00:00', endTime: '2024-05-12 08:02:10', duration: '2m 10s', status: 'failed' },
]);

const filters = reactive({ taskId: '', taskName: '', status: '', keyword: '' });

const filteredRuns = computed(() => {
  let list = [...mockRuns.value];
  if (filters.taskId) list = list.filter((r) => r.taskId.toLowerCase().includes(filters.taskId.toLowerCase()));
  if (filters.taskName) list = list.filter((r) => r.taskName.includes(filters.taskName));
  if (filters.status) list = list.filter((r) => r.status === filters.status);
  if (filters.keyword) {
    const kw = filters.keyword.toLowerCase();
    list = list.filter((r) => r.taskId.includes(kw) || r.taskName.includes(kw));
  }
  return list;
});
const filteredTotal = computed(() => filteredRuns.value.length);

const pageSize = 10;
const currentPage = ref(1);
const totalPages = computed(() => Math.max(1, Math.ceil(filteredTotal.value / pageSize)));
const pageStart = computed(() => Math.min((currentPage.value - 1) * pageSize + 1, filteredTotal.value));
const pageEnd = computed(() => Math.min(currentPage.value * pageSize, filteredTotal.value));

const paginatedRuns = computed(() =>
  filteredRuns.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
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
function handleReset() {
  filters.taskId = '';
  filters.taskName = '';
  filters.status = '';
  filters.keyword = '';
  currentPage.value = 1;
}
function handleQueryLog(run: TaskRun) {
  store.openLogDialog({
    taskId: run.taskId,
    taskName: run.taskName,
    params: '--channel=3 --speed=5MB/s',
  });
}

// --- Confirm Dialog ---
const confirmVisible = ref(false);
const confirmTitle = ref('');
const confirmMessage = ref('');
const confirmType = ref<'danger' | 'warning'>('danger');
let pendingAction: (() => void) | null = null;

function handleTerminate(run: TaskRun) {
  confirmTitle.value = '终止任务';
  confirmMessage.value = `确定要终止运行中的任务「${run.taskName}」(${run.taskId}) 吗？终止后数据可能丢失。`;
  confirmType.value = 'danger';
  pendingAction = () => {
    console.log('Terminate confirmed:', run.taskId);
    mockRuns.value = mockRuns.value.filter((r) => r.id !== run.id);
  };
  confirmVisible.value = true;
}
function handleRetry(run: TaskRun) {
  confirmTitle.value = '重试任务';
  confirmMessage.value = `确定要重试失败的任务「${run.taskName}」(${run.taskId}) 吗？`;
  confirmType.value = 'warning';
  pendingAction = () => {
    console.log('Retry confirmed:', run.taskId);
    run.status = 'running';
  };
  confirmVisible.value = true;
}

function handleConfirmAction() {
  pendingAction?.();
  confirmVisible.value = false;
}

function statusLabel(s: string) {
  return { running: '运行中', success: '成功', failed: '失败' }[s] ?? s;
}
function statusBadgeClass(s: string) {
  return { running: 'bg-cyan-500/10 text-cyan-400', success: 'bg-emerald-500/10 text-emerald-400', failed: 'bg-red-500/10 text-red-400' }[s] ?? '';
}
function statusDotClass(s: string) {
  return { running: 'bg-cyan-400 animate-pulse', success: 'bg-emerald-400', failed: 'bg-red-400' }[s] ?? '';
}
</script>
