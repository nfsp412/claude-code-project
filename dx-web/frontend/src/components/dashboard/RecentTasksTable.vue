<template>
  <div class="bg-dx-card border border-dx-border rounded-lg p-5">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-[15px] font-semibold text-dx-text-primary">近期任务列表</h3>
      <button class="text-xs text-dx-accent hover:text-cyan-300 transition-colors font-medium">
        查看全部 →
      </button>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-dx-border">
            <th class="text-left py-2.5 pr-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide">任务ID</th>
            <th class="text-left py-2.5 pr-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide">任务名称</th>
            <th class="text-left py-2.5 pr-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide">状态</th>
            <th class="text-left py-2.5 pr-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide">数据源</th>
            <th class="text-left py-2.5 pr-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide">耗时</th>
            <th class="text-right py-2.5 text-xs font-medium text-dx-text-muted uppercase tracking-wide">执行时间</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="task in tasks"
            :key="task.id"
            class="border-b border-dx-border/50 hover:bg-dx-card-hover transition-colors"
          >
            <td class="py-3 pr-4 font-mono text-xs text-dx-text-secondary">{{ task.id }}</td>
            <td class="py-3 pr-4 text-dx-text-primary font-medium">{{ task.name }}</td>
            <td class="py-3 pr-4">
              <span
                class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium"
                :class="statusClass(task.status)"
              >
                <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(task.status)" />
                {{ statusLabel(task.status) }}
              </span>
            </td>
            <td class="py-3 pr-4 text-dx-text-secondary text-xs">{{ task.dataSource }}</td>
            <td class="py-3 pr-4 text-dx-text-secondary text-xs font-mono">{{ task.duration }}</td>
            <td class="py-3 text-right text-dx-text-muted text-xs">{{ task.startTime }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TaskRecord } from '@/types';

const emptyNodes = [{ address: '10.23.45.101:8801', hostname: 'dx-worker-nj-01', spec: '8C / 16G', online: true }];
const tasks: TaskRecord[] = [
  { id: 'DX-20240512-001', name: '用户行为数据同步', status: 'success', dataSource: 'mysql_analytics', duration: '3m 42s', startTime: '2024-05-12 10:00', user: '张工', group: '数据平台组', scheduled: true, nodes: emptyNodes },
  { id: 'DX-20240512-002', name: '订单数据ETL', status: 'running', dataSource: 'pg_orders', duration: '12m 18s', startTime: '2024-05-12 10:05', user: '李工', group: '电商组', scheduled: true, nodes: emptyNodes },
  { id: 'DX-20240512-003', name: '日志数据清洗', status: 'success', dataSource: 'hdfs_logs', duration: '8m 05s', startTime: '2024-05-12 09:45', user: '王工', group: '数据平台组', scheduled: false, nodes: emptyNodes },
  { id: 'DX-20240512-004', name: '商品信息全量同步', status: 'failed', dataSource: 'mongo_products', duration: '2m 33s', startTime: '2024-05-12 09:30', user: '赵工', group: '商品组', scheduled: true, nodes: emptyNodes },
  { id: 'DX-20240512-005', name: '用户画像更新', status: 'pending', dataSource: 'hive_user_profile', duration: '—', startTime: '2024-05-12 11:00', user: '刘工', group: '增长组', scheduled: false, nodes: emptyNodes },
  { id: 'DX-20240512-006', name: '库存数据增量同步', status: 'success', dataSource: 'mysql_inventory', duration: '1m 15s', startTime: '2024-05-12 10:15', user: '陈工', group: '商品组', scheduled: true, nodes: emptyNodes },
  { id: 'DX-20240512-007', name: '广告投放数据汇总', status: 'running', dataSource: 'clickhouse_ads', duration: '5m 50s', startTime: '2024-05-12 10:10', user: '周工', group: '增长组', scheduled: true, nodes: emptyNodes },
];

function statusLabel(status: string): string {
  const map: Record<string, string> = { running: '运行中', success: '成功', failed: '失败', pending: '等待中' };
  return map[status] ?? status;
}
function statusClass(status: string): string {
  const map: Record<string, string> = {
    running: 'bg-cyan-500/10 text-cyan-400',
    success: 'bg-emerald-500/10 text-emerald-400',
    failed: 'bg-red-500/10 text-red-400',
    pending: 'bg-amber-500/10 text-amber-400',
  };
  return map[status] ?? '';
}
function statusDotClass(status: string): string {
  const map: Record<string, string> = {
    running: 'bg-cyan-400 animate-pulse',
    success: 'bg-emerald-400',
    failed: 'bg-red-400',
    pending: 'bg-amber-400',
  };
  return map[status] ?? '';
}
</script>
