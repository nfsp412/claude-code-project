export interface MenuItem {
  key: string;
  label: string;
  icon: string;
  path?: string;
  children?: MenuItem[];
}

export interface UserInfo {
  name: string;
  hdfsAccount: string;
  avatar?: string;
}

export interface MetricData {
  title: string;
  value: number | string;
  change: number;
  changeLabel: string;
  icon: string;
  color: 'accent' | 'success' | 'warning' | 'danger';
}

export interface TaskRecord {
  id: string;
  name: string;
  status: 'running' | 'success' | 'failed' | 'pending';
  duration: string;
  startTime: string;
  dataSource: string;
  user: string;
  group: string;
  scheduled: boolean;
  nodes: ClusterNode[];
}

export interface ClusterNode {
  address: string;
  hostname: string;
  spec: string;
  online: boolean;
}

export interface DataSource {
  id: string;
  type: string;
  name: string;
  remark: string;
  ip: string;
  port: string;
  dbName: string;
  username: string;
  password: string;
  jdbcUrl: string;
  driverClass: string;
}

export interface AppState {
  sidebarCollapsed: boolean;
  activeMenu: string;
  expandedMenus: string[];
  userInfo: UserInfo;
}

export interface LogLine {
  time: string;
  level: string;
  msg: string;
}

export interface HighlightedTask {
  id: string;
  name: string;
}
