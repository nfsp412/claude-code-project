<template>
  <div class="p-6 flex flex-col gap-4">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span>/</span><span class="text-dx-accent">DataX 执行集群管理</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">DataX 执行集群管理</h1>
    </div>

    <!-- Overview Cards -->
    <div class="grid grid-cols-5 gap-4">
      <div v-for="card in overviewCards" :key="card.label" class="bg-dx-card border border-dx-border rounded-lg p-4">
        <span class="text-xs text-dx-text-muted">{{ card.label }}</span>
        <div class="text-2xl font-bold mt-1" :class="card.color">{{ card.value }}</div>
        <span class="text-xs" :class="card.subColor || 'text-dx-text-muted'">{{ card.sub }}</span>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="flex items-center gap-3">
      <div class="relative flex-1 max-w-sm"><input v-model="searchQuery" type="text" placeholder="搜索节点主机名 / IP..." class="w-full h-9 pl-9 pr-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"><svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-dx-text-muted" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" d="M21 21l-4.3-4.3"/></svg></div>
      <button class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors">搜索</button>
      <button class="h-9 px-4 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5 ml-auto"><svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M12 5v14M5 12h14"/></svg> 注册节点</button>
      <button class="h-9 px-4 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover transition-colors flex items-center gap-1.5"><svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg> 刷新状态</button>
    </div>

    <!-- Node Table -->
    <div class="bg-dx-card border border-dx-border rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm"><thead><tr class="bg-dx-input border-b border-dx-border"><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">节点信息</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">规格</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">CPU 使用</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">内存使用</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">运行任务</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">运行时间</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">状态</th><th class="text-right py-3 px-4 text-xs font-medium text-dx-text-muted uppercase w-[120px]">操作</th></tr></thead>
          <tbody>
            <tr v-for="node in filteredNodes" :key="node.host" class="border-b border-dx-border/50 hover:bg-dx-card-hover transition-colors last:border-b-0">
              <td class="py-3 px-4"><div class="font-medium text-dx-text-primary">{{ node.host }}</div><div class="text-xs text-dx-text-muted font-mono">{{ node.ip }}</div></td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary">{{ node.spec }}</td>
              <td class="py-3 px-4"><div v-if="node.online" class="flex items-center gap-2"><span class="text-xs font-mono w-10" :class="node.cpu > 85 ? 'text-dx-danger' : 'text-dx-text-primary'">{{ node.cpu }}%</span><div class="w-20 h-1.5 rounded-full bg-dx-input"><div class="h-full rounded-full transition-all duration-500" :style="{ width: node.cpu + '%', backgroundColor: node.cpu > 85 ? '#EF4444' : node.cpu > 65 ? '#F59E0B' : '#10B981' }" /></div></div><span v-else class="text-xs text-dx-text-muted">—</span></td>
              <td class="py-3 px-4"><div v-if="node.online" class="flex items-center gap-2"><span class="text-xs font-mono w-10" :class="node.mem > 85 ? 'text-dx-danger' : 'text-dx-text-primary'">{{ node.mem }}%</span><div class="w-20 h-1.5 rounded-full bg-dx-input"><div class="h-full rounded-full transition-all duration-500" :style="{ width: node.mem + '%', backgroundColor: node.mem > 85 ? '#EF4444' : node.mem > 65 ? '#F59E0B' : '#10B981' }" /></div></div><span v-else class="text-xs text-dx-text-muted">—</span></td>
              <td class="py-3 px-4 text-xs font-mono" :class="node.online ? 'text-dx-text-primary' : 'text-dx-text-muted'"><span v-if="node.online"><span :class="node.tasks > node.maxTasks * 0.8 ? 'text-dx-danger' : 'text-dx-accent'">{{ node.tasks }}</span> / {{ node.maxTasks }}</span><span v-else>—</span></td>
              <td class="py-3 px-4 text-xs" :class="node.online ? 'text-dx-text-secondary' : 'text-dx-text-muted'">{{ node.online ? node.uptime : '—' }}</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center gap-1.5 text-xs px-2 py-0.5 rounded" :class="node.statusColor">{{ node.online ? (node.cpu > 85 || node.mem > 85 ? '⚠ 高负载' : '● 在线') : '● 离线' }}</span>
              </td>
              <td class="py-3 px-4 text-right">
                <div class="relative inline-block">
                  <button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-dx-card-hover transition-colors" @click="toggleMenu(node.host)" @blur="closeMenu">操作 ▾</button>
                  <div v-if="openMenuId === node.host" class="absolute right-0 top-full mt-1 z-50 min-w-[120px] bg-dx-card border border-dx-border rounded-lg shadow-lg py-1">
                    <button class="w-full text-left px-3 py-2 text-xs text-dx-text-secondary hover:bg-dx-card-hover transition-colors" @mousedown.prevent="handleAction(node, 'detail')">查看详情</button>
                    <button v-if="node.online" class="w-full text-left px-3 py-2 text-xs text-dx-warning hover:bg-amber-500/10 transition-colors" @mousedown.prevent="handleAction(node, 'drain')">排空任务</button>
                    <div class="border-t border-dx-border my-1" />
                    <button v-if="node.online" class="w-full text-left px-3 py-2 text-xs text-dx-danger hover:bg-red-500/10 transition-colors" @mousedown.prevent="handleAction(node, 'offline')">下线节点</button>
                    <button v-else class="w-full text-left px-3 py-2 text-xs text-dx-text-secondary hover:bg-dx-card-hover transition-colors" @mousedown.prevent="handleAction(node, 'reconnect')">重新连接</button>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="flex items-center justify-between px-4 py-3 border-t border-dx-border bg-dx-card-hover/30"><span class="text-xs text-dx-text-muted">共 {{ nodes.length }} 个节点</span><div class="flex items-center gap-1"><button class="w-8 h-8 rounded-md text-xs text-dx-text-muted/40 cursor-not-allowed" disabled>‹</button><button class="w-8 h-8 rounded-md text-xs font-medium bg-dx-accent text-white">1</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">2</button><button class="w-8 h-8 rounded-md text-xs text-dx-text-secondary hover:bg-dx-card-hover">›</button></div></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface ClusterNode { host: string; ip: string; spec: string; cpu: number; mem: number; disk: number; tasks: number; maxTasks: number; uptime: string; online: boolean; statusColor: string; }

const nodes = ref<ClusterNode[]>([
  { host: 'dx-worker-nj-01', ip: '10.23.45.101:8801', spec: '8C / 16G / 200G SSD', cpu: 72, mem: 85, disk: 42, tasks: 3, maxTasks: 8, uptime: '45天 12h', online: true, statusColor: 'bg-emerald-500/10 text-emerald-400' },
  { host: 'dx-worker-nj-02', ip: '10.23.45.102:8801', spec: '8C / 16G / 200G SSD', cpu: 45, mem: 58, disk: 38, tasks: 2, maxTasks: 8, uptime: '120天 3h', online: true, statusColor: 'bg-emerald-500/10 text-emerald-400' },
  { host: 'dx-worker-nj-03', ip: '10.23.45.103:8801', spec: '16C / 32G / 500G SSD', cpu: 91, mem: 88, disk: 55, tasks: 7, maxTasks: 16, uptime: '90天 8h', online: true, statusColor: 'bg-dx-danger/10 text-dx-danger' },
  { host: 'dx-worker-nj-04', ip: '10.23.45.104:8801', spec: '16C / 32G / 500G SSD', cpu: 0, mem: 0, disk: 12, tasks: 0, maxTasks: 16, uptime: '', online: false, statusColor: 'bg-amber-500/10 text-amber-400' },
]);

const searchQuery = ref('');
const filteredNodes = computed(() => {
  if (!searchQuery.value) return nodes.value;
  const q = searchQuery.value.toLowerCase();
  return nodes.value.filter((n) => n.host.includes(q) || n.ip.includes(q));
});

const overviewCards = computed(() => {
  const online = nodes.value.filter((n) => n.online);
  const offline = nodes.value.filter((n) => !n.online);
  const running = online.reduce((s, n) => s + n.tasks, 0);
  return [
    { label: '集群节点', value: nodes.value.length, color: 'text-dx-text-primary', sub: '总计', subColor: 'text-dx-text-muted' },
    { label: '在线节点', value: online.length, color: 'text-dx-success', sub: Math.round((online.length / nodes.value.length) * 100) + '%', subColor: 'text-dx-text-muted' },
    { label: '离线节点', value: offline.length, color: 'text-dx-text-muted', sub: Math.round((offline.length / nodes.value.length) * 100) + '%', subColor: 'text-dx-text-muted' },
    { label: '运行中任务', value: running, color: 'text-dx-accent', sub: '当前', subColor: 'text-dx-text-muted' },
    { label: '集群版本', value: 'v3.2.1', color: 'text-dx-text-primary', sub: '已是最新', subColor: 'text-dx-success' },
  ];
});

const openMenuId = ref<string | null>(null);
function toggleMenu(id: string) { openMenuId.value = openMenuId.value === id ? null : id; }
function closeMenu() { setTimeout(() => { openMenuId.value = null; }, 150); }
function handleAction(node: ClusterNode, action: string) { openMenuId.value = null; console.log(action, node.host); }
</script>
