<template>
  <div class="p-6 flex flex-col gap-4">
    <!-- Breadcrumb + Title -->
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
        </svg>
        <span>/</span><span class="text-dx-accent">数据源管理</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">数据源管理</h1>
    </div>

    <!-- Tool Bar -->
    <div class="flex items-center gap-3">
      <div class="relative flex-1 max-w-sm">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索数据源名称 / JDBC 链接..."
          class="w-full h-9 pl-9 pr-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors"
          @keyup.enter="handleSearch"
        />
        <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-dx-text-muted" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" d="M21 21l-4.3-4.3"/></svg>
      </div>
      <button class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5" @click="handleSearch">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" d="M21 21l-4.3-4.3"/></svg>
        搜索
      </button>
      <button class="h-9 px-4 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5 ml-auto" @click="openDrawer('add')">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" d="M12 5v14M5 12h14"/></svg>
        添加数据源
      </button>
    </div>

    <!-- Data Table -->
    <div class="bg-dx-card border border-dx-border rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-dx-input border-b border-dx-border">
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">数据源类型</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">数据源名称</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">备注信息</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap max-w-[220px]">JDBC 链接</th>
              <th class="text-left py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap">JDBC 驱动全类名</th>
              <th class="text-right py-3 px-4 text-xs font-medium text-dx-text-muted uppercase tracking-wide whitespace-nowrap w-[100px]">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredList.length === 0">
              <td colspan="6" class="py-12 text-center text-sm text-dx-text-muted">暂无数据源</td>
            </tr>
            <tr
              v-for="ds in filteredList"
              :key="ds.id"
              class="border-b border-dx-border/50 hover:bg-dx-card-hover transition-colors"
            >
              <td class="py-3 px-4">
                <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium" :class="typeBadgeClass(ds.type)">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7M4 7c0-2 1-3 3-3h10c2 0 3 1 3 3M4 7h16M9 21v-6H6m12 0h-3v6"/></svg>
                  {{ ds.type }}
                </span>
              </td>
              <td class="py-3 px-4 text-dx-text-primary font-medium whitespace-nowrap">{{ ds.name }}</td>
              <td class="py-3 px-4 text-xs text-dx-text-secondary max-w-[140px] truncate">{{ ds.remark }}</td>
              <td class="py-3 px-4 font-mono text-xs text-dx-text-secondary max-w-[220px] truncate" :title="ds.jdbcUrl">{{ ds.jdbcUrl }}</td>
              <td class="py-3 px-4 font-mono text-xs text-dx-text-muted whitespace-nowrap">{{ ds.driverClass }}</td>
              <td class="py-3 px-4 text-right">
                <div class="flex items-center justify-end gap-1">
                  <button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-accent transition-colors" @click="openDrawer('edit', ds)">编辑</button>
                  <button class="px-2.5 py-1.5 rounded text-xs text-dx-text-secondary hover:bg-red-500/10 hover:text-dx-danger transition-colors" @click="handleDelete(ds)">删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="flex items-center justify-between px-4 py-3 border-t border-dx-border bg-dx-card-hover/30">
        <span class="text-xs text-dx-text-muted">共 {{ filteredList.length }} 条数据源</span>
      </div>
    </div>

    <!-- Drawer Overlay -->
    <Teleport to="body">
      <Transition name="drawer">
        <div v-if="drawerVisible" class="fixed inset-0 z-[100]">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/50" @click="closeDrawer" />
          <!-- Panel -->
          <div class="drawer-panel absolute top-0 right-0 h-full bg-dx-card border-l border-dx-border shadow-2xl flex flex-col" style="width: 560px;">
          <!-- Header -->
          <div class="flex-shrink-0 flex items-center justify-between px-6 py-4 border-b border-dx-border">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-dx-accent/10 flex items-center justify-center">
                <svg class="w-4 h-4 text-dx-accent" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7M4 7c0-2 1-3 3-3h10c2 0 3 1 3 3M4 7h16M9 21v-6H6m12 0h-3v6"/></svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-dx-text-primary">{{ isEditing ? '编辑数据源' : '添加数据源' }}</h2>
                <p class="text-xs text-dx-text-muted">{{ isEditing ? '修改数据源连接信息' : '配置新的数据源连接信息' }}</p>
              </div>
            </div>
            <button class="w-7 h-7 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors" @click="closeDrawer">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <!-- Body (scrollable) -->
          <div class="flex-1 overflow-y-auto px-6 py-5" style="min-height: 0;">
            <div class="flex flex-col gap-4">
              <!-- 数据源类型 -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-medium text-dx-text-secondary">数据源类型 <span class="text-red-400">*</span></label>
                <select v-model="form.type" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary focus:outline-none focus:border-dx-accent transition-colors" @change="autoFillJdbc">
                  <option value="" disabled>请选择数据源类型</option>
                  <option v-for="opt in dsTypes" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
              </div>

              <!-- 数据源名称 -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-medium text-dx-text-secondary">数据源名称 <span class="text-red-400">*</span></label>
                <input v-model="form.name" type="text" placeholder="例如: 生产订单数据库" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" />
              </div>

              <!-- IP + Port -->
              <div class="grid grid-cols-2 gap-4">
                <div class="flex flex-col gap-1.5">
                  <label class="text-xs font-medium text-dx-text-secondary">IP <span class="text-red-400">*</span></label>
                  <input v-model="form.ip" type="text" placeholder="例如: 10.23.45.101" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" @input="autoFillJdbc" />
                </div>
                <div class="flex flex-col gap-1.5">
                  <label class="text-xs font-medium text-dx-text-secondary">端口 <span class="text-red-400">*</span></label>
                  <input v-model="form.port" type="text" placeholder="例如: 3306" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" @input="autoFillJdbc" />
                </div>
              </div>

              <!-- 数据库名称 + 用户名 -->
              <div class="grid grid-cols-2 gap-4">
                <div class="flex flex-col gap-1.5">
                  <label class="text-xs font-medium text-dx-text-secondary">数据库名称 <span class="text-red-400">*</span></label>
                  <input v-model="form.dbName" type="text" placeholder="例如: orders_db" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" @input="autoFillJdbc" />
                </div>
                <div class="flex flex-col gap-1.5">
                  <label class="text-xs font-medium text-dx-text-secondary">用户名 <span class="text-red-400">*</span></label>
                  <input v-model="form.username" type="text" placeholder="例如: datax_reader" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" />
                </div>
              </div>

              <!-- 密码 -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-medium text-dx-text-secondary">密码 <span class="text-red-400">*</span></label>
                <div class="relative">
                  <input v-model="form.password" :type="showPassword ? 'text' : 'password'" placeholder="请输入密码" class="w-full h-9 px-3 pr-9 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" />
                  <button class="absolute right-2 top-1/2 -translate-y-1/2 text-dx-text-muted hover:text-dx-text-secondary transition-colors" @click="showPassword = !showPassword">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                  </button>
                </div>
              </div>

              <!-- Divider -->
              <div class="border-t border-dx-border my-1" />

              <!-- JDBC URL -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-medium text-dx-text-secondary">
                  JDBC URL 链接
                  <span class="text-2xs text-dx-text-muted font-normal ml-1">— 根据上方信息自动生成，可手动修改</span>
                </label>
                <input v-model="form.jdbcUrl" type="text" placeholder="选择数据源类型并填写 IP/端口/库名后自动生成" class="w-full h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" />
              </div>

              <!-- JDBC 驱动全类名 -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-medium text-dx-text-secondary">
                  JDBC 驱动全类名
                  <span class="text-2xs text-dx-text-muted font-normal ml-1">— 根据数据源类型自动填充，可手动修改</span>
                </label>
                <input v-model="form.driverClass" type="text" placeholder="选择数据源类型后自动填充" class="w-full h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" />
              </div>

              <!-- 注释 -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-medium text-dx-text-secondary">注释 <span class="text-dx-text-muted">(选填)</span></label>
                <textarea v-model="form.remark" rows="3" placeholder="备注信息，如数据源用途、负责人等" class="w-full px-3 py-2 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors resize-none" />
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="flex-shrink-0 flex items-center justify-between px-6 py-4 border-t border-dx-border bg-dx-card-hover/30">
            <button
              class="h-9 px-4 rounded-md border border-dx-border text-sm transition-colors flex items-center gap-1.5"
              :class="testing ? 'text-dx-success border-dx-success' : 'text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary'"
              :disabled="testing"
              @click="testConnection"
            >
              <svg v-if="testing" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
              <svg v-else-if="testResult === 'success'" class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              {{ testing ? '测试中...' : testResult === 'success' ? '连接成功' : '测试连接' }}
            </button>
            <div class="flex items-center gap-3">
              <button class="h-9 px-5 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors" @click="closeDrawer">取消</button>
              <button class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors" @click="handleConfirm">确认</button>
            </div>
          </div>
        </div>
      </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import type { DataSource } from '@/types';

// --- Mock data ---
const list = ref<DataSource[]>([
  { id: '1', type: 'MySQL', name: '生产订单数据库', remark: '线上订单主库，只读副本', ip: '10.23.45.101', port: '3306', dbName: 'orders_db', username: 'datax_reader', password: '***', jdbcUrl: 'jdbc:mysql://10.23.45.101:3306/orders_db?useSSL=false', driverClass: 'com.mysql.cj.jdbc.Driver' },
  { id: '2', type: 'PostgreSQL', name: '数据仓库 PG', remark: '离线数据仓库实例', ip: '10.23.45.201', port: '5432', dbName: 'dw_analytics', username: 'datax_etl', password: '***', jdbcUrl: 'jdbc:postgresql://10.23.45.201:5432/dw_analytics', driverClass: 'org.postgresql.Driver' },
  { id: '3', type: 'ClickHouse', name: '广告投放分析库', remark: '实时广告数据 OLAP', ip: '10.23.45.202', port: '8123', dbName: 'ad_analytics', username: 'default', password: '***', jdbcUrl: 'jdbc:clickhouse://10.23.45.202:8123/ad_analytics', driverClass: 'ru.yandex.clickhouse.ClickHouseDriver' },
  { id: '4', type: 'Hive', name: '用户画像 Hive 库', remark: '用户标签和画像数据', ip: '10.23.45.103', port: '10000', dbName: 'user_profile', username: 'hive_etl', password: '***', jdbcUrl: 'jdbc:hive2://10.23.45.103:10000/user_profile', driverClass: 'org.apache.hive.jdbc.HiveDriver' },
  { id: '5', type: 'Oracle', name: '财务系统 Oracle', remark: '财务核心数据库', ip: '10.23.45.104', port: '1521', dbName: 'fin', username: 'fin_reader', password: '***', jdbcUrl: 'jdbc:oracle:thin:@10.23.45.104:1521:fin', driverClass: 'oracle.jdbc.OracleDriver' },
]);

// --- Search ---
const searchQuery = ref('');
function handleSearch() { /* filters via computed */ }
const filteredList = computed(() => {
  if (!searchQuery.value) return list.value;
  const q = searchQuery.value.toLowerCase();
  return list.value.filter((d) => d.name.toLowerCase().includes(q) || d.jdbcUrl.toLowerCase().includes(q));
});

// --- Drawer ---
const drawerVisible = ref(false);
const isEditing = ref(false);
const editingId = ref<string | null>(null);
const showPassword = ref(false);

const dsTypes = [
  { value: 'mysql', label: 'MySQL' },
  { value: 'postgresql', label: 'PostgreSQL' },
  { value: 'clickhouse', label: 'ClickHouse' },
  { value: 'hive', label: 'Hive / Spark SQL' },
  { value: 'oracle', label: 'Oracle' },
  { value: 'sqlserver', label: 'SQL Server' },
];

const jdbcConfig: Record<string, { url: string; driver: string; defaultPort: string }> = {
  mysql:      { url: 'jdbc:mysql://{ip}:{port}/{db}?useSSL=false&serverTimezone=Asia/Shanghai', driver: 'com.mysql.cj.jdbc.Driver', defaultPort: '3306' },
  postgresql: { url: 'jdbc:postgresql://{ip}:{port}/{db}', driver: 'org.postgresql.Driver', defaultPort: '5432' },
  clickhouse: { url: 'jdbc:clickhouse://{ip}:{port}/{db}', driver: 'ru.yandex.clickhouse.ClickHouseDriver', defaultPort: '8123' },
  hive:       { url: 'jdbc:hive2://{ip}:{port}/{db}', driver: 'org.apache.hive.jdbc.HiveDriver', defaultPort: '10000' },
  oracle:     { url: 'jdbc:oracle:thin:@{ip}:{port}:{db}', driver: 'oracle.jdbc.OracleDriver', defaultPort: '1521' },
  sqlserver:  { url: 'jdbc:sqlserver://{ip}:{port};databaseName={db}', driver: 'com.microsoft.sqlserver.jdbc.SQLServerDriver', defaultPort: '1433' },
};

const emptyForm = (): DataSource => ({
  id: '', type: '', name: '', remark: '', ip: '', port: '', dbName: '', username: '', password: '', jdbcUrl: '', driverClass: '',
});

const form = reactive<DataSource>(emptyForm());

function openDrawer(mode: 'add' | 'edit', ds?: DataSource) {
  drawerVisible.value = true;
  if (mode === 'edit' && ds) {
    isEditing.value = true;
    editingId.value = ds.id;
    Object.assign(form, { ...ds });
  } else {
    isEditing.value = false;
    editingId.value = null;
    Object.assign(form, emptyForm());
  }
  showPassword.value = false;
  testResult.value = null;
}

function closeDrawer() {
  drawerVisible.value = false;
}

function autoFillJdbc() {
  const cfg = jdbcConfig[form.type];
  if (!cfg) return;
  if (!form.port) form.port = cfg.defaultPort;
  const ip = form.ip || '{ip}';
  const port = form.port || cfg.defaultPort;
  const db = form.dbName || '{db}';
  form.jdbcUrl = cfg.url.replace('{ip}', ip).replace('{port}', port).replace('{db}', db);
  form.driverClass = cfg.driver;
}

// --- Test connection ---
const testing = ref(false);
const testResult = ref<'success' | null>(null);
function testConnection() {
  testing.value = true;
  testResult.value = null;
  setTimeout(() => {
    testing.value = false;
    testResult.value = 'success';
    setTimeout(() => { testResult.value = null; }, 2500);
  }, 1500);
}

// --- CRUD ---
function handleConfirm() {
  if (!form.name || !form.type || !form.ip || !form.port || !form.dbName || !form.username || !form.password) return;
  if (isEditing.value && editingId.value) {
    const idx = list.value.findIndex((d) => d.id === editingId.value);
    if (idx > -1) list.value[idx] = { ...form, id: editingId.value };
  } else {
    const id = String(Date.now());
    list.value.push({ ...form, id });
  }
  closeDrawer();
}

function handleDelete(ds: DataSource) {
  list.value = list.value.filter((d) => d.id !== ds.id);
}

// --- Helpers ---
function typeBadgeClass(type: string) {
  const m: Record<string, string> = {
    MySQL: 'bg-cyan-500/10 text-cyan-400', PostgreSQL: 'bg-blue-500/10 text-blue-400',
    ClickHouse: 'bg-amber-500/10 text-amber-400', Hive: 'bg-purple-500/10 text-purple-400',
    Oracle: 'bg-emerald-500/10 text-emerald-400', 'SQL Server': 'bg-red-500/10 text-red-400',
  };
  return m[type] ?? 'bg-dx-input text-dx-text-secondary';
}
</script>

<style scoped>
/* === Drawer transition === */

/* Overlay: opacity fade */
.drawer-enter-active {
  transition: opacity 0.35s cubic-bezier(0.22, 0.61, 0.36, 1);
}
.drawer-leave-active {
  transition: opacity 0.25s cubic-bezier(0.55, 0, 1, 0.45);
}
.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

/* Panel: translateX slide + shadow */
.drawer-enter-active .drawer-panel,
.drawer-leave-active .drawer-panel {
  transition:
    transform 0.35s cubic-bezier(0.22, 0.61, 0.36, 1),
    box-shadow 0.35s ease;
  will-change: transform;
}
.drawer-enter-from .drawer-panel {
  transform: translateX(100%);
  box-shadow: none;
}
.drawer-leave-to .drawer-panel {
  transform: translateX(100%);
  box-shadow: none;
}
.drawer-enter-to .drawer-panel,
.drawer-leave-from .drawer-panel {
  transform: translateX(0);
}
</style>
