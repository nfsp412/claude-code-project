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
      <!-- CPU Trend -->
      <div class="bg-dx-card border border-dx-border rounded-lg p-5 col-span-2">
        <div class="flex items-center justify-between mb-4"><h3 class="text-sm font-semibold text-dx-text-primary">CPU 使用趋势</h3><div class="flex items-center gap-3"><span class="flex items-center gap-1.5 text-xs text-dx-text-muted"><span class="w-2.5 h-2.5 rounded-sm bg-cyan-400" /> 平均</span><span class="flex items-center gap-1.5 text-xs text-dx-text-muted"><span class="w-2.5 h-2.5 rounded-sm bg-dx-warning" /> 峰值</span></div></div>
        <div class="flex items-end gap-1 h-44 px-1">
          <div v-for="(d, i) in cpuTrendData" :key="i" class="flex-1 flex flex-col items-center gap-0.5">
            <div class="w-full rounded-t-sm" :style="{ height: d.peak * 1.4 + 'px', background: '#F59E0B', opacity: 0.3 }" />
            <div class="w-full rounded-t-sm" :style="{ height: d.avg * 1.4 + 'px', background: '#06B6D4', marginTop: -(d.peak * 1.4) + 'px' }" />
          </div>
        </div>
        <div class="flex justify-between text-2xs text-dx-text-muted mt-2 px-1"><span>14:00</span><span>15:00</span><span>16:00</span><span>17:00</span><span>18:00</span><span>现在</span></div>
      </div>

      <!-- Memory Breakdown -->
      <div class="bg-dx-card border border-dx-border rounded-lg p-5">
        <h3 class="text-sm font-semibold text-dx-text-primary mb-4">内存分布</h3>
        <div class="w-32 h-32 mx-auto mb-4 relative">
          <svg viewBox="0 0 128 128"><circle cx="64" cy="64" r="48" fill="none" stroke="#06B6D4" stroke-width="18" stroke-dasharray="120 181" /><circle cx="64" cy="64" r="48" fill="none" stroke="#10B981" stroke-width="18" stroke-dasharray="105 196" stroke-dashoffset="-120" /><circle cx="64" cy="64" r="48" fill="none" stroke="#F59E0B" stroke-width="18" stroke-dasharray="45 256" stroke-dashoffset="-225" /><circle cx="64" cy="64" r="48" fill="none" stroke="#EF4444" stroke-width="18" stroke-dasharray="31 270" stroke-dashoffset="-270" /></svg>
          <div class="absolute inset-0 flex items-center justify-center"><span class="text-lg font-bold text-dx-text-primary">78%</span></div>
        </div>
        <div class="flex flex-col gap-2 text-xs">
          <div v-for="seg in memorySegments" :key="seg.label" class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-sm" :style="{ background: seg.color }" /><span class="text-dx-text-secondary">{{ seg.label }}</span><span class="ml-auto text-dx-text-primary font-mono">{{ seg.value }}</span></div>
        </div>
      </div>
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

const timeRange = ref('realtime');
const timeOptions = [{ value: 'realtime', label: '实时' },{ value: '1h', label: '1h' },{ value: '6h', label: '6h' },{ value: '24h', label: '24h' }];

const overviewCards = [
  { label: '集群节点', value: '12<span class="text-sm text-dx-success ml-2">● 10 在线</span>', progress: null, sub: '', iconBg: 'bg-cyan-500/10', iconColor: 'text-cyan-400', barColor: '', icon: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2M11 17h2M11 7h2' }) },
  { label: 'CPU 使用率', value: '67<span class="text-sm text-dx-text-secondary">%</span>', progress: 67, sub: '', iconBg: 'bg-emerald-500/10', iconColor: 'text-emerald-400', barColor: '#10B981', icon: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' }) },
  { label: '内存使用率', value: '78<span class="text-sm text-dx-text-secondary">%</span>', progress: 78, sub: '', iconBg: 'bg-amber-500/10', iconColor: 'text-amber-400', barColor: '#F59E0B', icon: () => h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M20 12H4' }) },
  { label: '磁盘 I/O', value: '320<span class="text-sm text-dx-text-secondary"> MB/s</span>', progress: null, sub: '读: 180 MB/s | 写: 140 MB/s', iconBg: 'bg-purple-500/10', iconColor: 'text-purple-400', barColor: '', icon: () => [h('circle', { cx: '12', cy: '12', r: '10' }), h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M12 6v6l4 2' })] },
];

const cpuTrendData = Array.from({ length: 24 }, () => ({ avg: 30 + Math.random() * 50, peak: 45 + Math.random() * 40 }));

const memorySegments = [
  { label: 'DataX Worker', value: '38 GB', color: '#06B6D4' },
  { label: '系统缓存', value: '28 GB', color: '#10B981' },
  { label: 'JVM Heap', value: '12 GB', color: '#F59E0B' },
  { label: '其他', value: '8 GB', color: '#EF4444' },
];

const nodeData = [
  { host: 'dx-worker-nj-01', ip: '10.23.45.101', cpu: 72, mem: 85, disk: 42, netIn: '120', netOut: '80', tasks: 3, status: '在线' },
  { host: 'dx-worker-nj-02', ip: '10.23.45.102', cpu: 45, mem: 62, disk: 38, netIn: '95', netOut: '65', tasks: 2, status: '在线' },
  { host: 'dx-worker-nj-03', ip: '10.23.45.103', cpu: 91, mem: 88, disk: 55, netIn: '210', netOut: '150', tasks: 5, status: '高负载' },
  { host: 'dx-worker-nj-04', ip: '10.23.45.104', cpu: 0, mem: 5, disk: 12, netIn: '', netOut: '', tasks: 0, status: '离线' },
];
</script>
