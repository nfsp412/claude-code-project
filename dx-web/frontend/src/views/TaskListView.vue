<template>
  <div class="p-6 flex flex-col gap-4">
    <!-- Breadcrumb + Title -->
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
        </svg>
        <span>/</span><span class="text-dx-text-muted">任务管理</span><span>/</span><span class="text-dx-accent">任务明细列表</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">任务明细列表</h1>
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
        <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">关键字搜索</label>
        <input
          v-model="filters.keyword"
          type="text"
          placeholder="关键字/用户/组名"
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
        共 <span class="text-dx-text-primary font-semibold">{{ filteredTotal }}</span> 条任务
      </div>
    </div>

    <!-- Data Table -->
    <div class="bg-dx-card border border-dx-border rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-dx-input border-b border-dx-border">
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">
                <button class="flex items-center gap-1 select-none hover:text-dx-text-primary transition-colors" @click="toggleSort('id')">
                  任务ID
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7 11l5-5m0 0l5 5m-5-5v12"/>
                  </svg>
                </button>
              </th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">任务名称</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">所属用户</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">所属组</th>
              <th class="text-center py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap w-[100px]">定时调度</th>
              <th class="text-center py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap w-[100px]">注册节点</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">执行状态</th>
              <th class="text-right py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap w-[120px]">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="task in paginatedTasks"
              :key="task.id"
              class="border-b border-dx-border/50 hover:bg-dx-card-hover transition-colors"
            >
              <td class="py-3 px-4 font-mono text-xs text-dx-accent whitespace-nowrap">{{ task.id }}</td>
              <td class="py-3 px-4 text-dx-text-primary font-medium whitespace-nowrap">{{ task.name }}</td>
              <td class="py-3 px-4 text-dx-text-secondary text-xs whitespace-nowrap">{{ task.user }}</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium" :class="groupBadgeClass(task.group)">
                  {{ task.group }}
                </span>
              </td>
              <td class="py-3 px-4 text-center">
                <button
                  class="relative inline-flex items-center w-9 h-5 rounded-full transition-colors duration-200 focus:outline-none"
                  :class="task.scheduled ? 'bg-dx-accent' : 'bg-dx-border'"
                  role="switch"
                  :aria-checked="task.scheduled"
                  @click="toggleScheduled(task)"
                >
                  <span
                    class="inline-block w-3.5 h-3.5 rounded-full bg-white shadow-sm transform transition-transform duration-200"
                    :class="task.scheduled ? 'translate-x-[18px]' : 'translate-x-[3px]'"
                    :style="{ backgroundColor: task.scheduled ? '#fff' : '#64748B' }"
                  />
                </button>
              </td>
              <td class="py-3 px-4 text-center">
                <button
                  class="inline-flex items-center gap-1 px-2.5 py-1 rounded text-xs font-medium bg-dx-accent/10 text-dx-accent hover:bg-dx-accent/20 transition-colors"
                  @click="openNodeModal(task)"
                >
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2M11 17h2M11 7h2"/>
                  </svg>
                  {{ task.nodes.length }} 节点
                </button>
              </td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium" :class="statusBadgeClass(task.status)">
                  <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(task.status)" />
                  {{ statusLabel(task.status) }}
                </span>
              </td>
              <td class="py-3 px-4 text-right">
                <div class="relative inline-block" @click.stop>
                  <button
                    class="inline-flex items-center gap-1 px-2 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
                    @click="toggleActionMenu(task.id)"
                    @blur="closeActionMenu"
                  >
                    操作
                    <svg class="w-3 h-3 transition-transform" :class="{ 'rotate-180': openActionMenuId === task.id }" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </button>
                  <div
                    v-if="openActionMenuId === task.id"
                    class="absolute right-0 top-full mt-1 z-50 min-w-[140px] bg-dx-card border border-dx-border rounded-lg shadow-lg py-1"
                  >
                    <button class="w-full text-left px-3 py-2 text-xs text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors flex items-center gap-2" @click="handleEdit(task)">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                      编辑
                    </button>
                    <button class="w-full text-left px-3 py-2 text-xs text-dx-danger hover:bg-red-500/10 transition-colors flex items-center gap-2" @click="handleDelete(task)">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                      删除
                    </button>
                    <div class="border-t border-dx-border my-1" />
                    <button class="w-full text-left px-3 py-2 text-xs text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors flex items-center gap-2" @click="handleRunOnce(task)">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                      手动执行一次
                    </button>
                    <button class="w-full text-left px-3 py-2 text-xs text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors flex items-center gap-2" @click="handleQueryLog(task)">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6M9 15h6"/></svg>
                      查询执行日志
                    </button>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
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

    <!-- Node Info Modal -->
    <Teleport to="body">
      <div
        v-if="nodeModalVisible"
        class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60"
        @click.self="closeNodeModal"
      >
        <div class="bg-dx-card border border-dx-border rounded-xl shadow-2xl w-[480px] max-h-[70vh] overflow-hidden">
          <div class="flex items-center justify-between px-5 py-4 border-b border-dx-border">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-md bg-dx-accent/10 flex items-center justify-center">
                <svg class="w-4 h-4 text-dx-accent" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2M11 17h2M11 7h2"/></svg>
              </div>
              <div>
                <h3 class="text-sm font-semibold text-dx-text-primary">注册节点信息</h3>
                <p class="text-xs text-dx-text-muted">任务: {{ selectedTask?.id }} — {{ selectedTask?.name }}</p>
              </div>
            </div>
            <button class="w-7 h-7 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors" @click="closeNodeModal">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>
          <div class="p-5 overflow-y-auto max-h-[50vh]">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-dx-border">
                  <th class="text-left py-2 text-xs font-medium text-dx-text-muted uppercase">节点地址</th>
                  <th class="text-left py-2 text-xs font-medium text-dx-text-muted uppercase">主机名</th>
                  <th class="text-left py-2 text-xs font-medium text-dx-text-muted uppercase">规格</th>
                  <th class="text-right py-2 text-xs font-medium text-dx-text-muted uppercase">状态</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="node in selectedTask?.nodes" :key="node.address" class="border-b border-dx-border/50 last:border-b-0">
                  <td class="py-2.5 font-mono text-xs text-dx-text-primary">{{ node.address }}</td>
                  <td class="py-2.5 text-xs text-dx-text-secondary">{{ node.hostname }}</td>
                  <td class="py-2.5 text-xs text-dx-text-muted">{{ node.spec }}</td>
                  <td class="py-2.5 text-right">
                    <span class="text-xs px-2 py-0.5 rounded" :class="node.online ? 'text-emerald-400 bg-emerald-500/10' : 'text-amber-400 bg-amber-500/10'">
                      {{ node.online ? '在线' : '离线' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import type { TaskRecord } from '@/types';

// --- Mock Data ---
const mockTasks: TaskRecord[] = [
  { id: 'DX-20240512-001', name: '用户行为数据同步', user: '张工', group: '数据平台组', scheduled: true, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.102:8801', hostname: 'dx-worker-nj-02', spec: '8C / 16G', online: true }, { address: '10.23.45.103:8801', hostname: 'dx-worker-nj-03', spec: '16C / 32G', online: false }], status: 'success', dataSource: 'mysql_analytics', duration: '3m 42s', startTime: '2024-05-12 10:00' },
  { id: 'DX-20240512-002', name: '订单数据ETL', user: '李工', group: '电商组', scheduled: true, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }], status: 'running', dataSource: 'pg_orders', duration: '12m 18s', startTime: '2024-05-12 10:05' },
  { id: 'DX-20240512-003', name: '日志数据清洗', user: '王工', group: '数据平台组', scheduled: false, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.102:8801', hostname: 'dx-worker-nj-02', spec: '8C / 16G', online: true }, { address: '10.23.45.103:8801', hostname: 'dx-worker-nj-03', spec: '16C / 32G', online: false }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }, { address: '10.23.45.105:8801', hostname: 'dx-worker-nj-05', spec: '8C / 16G', online: true }], status: 'success', dataSource: 'hdfs_logs', duration: '8m 05s', startTime: '2024-05-12 09:45' },
  { id: 'DX-20240512-004', name: '商品信息全量同步', user: '赵工', group: '商品组', scheduled: true, nodes: [{ address: '10.23.45.102:8801', hostname: 'dx-worker-nj-02', spec: '8C / 16G', online: true }, { address: '10.23.45.103:8801', hostname: 'dx-worker-nj-03', spec: '16C / 32G', online: false }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }, { address: '10.23.45.105:8801', hostname: 'dx-worker-nj-05', spec: '8C / 16G', online: true }], status: 'failed', dataSource: 'mongo_products', duration: '2m 33s', startTime: '2024-05-12 09:30' },
  { id: 'DX-20240512-005', name: '用户画像更新', user: '刘工', group: '增长组', scheduled: false, nodes: [{ address: '10.23.45.105:8801', hostname: 'dx-worker-nj-05', spec: '8C / 16G', online: true }], status: 'pending', dataSource: 'hive_user_profile', duration: '—', startTime: '2024-05-12 11:00' },
  { id: 'DX-20240512-006', name: '库存数据增量同步', user: '陈工', group: '商品组', scheduled: true, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }], status: 'success', dataSource: 'mysql_inventory', duration: '1m 15s', startTime: '2024-05-12 10:15' },
  { id: 'DX-20240512-007', name: '广告投放数据汇总', user: '周工', group: '增长组', scheduled: true, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.102:8801', hostname: 'dx-worker-nj-02', spec: '8C / 16G', online: true }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }], status: 'running', dataSource: 'clickhouse_ads', duration: '5m 50s', startTime: '2024-05-12 10:10' },
];

// --- Filters ---
const filters = reactive({ taskId: '', taskName: '', keyword: '' });

// --- Sort ---
const sortField = ref<'id' | null>(null);
const sortDir = ref<'asc' | 'desc'>('asc');
function toggleSort(field: 'id') {
  if (sortField.value === field) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortField.value = field;
    sortDir.value = 'asc';
  }
}

// --- Filtered data ---
const filteredTasks = computed(() => {
  let list = [...mockTasks];
  if (filters.taskId) list = list.filter((t) => t.id.toLowerCase().includes(filters.taskId.toLowerCase()));
  if (filters.taskName) list = list.filter((t) => t.name.includes(filters.taskName));
  if (filters.keyword) {
    const kw = filters.keyword.toLowerCase();
    list = list.filter((t) => t.user.includes(kw) || t.group.includes(kw) || t.name.includes(kw));
  }
  if (sortField.value) {
    list.sort((a, b) => {
      const va = a[sortField.value!];
      const vb = b[sortField.value!];
      const cmp = String(va).localeCompare(String(vb));
      return sortDir.value === 'asc' ? cmp : -cmp;
    });
  }
  return list;
});
const filteredTotal = computed(() => filteredTasks.value.length);

// --- Pagination ---
const pageSize = 10;
const currentPage = ref(1);
const totalPages = computed(() => Math.max(1, Math.ceil(filteredTotal.value / pageSize)));
const pageStart = computed(() => Math.min((currentPage.value - 1) * pageSize + 1, filteredTotal.value));
const pageEnd = computed(() => Math.min(currentPage.value * pageSize, filteredTotal.value));

const paginatedTasks = computed(() =>
  filteredTasks.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
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
  filters.keyword = '';
  currentPage.value = 1;
}

// --- Action menu ---
const openActionMenuId = ref<string | null>(null);
function toggleActionMenu(id: string) {
  openActionMenuId.value = openActionMenuId.value === id ? null : id;
}
function closeActionMenu() {
  // Delayed to allow click on menu items
  setTimeout(() => { openActionMenuId.value = null; }, 150);
}
function handleEdit(task: TaskRecord) { openActionMenuId.value = null; console.log('Edit:', task.id); }
function handleDelete(task: TaskRecord) { openActionMenuId.value = null; console.log('Delete:', task.id); }
function handleRunOnce(task: TaskRecord) { openActionMenuId.value = null; console.log('Run once:', task.id); }
function handleQueryLog(task: TaskRecord) { openActionMenuId.value = null; console.log('Query log:', task.id); }

// --- Toggle scheduled ---
function toggleScheduled(task: TaskRecord) {
  task.scheduled = !task.scheduled;
}

// --- Node modal ---
const nodeModalVisible = ref(false);
const selectedTask = ref<TaskRecord | null>(null);
function openNodeModal(task: TaskRecord) {
  selectedTask.value = task;
  nodeModalVisible.value = true;
}
function closeNodeModal() {
  nodeModalVisible.value = false;
  selectedTask.value = null;
}

// --- Status helpers ---
function statusLabel(s: string) {
  const m: Record<string, string> = { running: '运行中', success: '成功', failed: '失败', pending: '等待中' };
  return m[s] ?? s;
}
function statusBadgeClass(s: string) {
  const m: Record<string, string> = { running: 'bg-cyan-500/10 text-cyan-400', success: 'bg-emerald-500/10 text-emerald-400', failed: 'bg-red-500/10 text-red-400', pending: 'bg-amber-500/10 text-amber-400' };
  return m[s] ?? '';
}
function statusDotClass(s: string) {
  const m: Record<string, string> = { running: 'bg-cyan-400 animate-pulse', success: 'bg-emerald-400', failed: 'bg-red-400', pending: 'bg-amber-400' };
  return m[s] ?? '';
}
function groupBadgeClass(g: string) {
  const m: Record<string, string> = { '数据平台组': 'bg-blue-500/10 text-blue-400', '电商组': 'bg-violet-500/10 text-violet-400', '商品组': 'bg-amber-500/10 text-amber-400', '增长组': 'bg-pink-500/10 text-pink-400' };
  return m[g] ?? 'bg-dx-input text-dx-text-secondary';
}
</script>
