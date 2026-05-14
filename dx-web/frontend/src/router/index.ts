import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { title: '任务监控仪表盘' },
  },
  {
    path: '/tasks/list',
    name: 'task-list',
    component: () => import('@/views/TaskListView.vue'),
    meta: { title: '任务列表' },
  },
  {
    path: '/tasks/builder',
    name: 'task-builder',
    component: () => import('@/views/TaskBuilderView.vue'),
    meta: { title: '任务构建' },
  },
  {
    path: '/schedule',
    name: 'schedule-config',
    component: () => import('@/views/ScheduleView.vue'),
    meta: { title: '任务调度' },
  },
  {
    path: '/schedule/run-detail',
    name: 'schedule-run-detail',
    component: () => import('@/views/TaskRunDetailView.vue'),
    meta: { title: '任务运行明细' },
  },
  {
    path: '/datasource',
    name: 'datasource',
    component: () => import('@/views/DataSourceView.vue'),
    meta: { title: '数据源管理' },
  },
  {
    path: '/logs',
    name: 'logs',
    component: () => import('@/views/LogQueryView.vue'),
    meta: { title: '日志查询' },
  },
  {
    path: '/cluster',
    name: 'cluster',
    component: () => import('@/views/ClusterView.vue'),
    meta: { title: 'DataX执行集群管理' },
  },
  {
    path: '/resource',
    name: 'resource',
    component: () => import('@/views/ResourceView.vue'),
    meta: { title: '资源使用监控' },
  },
  {
    path: '/json-tool',
    name: 'json-tool',
    component: () => import('@/views/JsonToolView.vue'),
    meta: { title: 'JSON格式化' },
  },
  {
    path: '/task-canvas',
    name: 'task-canvas',
    component: () => import('@/views/TaskCanvasView.vue'),
    meta: { title: '节点画布' },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  document.title = `${to.meta.title} - DataX 监控调度平台`;
});

export default router;
