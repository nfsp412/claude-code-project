<template>
  <div class="p-6 flex flex-col gap-4">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span>/</span><span class="text-dx-accent">调度管理</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">调度管理</h1>
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
    <div class="flex items-center gap-3">
      <div class="relative flex-1 max-w-sm"><input v-model="searchQuery" type="text" placeholder="搜索任务名称..." class="w-full h-9 pl-9 pr-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent"><svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-dx-text-muted" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.3-4.3"/></svg></div>
      <button class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors">搜索</button>
      <button class="h-9 px-4 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5 ml-auto"><svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M12 5v14M5 12h14"/></svg> 新建调度</button>
    </div>

    <!-- Schedule Table -->
    <div class="bg-dx-card border border-dx-border rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm"><thead><tr class="bg-dx-input border-b border-dx-border"><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">任务名称</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">Cron 表达式</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">下次执行</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">上次执行</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">最近状态</th><th class="text-center py-3 px-4 text-xs font-medium text-dx-text-muted uppercase w-[80px]">启用</th><th class="text-right py-3 px-4 text-xs font-medium text-dx-text-muted uppercase w-[130px]">操作</th></tr></thead>
          <tbody>
            <tr v-for="s in filteredSchedules" :key="s.id" class="border-b border-dx-border/50 hover:bg-dx-card-hover transition-colors last:border-b-0">
              <td class="py-3 px-4"><span class="text-dx-text-primary font-medium">{{ s.taskName }}</span><br><span class="text-xs text-dx-text-muted">{{ s.id }}</span></td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-1 flex-wrap">
                  <span v-for="(part, pi) in cronParts(s.cron)" :key="pi" class="inline-block px-1.5 py-0.5 rounded text-[11px] font-mono border" :class="cronPartColor(pi)" :style="{ background: cronPartBg(pi) }">{{ part }}</span>
                </div>
                <span class="text-[10px] text-dx-text-muted mt-1 block">{{ cronDescription(s.cron) }}</span>
              </td>
              <td class="py-3 px-4 text-xs"><span class="text-dx-accent">{{ s.nextRun }}</span><br><span class="text-[10px] text-dx-text-muted">{{ s.nextRunRelative }}</span></td>
              <td class="py-3 px-4 text-xs"><span class="text-dx-text-secondary">{{ s.lastRun }}</span><br><span class="text-[10px]" :class="s.lastStatus === '成功' ? 'text-emerald-400' : 'text-dx-danger'">{{ s.lastStatus }}</span></td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center gap-1.5 text-xs px-2 py-0.5 rounded" :class="statusBadge(s.recentStatus)">
                  <span class="w-1.5 h-1.5 rounded-full" :class="statusDot(s.recentStatus)" />{{ s.recentStatus }}
                </span>
              </td>
              <td class="py-3 px-4 text-center">
                <button class="relative inline-flex items-center w-9 h-5 rounded-full transition-colors duration-200 focus:outline-none" :class="s.enabled ? 'bg-dx-accent' : 'bg-dx-border'" role="switch" @click="s.enabled = !s.enabled">
                  <span class="inline-block w-3.5 h-3.5 rounded-full shadow-sm transform transition-transform duration-200" :class="s.enabled ? 'translate-x-[18px] bg-white' : 'translate-x-[3px]'" :style="{ backgroundColor: s.enabled ? '#fff' : '#64748B' }" />
                </button>
              </td>
              <td class="py-3 px-4 text-right"><div class="flex items-center justify-end gap-1"><button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-accent transition-colors" @click="handleEdit(s)">编辑</button><button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-accent transition-colors" @click="handleRunNow(s)">立即执行</button><button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-red-500/10 hover:text-dx-danger transition-colors" @click="handleDelete(s)">删除</button></div></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="flex items-center justify-between px-4 py-3 border-t border-dx-border bg-dx-card-hover/30"><span class="text-xs text-dx-text-muted">共 {{ schedules.length }} 条调度</span><div class="flex items-center gap-1"><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">‹</button><button class="w-8 h-8 rounded-md text-xs font-medium bg-dx-accent text-white">1</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">2</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">3</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">›</button></div></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const searchQuery = ref('');

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
  if (!searchQuery.value) return schedules.value;
  const q = searchQuery.value.toLowerCase();
  return schedules.value.filter((s) => s.taskName.toLowerCase().includes(q) || s.id.toLowerCase().includes(q));
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
  const m: Record<string, string> = { '0 2 * * *': '每天凌晨 2:00', '*/30 * * * *': '每 30 分钟', '0 1 * * 0': '每周日凌晨 1:00', '0 8 * * 1-5': '工作日早上 8:00', '*/5 8-22 * * *': '8:00-22:00 每5分钟', '0 3 1 * *': '每月1号凌晨 3:00' };
  return m[cron] ?? cron;
}

function statusBadge(s: string) { const m: Record<string, string> = { '成功': 'bg-emerald-500/10 text-emerald-400', '运行中': 'bg-cyan-500/10 text-cyan-400', '失败': 'bg-red-500/10 text-red-400', '等待中': 'bg-amber-500/10 text-amber-400' }; return m[s] ?? ''; }
function statusDot(s: string) { const m: Record<string, string> = { '成功': 'bg-emerald-400', '运行中': 'bg-cyan-400', '失败': 'bg-red-400', '等待中': 'bg-amber-400' }; return m[s] ?? ''; }

function handleEdit(s: Schedule) { console.log('Edit:', s.id); }
function handleRunNow(s: Schedule) { console.log('Run now:', s.id); }
function handleDelete(s: Schedule) { schedules.value = schedules.value.filter((x) => x.id !== s.id); }
</script>
