<template>
  <div class="p-6 flex flex-col gap-4">
    <!-- Breadcrumb + Title -->
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
        </svg>
        <span>/</span><span class="text-dx-accent">任务列表</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">任务列表</h1>
    </div>

    <!-- Highlighted Task Banner -->
    <div v-if="store.highlightedTask" class="bg-dx-accent/10 border border-dx-accent/30 rounded-lg px-4 py-3 flex items-center gap-3">
      <svg class="w-5 h-5 text-dx-accent flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <span class="text-sm text-dx-text-primary">
        已构建任务：<span class="font-semibold text-dx-accent">{{ store.highlightedTask.name }}</span>
        <span class="text-dx-text-muted font-mono">({{ store.highlightedTask.id }})</span>，已加入任务列表。
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
              <th class="text-right py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap w-[280px]">操作</th>
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
              <td class="py-3 px-4 text-right">
                <div class="flex items-center justify-end gap-1.5">
                  <button
                    class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded text-xs font-medium text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
                    @click="handleEdit(task)"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                    编辑
                  </button>
                  <button
                    class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded text-xs font-medium text-dx-danger hover:bg-red-500/10 transition-colors"
                    @click="handleDelete(task)"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                    删除
                  </button>
                  <button
                    class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded text-xs font-medium text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
                    @click="handleRunOnce(task)"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                    手动执行一次
                  </button>
                  <button
                    class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded text-xs font-medium bg-dx-accent/10 text-dx-accent hover:bg-dx-accent/20 transition-colors"
                    @click="handleQueryLog(task)"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zM14 2v6h6M9 15h6"/></svg>
                    查询日志
                  </button>
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
  </div>

    <!-- Edit Task JSON Modal -->
    <Teleport to="body">
      <div
        v-if="editModalVisible"
        class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60"
        @click.self="closeEditModal"
      >
        <div class="bg-dx-card border border-dx-border rounded-xl shadow-2xl w-[800px] max-h-[90vh] overflow-hidden flex flex-col">
          <div class="flex items-center justify-between px-5 py-4 border-b border-dx-border flex-shrink-0">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-md bg-dx-accent/10 flex items-center justify-center">
                <svg class="w-4 h-4 text-dx-accent" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              </div>
              <div>
                <h3 class="text-sm font-semibold text-dx-text-primary">编辑任务配置</h3>
                <p class="text-xs text-dx-text-muted font-mono">{{ editingTask?.id }} — {{ editingTask?.name }}</p>
              </div>
            </div>
            <button class="w-7 h-7 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors" @click="closeEditModal">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto p-5">
            <p class="text-xs text-dx-text-muted mb-3">直接编辑下方 DataX JSON 配置，修改后点击「校验 JSON」确认格式，再点击「保存」。</p>
            <div class="relative rounded-lg border border-dx-border bg-dx-input focus-within:border-dx-accent transition-colors" style="height: 480px;">
              <!-- Line numbers gutter -->
              <div
                ref="gutterRef"
                class="absolute left-0 top-0 bottom-0 w-12 py-4 overflow-hidden select-none pointer-events-none text-right pr-3 font-mono text-xs leading-[23px] text-dx-text-muted/50 border-r border-dx-border"
              >
                <div v-for="n in lineCount" :key="n" class="h-[23px]">{{ n }}</div>
              </div>
              <!-- Editor -->
              <textarea
                ref="editorRef"
                v-model="editJson"
                class="w-full h-full pl-14 pr-4 py-4 bg-transparent text-sm text-dx-text-primary font-mono leading-[23px] resize-none focus:outline-none"
                spellcheck="false"
                @scroll="syncScroll"
              ></textarea>
            </div>

            <div
              v-if="jsonError"
              class="mt-3 flex items-start gap-2 px-3 py-2.5 rounded-md bg-red-500/10 border border-red-500/20"
            >
              <svg class="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" d="M12 8v4M12 16h.01"/></svg>
              <span class="text-xs text-red-400 font-mono">{{ jsonError }}</span>
            </div>

            <div
              v-if="jsonSuccess"
              class="mt-3 flex items-center gap-2 px-3 py-2.5 rounded-md bg-emerald-500/10 border border-emerald-500/20"
            >
              <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4"/></svg>
              <span class="text-xs text-emerald-400">JSON 格式校验通过</span>
            </div>
          </div>

          <div class="flex items-center justify-between px-5 py-4 border-t border-dx-border bg-dx-card-hover/30 flex-shrink-0">
            <span class="text-xs text-dx-text-muted">修改内容将直接更新任务配置</span>
            <div class="flex items-center gap-2">
              <button
                class="h-9 px-4 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
                @click="closeEditModal"
              >
                取消
              </button>
              <button
                class="h-9 px-4 rounded-md border border-dx-accent text-sm text-dx-accent hover:bg-dx-accent/10 transition-colors flex items-center gap-1.5"
                @click="handleValidateJson"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4"/></svg>
                校验 JSON
              </button>
              <button
                class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5"
                @click="handleSaveJson"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                保存
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Manual Run Modal -->
    <ManualRunModal
      :visible="runModalVisible"
      :task="runTask"
      @close="closeRunModal"
      @confirm="handleConfirmRun"
    />
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import type { TaskRecord } from '@/types';
import { useAppStore } from '@/stores/app';
import ManualRunModal from '@/components/common/ManualRunModal.vue';

const router = useRouter();
const store = useAppStore();

// --- Mock Data ---
const mockTasks = ref<TaskRecord[]>([
  { id: 'DX-20240512-001', name: '用户行为数据同步', user: '张工', group: '数据平台组', scheduled: true, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.102:8801', hostname: 'dx-worker-nj-02', spec: '8C / 16G', online: true }, { address: '10.23.45.103:8801', hostname: 'dx-worker-nj-03', spec: '16C / 32G', online: false }], status: 'success', dataSource: 'mysql_analytics', duration: '3m 42s', startTime: '2024-05-12 10:00' },
  { id: 'DX-20240512-002', name: '订单数据ETL', user: '李工', group: '电商组', scheduled: true, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }], status: 'running', dataSource: 'pg_orders', duration: '12m 18s', startTime: '2024-05-12 10:05' },
  { id: 'DX-20240512-003', name: '日志数据清洗', user: '王工', group: '数据平台组', scheduled: false, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.102:8801', hostname: 'dx-worker-nj-02', spec: '8C / 16G', online: true }, { address: '10.23.45.103:8801', hostname: 'dx-worker-nj-03', spec: '16C / 32G', online: false }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }, { address: '10.23.45.105:8801', hostname: 'dx-worker-nj-05', spec: '8C / 16G', online: true }], status: 'success', dataSource: 'hdfs_logs', duration: '8m 05s', startTime: '2024-05-12 09:45' },
  { id: 'DX-20240512-004', name: '商品信息全量同步', user: '赵工', group: '商品组', scheduled: true, nodes: [{ address: '10.23.45.102:8801', hostname: 'dx-worker-nj-02', spec: '8C / 16G', online: true }, { address: '10.23.45.103:8801', hostname: 'dx-worker-nj-03', spec: '16C / 32G', online: false }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }, { address: '10.23.45.105:8801', hostname: 'dx-worker-nj-05', spec: '8C / 16G', online: true }], status: 'failed', dataSource: 'mongo_products', duration: '2m 33s', startTime: '2024-05-12 09:30' },
  { id: 'DX-20240512-005', name: '用户画像更新', user: '刘工', group: '增长组', scheduled: false, nodes: [{ address: '10.23.45.105:8801', hostname: 'dx-worker-nj-05', spec: '8C / 16G', online: true }], status: 'pending', dataSource: 'hive_user_profile', duration: '—', startTime: '2024-05-12 11:00' },
  { id: 'DX-20240512-006', name: '库存数据增量同步', user: '陈工', group: '商品组', scheduled: true, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }], status: 'success', dataSource: 'mysql_inventory', duration: '1m 15s', startTime: '2024-05-12 10:15' },
  { id: 'DX-20240512-007', name: '广告投放数据汇总', user: '周工', group: '增长组', scheduled: true, nodes: [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }, { address: '10.23.45.102:8801', hostname: 'dx-worker-nj-02', spec: '8C / 16G', online: true }, { address: '10.23.45.104:8801', hostname: 'dx-worker-nj-04', spec: '16C / 32G', online: true }], status: 'running', dataSource: 'clickhouse_ads', duration: '5m 50s', startTime: '2024-05-12 10:10' },
]);

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
  let list = [...mockTasks.value];
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

function handleEdit(task: TaskRecord) {
  editingTask.value = task;
  editJson.value = JSON.stringify(buildTaskJson(task), null, 2);
  jsonError.value = '';
  jsonSuccess.value = false;
  editModalVisible.value = true;
}
function handleDelete(task: TaskRecord) { mockTasks.value = mockTasks.value.filter((t) => t.id !== task.id); }
function handleRunOnce(task: TaskRecord) {
  runTask.value = task;
  runModalVisible.value = true;
}
function handleQueryLog(task: TaskRecord) {
  store.openLogDialog({
    taskId: task.id,
    taskName: task.name,
    params: '--channel=3 --speed=5MB/s',
  });
}
function groupBadgeClass(g: string) {
  const m: Record<string, string> = { '数据平台组': 'bg-blue-500/10 text-blue-400', '电商组': 'bg-violet-500/10 text-violet-400', '商品组': 'bg-amber-500/10 text-amber-400', '增长组': 'bg-pink-500/10 text-pink-400' };
  return m[g] ?? 'bg-dx-input text-dx-text-secondary';
}

// --- Edit Modal ---
const editModalVisible = ref(false);
const editingTask = ref<TaskRecord | null>(null);
const editJson = ref('');
const jsonError = ref('');
const jsonSuccess = ref(false);
const editorRef = ref<HTMLTextAreaElement | null>(null);
const gutterRef = ref<HTMLDivElement | null>(null);

const lineCount = computed(() => {
  const lines = editJson.value.split('\n').length;
  return Math.max(lines, 1);
});

function syncScroll() {
  if (editorRef.value && gutterRef.value) {
    gutterRef.value.scrollTop = editorRef.value.scrollTop;
  }
}

function buildTaskJson(task: TaskRecord) {
  return {
    job: {
      setting: {
        speed: { channel: 3 },
      },
      content: [
        {
          reader: {
            name: 'mysqlreader',
            parameter: {
              username: 'datax_user',
              password: '***',
              column: ['id', 'user_id', 'action', 'category', 'created_at'],
              connection: [
                {
                  table: [task.name],
                  jdbcUrl: [`jdbc:mysql://10.23.45.10:3306/${task.dataSource}`],
                },
              ],
            },
          },
          writer: {
            name: 'clickhousewriter',
            parameter: {
              username: 'default',
              password: '***',
              column: ['id', 'user_id', 'action', 'category', 'created_at'],
              connection: [
                {
                  table: [`dw_${task.dataSource}`],
                  jdbcUrl: ['jdbc:clickhouse://10.23.45.20:8123/analytics'],
                },
              ],
            },
          },
        },
      ],
    },
  };
}

function handleValidateJson() {
  try {
    JSON.parse(editJson.value);
    jsonError.value = '';
    jsonSuccess.value = true;
    setTimeout(() => { jsonSuccess.value = false; }, 2000);
  } catch (e: unknown) {
    jsonError.value = (e as Error).message;
    jsonSuccess.value = false;
  }
}

function handleSaveJson() {
  try {
    JSON.parse(editJson.value);
    console.log('Save task:', editingTask.value?.id, JSON.parse(editJson.value));
    editModalVisible.value = false;
    editingTask.value = null;
    jsonError.value = '';
    jsonSuccess.value = false;
  } catch (e: unknown) {
    jsonError.value = `保存失败: ${(e as Error).message}`;
  }
}

function closeEditModal() {
  editModalVisible.value = false;
  editingTask.value = null;
  jsonError.value = '';
  jsonSuccess.value = false;
}

// --- Run Modal ---
const runModalVisible = ref(false);
const runTask = ref<TaskRecord | null>(null);

function handleConfirmRun(params: string, jvmArgs: string) {
  if (!runTask.value) return;
  console.log('Manual run:', runTask.value.id, { params, jvmArgs });
  store.setHighlightedTask({ id: runTask.value.id, name: runTask.value.name });
  runModalVisible.value = false;
  runTask.value = null;
  router.push('/schedule/run-detail');
}

function closeRunModal() {
  runModalVisible.value = false;
  runTask.value = null;
}
</script>
