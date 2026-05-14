<template>
  <div class="p-6 flex flex-col gap-4">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span>/</span><span class="text-dx-accent">任务调度</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">任务调度</h1>
    </div>

    <!-- Overview Cards -->
    <div class="grid grid-cols-4 gap-4">
      <div v-for="card in overviewCards" :key="card.label" class="bg-dx-card border border-dx-border rounded-lg p-4">
        <span class="text-xs text-dx-text-muted">{{ card.label }}</span>
        <div class="text-2xl font-bold mt-1" :class="card.color">{{ card.value }}</div>
        <span class="text-xs text-dx-text-muted" v-if="card.sub">{{ card.sub }}</span>
      </div>
    </div>

    <!-- Toolbar -->
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
          placeholder="关键字搜索"
          class="w-52 h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"
          @keyup.enter="handleSearch"
        />
      </div>
      <button
        class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5"
        @click="handleSearch"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" d="M21 21l-4.3-4.3"/></svg>
        搜索
      </button>
      <button
        class="h-9 px-4 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
        @click="handleReset"
      >
        重置
      </button>
      <button class="h-9 px-4 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5 ml-auto" @click="openDrawer()"><svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M12 5v14M5 12h14"/></svg> 新建调度</button>
    </div>

    <!-- Schedule Table -->
    <div class="bg-dx-card border border-dx-border rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm"><thead><tr class="bg-dx-input border-b border-dx-border"><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase whitespace-nowrap">任务 ID</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">任务名称</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">Cron 表达式</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">下次执行</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">上次执行</th><th class="text-center py-3 px-4 text-xs font-medium text-dx-text-muted uppercase w-[80px]">启用</th><th class="text-right py-3 px-4 text-xs font-medium text-dx-text-muted uppercase w-[200px]">操作</th></tr></thead>
          <tbody>
            <tr v-for="s in filteredSchedules" :key="s.id" class="border-b border-dx-border/50 hover:bg-dx-card-hover transition-colors last:border-b-0">
              <td class="py-3 px-4 font-mono text-xs text-dx-accent whitespace-nowrap">{{ s.id }}</td>
              <td class="py-3 px-4"><span class="text-dx-text-primary font-medium">{{ s.taskName }}</span></td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-1 flex-wrap">
                  <span v-for="(part, pi) in cronParts(s.cron)" :key="pi" class="inline-block px-1.5 py-0.5 rounded text-[11px] font-mono border" :class="cronPartColor(pi)" :style="{ background: cronPartBg(pi) }">{{ part }}</span>
                </div>
                <span class="text-[10px] text-dx-text-muted mt-1 block">{{ cronDescription(s.cron) }}</span>
              </td>
              <td class="py-3 px-4 text-xs"><span class="text-dx-accent">{{ s.nextRun }}</span><br><span class="text-[10px] text-dx-text-muted">{{ s.nextRunRelative }}</span></td>
              <td class="py-3 px-4 text-xs"><span class="text-dx-text-secondary">{{ s.lastRun }}</span><br><span class="text-[10px]" :class="s.lastStatus === '成功' ? 'text-emerald-400' : 'text-dx-danger'">{{ s.lastStatus }}</span></td>
              <td class="py-3 px-4 text-center">
                <button class="relative inline-flex items-center w-9 h-5 rounded-full transition-colors duration-200 focus:outline-none" :class="s.enabled ? 'bg-dx-accent' : 'bg-dx-border'" role="switch" @click="s.enabled = !s.enabled">
                  <span class="inline-block w-3.5 h-3.5 rounded-full shadow-sm transform transition-transform duration-200" :class="s.enabled ? 'translate-x-[18px] bg-white' : 'translate-x-[3px]'" :style="{ backgroundColor: s.enabled ? '#fff' : '#64748B' }" />
                </button>
              </td>
              <td class="py-3 px-4 text-right"><div class="flex items-center justify-end gap-1"><button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-accent transition-colors" @click="handleEdit(s)">编辑</button><button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-accent transition-colors" @click="handleRunNow(s)">立即执行</button><button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-dx-accent/10 hover:text-dx-accent transition-colors" @click="handleQueryLog(s)">查询日志</button><button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-red-500/10 hover:text-dx-danger transition-colors" @click="handleDelete(s)">删除</button></div></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="flex items-center justify-between px-4 py-3 border-t border-dx-border bg-dx-card-hover/30"><span class="text-xs text-dx-text-muted">共 {{ schedules.length }} 条调度</span><div class="flex items-center gap-1"><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">‹</button><button class="w-8 h-8 rounded-md text-xs font-medium bg-dx-accent text-white">1</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">2</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">3</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">›</button></div></div>
    </div>
  </div>

  <!-- New Schedule Drawer -->
  <Teleport to="body">
    <Transition name="drawer">
      <div v-if="drawerVisible" class="fixed inset-0 z-[100]">
        <div class="absolute inset-0 bg-black/50" @click="closeDrawer" />
        <div class="drawer-panel absolute top-0 right-0 h-full bg-dx-card border-l border-dx-border shadow-2xl flex flex-col" style="width: 520px;">
          <!-- Header -->
          <div class="flex-shrink-0 flex items-center justify-between px-6 py-4 border-b border-dx-border">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-dx-accent/10 flex items-center justify-center">
                <svg class="w-4 h-4 text-dx-accent" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zM12 6v6l4 2"/></svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-dx-text-primary">{{ isEditMode ? '编辑调度' : '新建调度' }}</h2>
                <p class="text-xs text-dx-text-muted">{{ isEditMode ? '修改任务的 Cron 调度规则' : '配置任务的 Cron 调度规则' }}</p>
              </div>
            </div>
            <button class="w-7 h-7 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors" @click="closeDrawer">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <!-- Body -->
          <div class="flex-1 overflow-y-auto px-6 py-5" style="min-height: 0;">
            <div class="flex flex-col gap-4">
              <!-- 任务 ID -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-medium text-dx-text-secondary">任务 ID <span class="text-red-400">*</span></label>
                <select v-model="form.taskId" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono focus:outline-none focus:border-dx-accent transition-colors">
                  <option value="" disabled>请选择任务</option>
                  <option v-for="t in availableTasks" :key="t.id" :value="t.id">{{ t.id }} — {{ t.name }}</option>
                </select>
              </div>

              <!-- 任务名称 (auto-filled) -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-medium text-dx-text-secondary">任务名称</label>
                <input :value="selectedTaskName" type="text" readonly class="h-9 px-3 rounded-md bg-dx-input/50 border border-dx-border text-sm text-dx-text-muted cursor-not-allowed" />
              </div>

              <!-- Cron 表达式 -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-medium text-dx-text-secondary">Cron 表达式 <span class="text-red-400">*</span></label>

                <!-- Mode toggle -->
                <div class="flex bg-dx-input rounded-md p-0.5 w-fit">
                  <button
                    class="px-3 py-1 rounded text-xs font-medium transition-colors"
                    :class="cronMode === 'preset' ? 'bg-dx-accent text-white' : 'text-dx-text-secondary hover:text-dx-text-primary'"
                    @click="cronMode = 'preset'"
                  >快捷预设</button>
                  <button
                    class="px-3 py-1 rounded text-xs font-medium transition-colors"
                    :class="cronMode === 'custom' ? 'bg-dx-accent text-white' : 'text-dx-text-secondary hover:text-dx-text-primary'"
                    @click="cronMode = 'custom'"
                  >自定义</button>
                </div>

                <!-- Preset mode: clickable preset cards -->
                <div v-if="cronMode === 'preset'" class="grid grid-cols-2 gap-2">
                  <button
                    v-for="p in cronPresets"
                    :key="p.cron"
                    class="text-left px-3 py-2.5 rounded-md border transition-all duration-150"
                    :class="form.cron === p.cron
                      ? 'border-dx-accent bg-dx-accent/10'
                      : 'border-dx-border bg-dx-input hover:border-dx-text-muted'"
                    @click="selectPreset(p)"
                  >
                    <span class="block text-xs font-medium text-dx-text-primary">{{ p.label }}</span>
                    <span class="block text-[10px] text-dx-text-muted font-mono mt-0.5">{{ p.cron }}</span>
                  </button>
                </div>

                <!-- Custom mode: raw text input -->
                <div v-else class="flex flex-col gap-1">
                  <input
                    v-model="form.cron"
                    type="text"
                    placeholder="例如: 0 2 * * *"
                    class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"
                  />
                </div>

                <!-- Live preview -->
                <span v-if="form.cron" class="text-2xs text-dx-text-muted">{{ cronDescription(form.cron) }}</span>
              </div>

              <!-- Divider -->
              <div class="border-t border-dx-border my-1" />

              <!-- 启用开关 -->
              <div class="flex items-center justify-between">
                <div class="flex flex-col gap-0.5">
                  <span class="text-xs font-medium text-dx-text-secondary">启用调度</span>
                  <span class="text-2xs text-dx-text-muted">创建后立即开始按规则执行</span>
                </div>
                <button
                  class="relative inline-flex items-center w-9 h-5 rounded-full transition-colors duration-200 focus:outline-none"
                  :class="form.enabled ? 'bg-dx-accent' : 'bg-dx-border'"
                  role="switch"
                  @click="form.enabled = !form.enabled"
                >
                  <span class="inline-block w-3.5 h-3.5 rounded-full shadow-sm transform transition-transform duration-200" :class="form.enabled ? 'translate-x-[18px] bg-white' : 'translate-x-[3px]'" :style="{ backgroundColor: form.enabled ? '#fff' : '#64748B' }" />
                </button>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="flex-shrink-0 flex items-center justify-between px-6 py-4 border-t border-dx-border bg-dx-card-hover/30">
            <span class="text-xs text-dx-text-muted">创建后将在调度列表中显示</span>
            <div class="flex items-center gap-3">
              <button class="h-9 px-5 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors" @click="closeDrawer">取消</button>
              <button class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors" @click="handleCreate">{{ isEditMode ? '保存' : '创建' }}</button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>

  <!-- Manual Run Modal -->
  <ManualRunModal
    :visible="runModalVisible"
    :task="runSchedule ? { id: runSchedule.id, name: runSchedule.taskName } : null"
    @close="runModalVisible = false; runSchedule = null"
    @confirm="handleConfirmRunNow"
  />
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useAppStore } from '@/stores/app';
import ManualRunModal from '@/components/common/ManualRunModal.vue';

const store = useAppStore();

const filters = reactive({ taskId: '', taskName: '', keyword: '' });

function handleSearch() {}
function handleReset() {
  filters.taskId = '';
  filters.taskName = '';
  filters.keyword = '';
}

interface Schedule { id: string; taskName: string; cron: string; nextRun: string; nextRunRelative: string; lastRun: string; lastStatus: string; recentStatus: string; enabled: boolean; }
const schedules = ref<Schedule[]>([
  { id: 'DX-20240512-001', taskName: '用户行为数据同步', cron: '0 2 * * *', nextRun: '2024-05-13 02:00', nextRunRelative: '约 7h 后', lastRun: '2024-05-12 02:00', lastStatus: '成功 (3m 42s)', recentStatus: '成功', enabled: true },
  { id: 'DX-20240512-002', taskName: '订单数据ETL', cron: '*/30 * * * *', nextRun: '2024-05-12 19:00', nextRunRelative: '约 15m 后', lastRun: '2024-05-12 18:30', lastStatus: '成功 (12m 18s)', recentStatus: '运行中', enabled: true },
  { id: 'DX-20240512-004', taskName: '商品信息全量同步', cron: '0 1 * * 0', nextRun: '2024-05-19 01:00', nextRunRelative: '6天后', lastRun: '2024-05-12 01:00', lastStatus: '失败 (2m 33s)', recentStatus: '失败', enabled: true },
  { id: 'DX-20240512-003', taskName: '日志数据清洗', cron: '0 8 * * 1-5', nextRun: '2024-05-13 08:00', nextRunRelative: '约 13h 后', lastRun: '2024-05-10 08:00', lastStatus: '已跳过 (非工作日)', recentStatus: '等待中', enabled: false },
  { id: 'DX-20240512-006', taskName: '库存数据增量同步', cron: '*/5 8-22 * * *', nextRun: '2024-05-12 18:50', nextRunRelative: '约 5m 后', lastRun: '2024-05-12 18:45', lastStatus: '成功 (1m 15s)', recentStatus: '成功', enabled: true },
  { id: 'DX-20240512-005', taskName: '用户画像更新', cron: '0 3 1 * *', nextRun: '2024-06-01 03:00', nextRunRelative: '19天后', lastRun: '2024-05-01 03:00', lastStatus: '成功 (45m 10s)', recentStatus: '成功', enabled: false },
]);

const filteredSchedules = computed(() => {
  let list = [...schedules.value];
  if (filters.taskId) list = list.filter((s) => s.id.toLowerCase().includes(filters.taskId.toLowerCase()));
  if (filters.taskName) list = list.filter((s) => s.taskName.includes(filters.taskName));
  if (filters.keyword) {
    const kw = filters.keyword.toLowerCase();
    list = list.filter((s) => s.id.toLowerCase().includes(kw) || s.taskName.toLowerCase().includes(kw));
  }
  return list;
});

const overviewCards = computed(() => {
  const running = schedules.value.filter((s) => s.enabled).length;
  const paused = schedules.value.length - running;
  return [
    { label: '总调度数', value: schedules.value.length, color: 'text-dx-text-primary', sub: '' },
    { label: '运行中', value: running, color: 'text-dx-success', sub: Math.round((running / schedules.value.length) * 100) + '%' },
    { label: '已暂停', value: paused, color: 'text-dx-warning', sub: Math.round((paused / schedules.value.length) * 100) + '%' },
    { label: '今日执行', value: '1,247', color: 'text-dx-accent', sub: '成功 98.2%' },
  ];
});

function cronParts(cron: string) { return cron.split(' '); }
function cronPartColor(i: number) { const c = ['text-cyan-400','text-amber-400','text-emerald-400','text-purple-400','text-dx-text-secondary']; return c[i] || ''; }
function cronPartBg(i: number) { const b = ['#0c1222','#0c1222','#0c1222','#0c1222','#0c1222']; return b[i] || '#0c1222'; }

function cronDescription(cron: string) {
  const m: Record<string, string> = {
    '0 * * * *': '每小时整点',
    '*/30 * * * *': '每 30 分钟',
    '*/15 * * * *': '每 15 分钟',
    '*/5 * * * *': '每 5 分钟',
    '0 2 * * *': '每天凌晨 2:00',
    '0 8 * * *': '每天早上 8:00',
    '0 1 * * 0': '每周日凌晨 1:00',
    '0 8 * * 1-5': '工作日早上 8:00',
    '*/30 * * * 1-5': '工作日每 30 分钟',
    '*/5 8-22 * * *': '8:00-22:00 每 5 分钟',
    '0 3 1 * *': '每月 1 号凌晨 3:00',
  };
  return m[cron] ?? cron;
}

function handleEdit(s: Schedule) { openDrawer(s); }
function handleRunNow(s: Schedule) {
  runSchedule.value = s;
  runModalVisible.value = true;
}
function handleQueryLog(s: Schedule) {
  store.openLogDialog({
    taskId: s.id,
    taskName: s.taskName,
    params: '--channel=3 --speed=5MB/s',
  });
}
function handleDelete(s: Schedule) { schedules.value = schedules.value.filter((x) => x.id !== s.id); }

// --- Drawer ---
const drawerVisible = ref(false);
const editingSchedule = ref<Schedule | null>(null);
const isEditMode = computed(() => editingSchedule.value !== null);
const cronMode = ref<'preset' | 'custom'>('preset');
const form = reactive({ taskId: '', cron: '0 2 * * *', enabled: true });

const cronPresets = [
  { label: '每小时', cron: '0 * * * *' },
  { label: '每30分钟', cron: '*/30 * * * *' },
  { label: '每15分钟', cron: '*/15 * * * *' },
  { label: '每5分钟', cron: '*/5 * * * *' },
  { label: '每天凌晨 2:00', cron: '0 2 * * *' },
  { label: '每天早上 8:00', cron: '0 8 * * *' },
  { label: '工作日早上 8:00', cron: '0 8 * * 1-5' },
  { label: '工作日每30分钟', cron: '*/30 * * * 1-5' },
  { label: '每周日凌晨 1:00', cron: '0 1 * * 0' },
  { label: '每月1号凌晨 3:00', cron: '0 3 1 * *' },
];

function selectPreset(p: { label: string; cron: string }) {
  form.cron = p.cron;
}

const availableTasks = [
  { id: 'DX-20240512-001', name: '用户行为数据同步' },
  { id: 'DX-20240512-002', name: '订单数据ETL' },
  { id: 'DX-20240512-003', name: '日志数据清洗' },
  { id: 'DX-20240512-004', name: '商品信息全量同步' },
  { id: 'DX-20240512-005', name: '用户画像更新' },
  { id: 'DX-20240512-006', name: '库存数据增量同步' },
  { id: 'DX-20240512-007', name: '广告投放数据汇总' },
];

const selectedTaskName = computed(() => {
  const t = availableTasks.find((t) => t.id === form.taskId);
  return t ? t.name : '—';
});

function openDrawer(schedule?: Schedule) {
  editingSchedule.value = schedule ?? null;
  cronMode.value = 'preset';
  if (schedule) {
    form.taskId = schedule.id;
    form.cron = schedule.cron;
    form.enabled = schedule.enabled;
    const preset = cronPresets.find((p) => p.cron === schedule.cron);
    if (preset) cronMode.value = 'preset';
    else cronMode.value = 'custom';
  } else {
    form.taskId = '';
    form.cron = '0 2 * * *';
    form.enabled = true;
  }
  drawerVisible.value = true;
}

function closeDrawer() {
  drawerVisible.value = false;
  editingSchedule.value = null;
}

function handleCreate() {
  if (!form.taskId || !form.cron) return;
  const task = availableTasks.find((t) => t.id === form.taskId);

  if (isEditMode.value && editingSchedule.value) {
    Object.assign(editingSchedule.value, {
      taskName: task?.name ?? form.taskId,
      cron: form.cron,
      enabled: form.enabled,
    });
  } else {
    const newSchedule: Schedule = {
      id: form.taskId,
      taskName: task?.name ?? form.taskId,
      cron: form.cron,
      nextRun: '—',
      nextRunRelative: '—',
      lastRun: '—',
      lastStatus: '—',
      recentStatus: '等待中',
      enabled: form.enabled,
    };
    schedules.value.unshift(newSchedule);
  }
  closeDrawer();
}

// --- Manual Run Modal ---
const runModalVisible = ref(false);
const runSchedule = ref<Schedule | null>(null);

function handleConfirmRunNow(params: string, jvmArgs: string) {
  console.log('Run schedule:', runSchedule.value?.id, { params, jvmArgs });
  runModalVisible.value = false;
  runSchedule.value = null;
}
</script>

<style scoped>
.drawer-enter-active {
  transition: opacity 0.35s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.drawer-leave-active {
  transition: opacity 0.25s cubic-bezier(0.55, 0, 1, 0.45);
}
.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-enter-active .drawer-panel,
.drawer-leave-active .drawer-panel {
  transition:
    transform 0.35s cubic-bezier(0.22, 0.61, 0.36, 1),
    box-shadow 0.35s ease;
  will-change: transform;
}
.drawer-enter-from .drawer-panel {
  transform: translateX(100%);
  box-shadow: none;
}
.drawer-leave-to .drawer-panel {
  transform: translateX(100%);
  box-shadow: none;
}
.drawer-enter-to .drawer-panel,
.drawer-leave-from .drawer-panel {
  transform: translateX(0);
}
</style>
