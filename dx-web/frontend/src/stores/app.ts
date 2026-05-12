import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { MenuItem, UserInfo } from '@/types';

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false);
  const activeMenu = ref('dashboard');
  const expandedMenus = ref<string[]>(['task-management']);
  const userInfo = ref<UserInfo>({
    name: '张工',
    hdfsAccount: 'hdfs://prod-cluster-nj-01',
  });

  const menuItems = ref<MenuItem[]>([
    { key: 'dashboard', label: '任务监控仪表盘', icon: 'LayoutDashboard', path: '/' },
    {
      key: 'task-management',
      label: '任务管理',
      icon: 'ListChecks',
      children: [
        { key: 'task-list', label: '任务明细列表', icon: 'List', path: '/tasks/list' },
        { key: 'task-builder', label: '任务构建', icon: 'Hammer', path: '/tasks/builder' },
      ],
    },
    { key: 'schedule', label: '调度管理', icon: 'Clock', path: '/schedule' },
    { key: 'datasource', label: '数据源管理', icon: 'Database', path: '/datasource' },
    { key: 'logs', label: '日志查询', icon: 'FileSearch', path: '/logs' },
    { key: 'cluster', label: 'DataX执行集群管理', icon: 'Server', path: '/cluster' },
    { key: 'resource', label: '资源使用监控', icon: 'Activity', path: '/resource' },
    { key: 'json-tool', label: 'JSON格式化', icon: 'Braces', path: '/json-tool' },
  ]);

  const isMenuExpanded = computed(() => (key: string) => expandedMenus.value.includes(key));

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value;
  }

  function setActiveMenu(key: string) {
    activeMenu.value = key;
  }

  function toggleMenuExpand(key: string) {
    const idx = expandedMenus.value.indexOf(key);
    if (idx > -1) {
      expandedMenus.value.splice(idx, 1);
    } else {
      expandedMenus.value.push(key);
    }
  }

  return {
    sidebarCollapsed,
    activeMenu,
    expandedMenus,
    userInfo,
    menuItems,
    isMenuExpanded,
    toggleSidebar,
    setActiveMenu,
    toggleMenuExpand,
  };
});
