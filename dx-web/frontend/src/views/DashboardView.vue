<template>
  <div class="p-6 flex flex-col gap-6">
    <!-- Breadcrumb + Title -->
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
        </svg>
        <span>/</span>
        <span class="text-dx-accent">任务监控仪表盘</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">任务监控仪表盘</h1>
    </div>

    <!-- Metric Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <MetricCard
        title="运行中任务"
        :value="142"
        :change="12"
        change-label="较昨日 +12%"
        color="accent"
      />
      <MetricCard
        title="成功任务 (今日)"
        :value="3827"
        :change="8"
        change-label="较昨日 +8%"
        color="success"
      />
      <MetricCard
        title="失败任务 (今日)"
        :value="23"
        :change="-5"
        change-label="较昨日 -5%"
        color="danger"
      />
      <MetricCard
        title="等待中任务"
        :value="56"
        :change="0"
        change-label="与昨日持平"
        color="warning"
      />
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <TaskTrendChart />
      <TaskStatusChart />
    </div>

    <!-- Recent Tasks Table -->
    <RecentTasksTable />
  </div>
</template>

<script setup lang="ts">
import MetricCard from '@/components/dashboard/MetricCard.vue';
import TaskTrendChart from '@/components/dashboard/TaskTrendChart.vue';
import TaskStatusChart from '@/components/dashboard/TaskStatusChart.vue';
import RecentTasksTable from '@/components/dashboard/RecentTasksTable.vue';
</script>
