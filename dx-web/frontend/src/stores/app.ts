import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { MenuItem, UserInfo, LogLine, HighlightedTask } from '@/types';

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false);
  const activeMenu = ref('dashboard');
  const userInfo = ref<UserInfo>({
    name: '张工',
    hdfsAccount: 'hdfs://prod-cluster-nj-01',
  });

  const menuItems = ref<MenuItem[]>([
    { key: 'dashboard', label: '任务监控仪表盘', icon: 'LayoutDashboard', path: '/' },
    { key: 'task-list', label: '任务列表', icon: 'List', path: '/tasks/list' },
    { key: 'task-builder', label: '任务构建', icon: 'Hammer', path: '/tasks/builder' },
    { key: 'schedule-config', label: '任务调度', icon: 'Clock', path: '/schedule' },
    { key: 'schedule-run-detail', label: '任务运行明细', icon: 'FileText', path: '/schedule/run-detail' },
    { key: 'datasource', label: '数据源管理', icon: 'Database', path: '/datasource' },
    { key: 'logs', label: '日志查询', icon: 'FileSearch', path: '/logs' },
    { key: 'cluster', label: 'DataX执行集群管理', icon: 'Server', path: '/cluster' },
    { key: 'resource', label: '资源使用监控', icon: 'Activity', path: '/resource' },
    { key: 'json-tool', label: 'JSON格式化', icon: 'Braces', path: '/json-tool' },
    { key: 'task-canvas', label: '节点画布', icon: 'GitGraph', path: '/task-canvas' },
  ]);

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value;
  }

  function setActiveMenu(key: string) {
    activeMenu.value = key;
  }

  // --- Log Dialog ---
  const logDialogVisible = ref(false);
  const logDialogData = ref<{
    taskId: string;
    taskName: string;
    params: string;
    logLines: LogLine[];
  }>({
    taskId: '',
    taskName: '',
    params: '',
    logLines: [],
  });

  function openLogDialog(data: { taskId: string; taskName: string; params: string }) {
    logDialogData.value = {
      taskId: data.taskId,
      taskName: data.taskName,
      params: data.params,
      logLines: [
        { time: '10:00:00.001', level: 'INFO', msg: `Task started. Reader: mysqlreader → Writer: clickhousewriter. Channel: 3` },
        { time: '10:00:02.340', level: 'INFO', msg: `Reader task initializing. Source: ${data.taskId}` },
        { time: '10:00:05.672', level: 'DEBUG', msg: '[Channel-1] Batch #1 committed, offset=0, latency=12ms' },
        { time: '10:01:18.004', level: 'INFO', msg: 'Reader task completed. Fetched 2,458,391 rows in 1m 15s' },
        { time: '10:02:30.891', level: 'INFO', msg: 'Writer task completed. Inserted 2,458,391 rows.' },
        { time: '10:03:42.100', level: 'INFO', msg: `Task completed successfully. Total: 2,458,391 rows, Duration: 3m 42s, Speed: 17.2 MB/s` },
      ],
    };
    logDialogVisible.value = true;
  }

  function closeLogDialog() {
    logDialogVisible.value = false;
  }

  // --- Highlighted Task ---
  const highlightedTask = ref<HighlightedTask | null>(null);

  function setHighlightedTask(task: HighlightedTask | null) {
    highlightedTask.value = task;
  }

  return {
    sidebarCollapsed,
    activeMenu,
    userInfo,
    menuItems,
    toggleSidebar,
    setActiveMenu,
    logDialogVisible,
    logDialogData,
    openLogDialog,
    closeLogDialog,
    highlightedTask,
    setHighlightedTask,
  };
});
