<template>
  <div class="p-6 flex flex-col gap-4">
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span>/</span><span class="text-dx-accent">资源使用情况监控</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">资源使用情况监控仪表盘</h1>
    </div>

    <!-- Time Range -->
    <div class="flex items-center gap-2">
      <div class="flex bg-dx-input rounded-md p-0.5">
        <button v-for="opt in timeOptions" :key="opt.value" class="px-3 py-1.5 rounded text-xs font-medium transition-colors" :class="timeRange === opt.value ? 'bg-dx-accent text-white' : 'text-dx-text-secondary hover:text-dx-text-primary'" @click="timeRange = opt.value">{{ opt.label }}</button>
      </div>
      <span class="text-2xs text-dx-text-muted ml-2">自动刷新: 30s</span>
    </div>

    <!-- Overview Cards -->
    <div class="grid grid-cols-4 gap-4">
      <div v-for="card in overviewCards" :key="card.label" class="bg-dx-card border border-dx-border rounded-lg p-4">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs text-dx-text-muted">{{ card.label }}</span>
          <div class="w-8 h-8 rounded-lg flex items-center justify-center" :class="card.iconBg"><svg class="w-4 h-4" :class="card.iconColor" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><component :is="card.icon" /></svg></div>
        </div>
        <div class="text-2xl font-bold text-dx-text-primary" v-html="card.value" />
        <div v-if="card.progress != null" class="mt-2 h-1.5 rounded-full bg-dx-input"><div class="h-full rounded-full transition-all duration-500" :style="{ width: card.progress + '%', backgroundColor: card.barColor }" /></div>
        <div v-if="card.sub" class="text-xs text-dx-text-muted mt-1">{{ card.sub }}</div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-3 gap-4">
      <CpuTrendChart />
      <MemoryRingChart />
    </div>

    <!-- Node Resource Table -->
    <div class="bg-dx-card border border-dx-border rounded-lg overflow-hidden">
      <div class="flex items-center justify-between px-5 py-3 border-b border-dx-border"><h3 class="text-sm font-semibold text-dx-text-primary">节点资源详情</h3><span class="text-xs text-dx-text-muted">最后更新: 18:42:15</span></div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm"><thead><tr class="bg-dx-input border-b border-dx-border"><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">节点</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">CPU</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">内存</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">磁盘</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">网络</th><th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">运行任务</th><th class="text-right py-3 px-4 text-xs font-medium text-dx-text-muted uppercase">状态</th></tr></thead>
          <tbody>
            <tr v-for="node in nodeData" :key="node.host" class="border-b border-dx-border/50 hover:bg-dx-card-hover transition-colors last:border-b-0">
              <td class="py-3 px-4"><span class="text-dx-text-primary font-medium">{{ node.host }}</span><br><span class="text-xs text-dx-text-muted">{{ node.ip }}</span></td>
              <td class="py-3 px-4"><div class="flex items-center gap-2"><span class="text-xs font-mono w-10" :class="node.cpu > 85 ? 'text-dx-danger' : 'text-dx-text-primary'">{{ node.cpu }}%</span><div class="w-20 h-1.5 rounded-full bg-dx-input"><div class="h-full rounded-full transition-all duration-500" :style="{ width: node.cpu + '%', backgroundColor: node.cpu > 85 ? '#EF4444' : node.cpu > 65 ? '#F59E0B' : '#10B981' }" /></div></div></td>
              <td class="py-3 px-4"><div class="flex items-center gap-2"><span class="text-xs font-mono w-10" :class="node.mem > 85 ? 'text-dx-danger' : 'text-dx-text-primary'">{{ node.mem }}%</span><div class="w-20 h-1.5 rounded-full bg-dx-input"><div class="h-full rounded-full transition-all duration-500" :style="{ width: node.mem + '%', backgroundColor: node.mem > 85 ? '#EF4444' : node.mem > 65 ? '#F59E0B' : '#10B981' }" /></div></div></td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary">{{ node.disk }}%</td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary" :class="{ 'text-dx-text-muted': !node.netIn }">{{ node.netIn ? `↓${node.netIn} ↑${node.netOut} MB/s` : '—' }}</td>
              <td class="py-3 px-4 text-xs font-mono" :class="node.tasks ? 'text-dx-text-primary' : 'text-dx-text-muted'">{{ node.tasks || '—' }}</td>
              <td class="py-3 px-4 text-right">
                <span class="inline-flex items-center gap-1.5 text-xs px-2 py-0.5 rounded" :class="node.status === '在线' ? 'bg-emerald-500/10 text-emerald-400' : node.status === '高负载' ? 'bg-dx-danger/10 text-dx-danger' : 'bg-amber-500/10 text-amber-400'">
                  <span class="w-1.5 h-1.5 rounded-full" :class="node.status === '在线' ? 'bg-emerald-400' : node.status === '高负载' ? 'bg-dx-danger animate-pulse' : 'bg-amber-400'" />{{ node.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, h } from 'vue';
import CpuTrendChart from '@/components/charts/CpuTrendChart.vue';
import MemoryRingChart from '@/components/charts/MemoryRingChart.vue';

const timeRange = ref('realtime');
const timeOptions = [{ value: 'realtime', label: '实时' },{ value: '1h', label: '1h' },{ value: '6h', label: '6h' },{ value: '24h', label: '24h' }];

const overviewCards = [
  { label: '集群节点', value: '12<span class="text-sm text-dx-success ml-2">● 10 在线</span>', progress: null, sub: '', iconBg: 'bg-cyan-500/10', iconColor: 'text-cyan-400', barColor: '', icon: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2M11 17h2M11 7h2' }) },
  { label: 'CPU 使用率', value: '67<span class="text-sm text-dx-text-secondary">%</span>', progress: 67, sub: '', iconBg: 'bg-emerald-500/10', iconColor: 'text-emerald-400', barColor: '#10B981', icon: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' }) },
  { label: '内存使用率', value: '78<span class="text-sm text-dx-text-secondary">%</span>', progress: 78, sub: '', iconBg: 'bg-amber-500/10', iconColor: 'text-amber-400', barColor: '#F59E0B', icon: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M20 12H4' }) },
  { label: '磁盘 I/O', value: '320<span class="text-sm text-dx-text-secondary"> MB/s</span>', progress: null, sub: '读: 180 MB/s | 写: 140 MB/s', iconBg: 'bg-purple-500/10', iconColor: 'text-purple-400', barColor: '', icon: () => [h('circle', { cx: '12', cy: '12', r: '10' }), h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 6v6l4 2' })] },
];

const nodeData = [
  { host: 'dx-worker-nj-01', ip: '10.23.45.101', cpu: 72, mem: 85, disk: 42, netIn: '120', netOut: '80', tasks: 3, status: '在线' },
  { host: 'dx-worker-nj-02', ip: '10.23.45.102', cpu: 45, mem: 62, disk: 38, netIn: '95', netOut: '65', tasks: 2, status: '在线' },
  { host: 'dx-worker-nj-03', ip: '10.23.45.103', cpu: 91, mem: 88, disk: 55, netIn: '210', netOut: '150', tasks: 5, status: '高负载' },
  { host: 'dx-worker-nj-04', ip: '10.23.45.104', cpu: 0, mem: 5, disk: 12, netIn: '', netOut: '', tasks: 0, status: '离线' },
];
</script>
