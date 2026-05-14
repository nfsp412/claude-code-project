<template>
  <div class="flex flex-col h-full">
    <!-- Top Search Bar -->
    <div class="bg-dx-card border-b border-dx-border px-5 py-3 flex items-center gap-3 flex-shrink-0">
      <h1 class="text-lg font-semibold text-dx-text-primary mr-2">节点画布</h1>
      <div class="flex-1 max-w-md flex items-center gap-2 bg-dx-input border border-dx-border rounded-md px-3 py-1.5">
        <span class="text-xs text-dx-text-muted whitespace-nowrap">Task ID:</span>
        <input
          v-model="searchTaskId"
          type="text"
          placeholder="输入Task ID搜索..."
          class="flex-1 bg-transparent border-none outline-none text-sm text-dx-text-primary placeholder:text-dx-text-muted/50"
          @keyup.enter="handleSearch"
        />
      </div>
      <button
        class="inline-flex items-center gap-1 px-3 py-1.5 rounded-md bg-dx-accent text-white text-xs font-medium hover:bg-cyan-500 transition-colors"
        @click="handleSearch"
      >
        搜索
      </button>
      <button
        class="inline-flex items-center gap-1 px-3 py-1.5 rounded-md bg-dx-card text-dx-text-muted border border-dx-border text-xs font-medium hover:text-dx-text-primary transition-colors"
        @click="handleReset"
      >
        重置
      </button>
    </div>

    <!-- Main Content -->
    <div class="flex flex-1 overflow-hidden">
      <!-- Left: Toolbar -->
      <div class="bg-dx-sidebar border-r border-dx-border p-3 flex flex-col gap-1.5 w-12 items-center flex-shrink-0">
        <button
          class="w-8 h-8 rounded-md flex items-center justify-center hover:bg-dx-card-hover transition-colors"
          :class="linkingMode ? 'text-dx-text-muted' : 'text-dx-text-muted hover:text-dx-accent'"
          title="新增Task"
          @click="addTask"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
        </button>
        <button
          class="w-8 h-8 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-success transition-colors"
          title="上线Task"
          @click="onlineTask"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7"/></svg>
        </button>
        <button
          class="w-8 h-8 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-warning transition-colors"
          title="下线Task"
          @click="offlineTask"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 12H5M12 19l-7-7 7-7"/></svg>
        </button>
        <button
          class="w-8 h-8 rounded-md flex items-center justify-center text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-danger transition-colors"
          title="删除Task"
          @click="deleteTask"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
        </button>
        <div class="flex-1"></div>
        <button
          class="w-8 h-8 rounded-md flex items-center justify-center transition-colors"
          :class="linkingMode ? 'bg-dx-accent text-white' : 'text-dx-text-muted hover:bg-dx-card-hover hover:text-dx-accent'"
          title="连线模式"
          @click="toggleLinkingMode"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
        </button>
      </div>

      <!-- Center: Canvas -->
      <div
        ref="canvasContainer"
        class="flex-1 relative overflow-auto bg-dx-page"
        :style="{ backgroundImage: `radial-gradient(circle, #1E293B 1px, transparent 1px)`, backgroundSize: '24px 24px' }"
        @click.self="deselectNode"
        @dragover.prevent
        @drop.prevent="onCanvasDrop"
      >
        <svg class="absolute inset-0 pointer-events-none" :style="{ width: canvasWidth + 'px', height: canvasHeight + 'px', minWidth: '100%', minHeight: '100%' }">
          <defs>
            <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0, 8 3, 0 6" fill="#334155" />
            </marker>
          </defs>
          <line
            v-for="edge in edges"
            :key="edge.id"
            :x1="edge.x1"
            :y1="edge.y1"
            :x2="edge.x2"
            :y2="edge.y2"
            class="connector-line"
            stroke="#334155"
            stroke-width="1.5"
            marker-end="url(#arrowhead)"
          />
        </svg>

        <div :style="{ position: 'relative', width: canvasWidth + 'px', height: canvasHeight + 'px' }">
          <div
            v-for="node in filteredNodes"
            :key="node.id"
            class="task-node"
            :class="{
              'task-node-running': node.status === 'running',
              'task-node-pending': node.status === 'pending',
              'task-node-failed': node.status === 'failed',
              'task-node-success': node.status === 'success',
              'task-node-offline': node.status === 'offline',
              'task-node-selected': selectedNodeId === node.id,
              'task-node-link-target': linkingMode && selectedNodeId && selectedNodeId !== node.id,
            }"
            :style="{ left: node.x + 'px', top: node.y + 'px' }"
            draggable="true"
            @click.stop="selectNode(node.id)"
            @dragstart="onDragStart($event, node.id)"
            @dragend="onDragEnd"
          >
            <div class="text-xs text-dx-text-muted">Task ID: {{ node.id }}</div>
            <div class="text-sm font-medium text-dx-text-primary mt-0.5">{{ node.name }}</div>
            <div class="flex items-center gap-1.5 mt-2">
              <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(node.status)"></span>
              <span class="text-2xs" :class="statusTextClass(node.status)">{{ statusLabel(node.status) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Info Panel -->
      <div class="w-72 bg-dx-card border-l border-dx-border flex-shrink-0 overflow-y-auto flex flex-col">
        <div class="p-4 border-b border-dx-border">
          <h3 class="text-sm font-semibold text-dx-text-primary">画布信息</h3>
        </div>
        <div class="p-4 flex flex-col gap-4 flex-1">
          <div class="flex flex-col gap-1">
            <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">名称</label>
            <input
              v-model="canvasInfo.name"
              class="text-sm text-dx-text-primary bg-dx-input border border-dx-border rounded px-2 py-1 focus:outline-none focus:border-dx-accent"
            />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">描述信息</label>
            <textarea
              v-model="canvasInfo.description"
              rows="3"
              class="text-sm text-dx-text-secondary bg-dx-input border border-dx-border rounded px-2 py-1 resize-none focus:outline-none focus:border-dx-accent"
            ></textarea>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">画布 ID</label>
            <div class="text-sm text-dx-text-primary font-mono">{{ canvasInfo.canvasId }}</div>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">所属用户</label>
            <div class="text-sm text-dx-text-primary">{{ canvasInfo.owner }}</div>
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-2xs font-medium text-dx-text-muted uppercase tracking-wide">所属用户组</label>
            <div class="text-sm text-dx-text-primary">{{ canvasInfo.group }}</div>
          </div>

          <div class="border-t border-dx-border pt-4 mt-2">
            <h4 class="text-xs font-semibold text-dx-text-primary mb-2">统计</h4>
            <div class="flex flex-col gap-2">
              <div class="flex justify-between text-xs">
                <span class="text-dx-text-muted">总Task数</span>
                <span class="text-dx-text-primary font-mono">{{ nodes.length }}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="text-dx-text-muted">运行中</span>
                <span class="text-dx-success font-mono">{{ nodes.filter(n => n.status === 'running').length }}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="text-dx-text-muted">等待中</span>
                <span class="text-dx-warning font-mono">{{ nodes.filter(n => n.status === 'pending').length }}</span>
              </div>
              <div class="flex justify-between text-xs">
                <span class="text-dx-text-muted">已失败</span>
                <span class="text-dx-danger font-mono">{{ nodes.filter(n => n.status === 'failed').length }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Linking Mode Banner -->
    <div
      v-if="linkingMode"
      class="fixed bottom-4 left-1/2 -translate-x-1/2 bg-dx-accent text-white text-sm px-4 py-2 rounded-lg shadow-lg z-50"
    >
      连线模式：点击一个节点选择上游，再点击另一个节点建立依赖关系
      <button class="ml-3 underline" @click="toggleLinkingMode">退出</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue';
import type { TaskCanvasNode, CanvasInfo } from '@/types';

const canvasContainer = ref<HTMLElement | null>(null);
const canvasWidth = ref(1200);
const canvasHeight = ref(800);

// Search
const searchTaskId = ref('');

// Nodes
const nodeIdCounter = ref(5);

function generateId(): string {
  return `DX-${String(nodeIdCounter.value++).padStart(3, '0')}`;
}

const nodes = ref<TaskCanvasNode[]>([
  { id: 'DX-001', name: '数据同步主任务', status: 'running', x: 340, y: 60, upstreamIds: ['DX-002', 'DX-003', 'DX-004'] },
  { id: 'DX-002', name: 'MySQL数据抽取', status: 'running', x: 120, y: 260, upstreamIds: [] },
  { id: 'DX-003', name: '数据清洗转换', status: 'pending', x: 340, y: 260, upstreamIds: [] },
  { id: 'DX-004', name: 'ClickHouse写入', status: 'failed', x: 560, y: 260, upstreamIds: [] },
]);

// Canvas Info
const canvasInfo = ref<CanvasInfo>({
  name: '数据同步流程图',
  description: '展示MySQL到ClickHouse的数据同步流程，包含数据抽取、清洗和写入三个关键步骤',
  canvasId: 'CANVAS-DX-20240515-001',
  owner: '张工',
  group: '数据平台组',
});

// Selection & Linking
const selectedNodeId = ref<string | null>(null);
const linkingMode = ref(false);
const linkSourceId = ref<string | null>(null);

// Drag state
const dragNodeId = ref<string | null>(null);
const dragOffset = ref({ x: 0, y: 0 });

const filteredNodes = computed(() => {
  if (!searchTaskId.value.trim()) return nodes.value;
  const keyword = searchTaskId.value.trim().toLowerCase();
  return nodes.value.filter(n => n.id.toLowerCase().includes(keyword) || n.name.toLowerCase().includes(keyword));
});

// Edges: lines from each upstream node to its downstream
interface Edge {
  id: string;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

const edges = computed<Edge[]>(() => {
  const result: Edge[] = [];
  for (const node of nodes.value) {
    for (const upstreamId of node.upstreamIds) {
      const upstream = nodes.value.find(n => n.id === upstreamId);
      if (upstream) {
        result.push({
          id: `${upstream.id}-${node.id}`,
          x1: upstream.x + 80,
          y1: upstream.y + 60,
          x2: node.x + 80,
          y2: node.y,
        });
      }
    }
  }
  return result;
});

// Status helpers
function statusDotClass(status: string) {
  return {
    running: 'bg-dx-success',
    pending: 'bg-dx-warning',
    failed: 'bg-dx-danger',
    success: 'bg-dx-success',
    offline: 'bg-dx-text-muted',
  }[status] || 'bg-dx-text-muted';
}

function statusTextClass(status: string) {
  return {
    running: 'text-dx-success',
    pending: 'text-dx-warning',
    failed: 'text-dx-danger',
    success: 'text-dx-success',
    offline: 'text-dx-text-muted',
  }[status] || 'text-dx-text-muted';
}

function statusLabel(status: string) {
  return {
    running: '运行中',
    pending: '等待上游',
    failed: '失败',
    success: '已完成',
    offline: '已下线',
  }[status] || status;
}

// Node selection
function selectNode(id: string) {
  if (linkingMode.value) {
    if (!linkSourceId.value) {
      linkSourceId.value = id;
      selectedNodeId.value = id;
    } else if (linkSourceId.value !== id) {
      // Create dependency: linkSource is upstream of target
      const target = nodes.value.find(n => n.id === id);
      if (target && !target.upstreamIds.includes(linkSourceId.value)) {
        target.upstreamIds.push(linkSourceId.value);
      }
      linkSourceId.value = null;
      selectedNodeId.value = null;
      linkingMode.value = false;
    }
    return;
  }
  selectedNodeId.value = id;
}

function deselectNode() {
  if (linkingMode.value) return;
  selectedNodeId.value = null;
}

function toggleLinkingMode() {
  linkingMode.value = !linkingMode.value;
  linkSourceId.value = null;
  selectedNodeId.value = null;
}

// Search
function handleSearch() {
  // Filtering is done via computed, this triggers reactivity
}

function handleReset() {
  searchTaskId.value = '';
}

// Task operations
function addTask() {
  const id = generateId();
  nodes.value.push({
    id,
    name: `新任务 ${id}`,
    status: 'pending',
    x: 100 + Math.random() * 400,
    y: 100 + Math.random() * 400,
    upstreamIds: [],
  });
}

function onlineTask() {
  if (!selectedNodeId.value) return;
  const node = nodes.value.find(n => n.id === selectedNodeId.value);
  if (node) node.status = 'running';
}

function offlineTask() {
  if (!selectedNodeId.value) return;
  const node = nodes.value.find(n => n.id === selectedNodeId.value);
  if (node) node.status = 'offline';
}

function deleteTask() {
  if (!selectedNodeId.value) return;
  const id = selectedNodeId.value;
  // Remove this node from all upstream lists
  for (const node of nodes.value) {
    node.upstreamIds = node.upstreamIds.filter(uid => uid !== id);
  }
  nodes.value = nodes.value.filter(n => n.id !== id);
  selectedNodeId.value = null;
}

// Drag & drop
function onDragStart(e: DragEvent, nodeId: string) {
  if (linkingMode.value) return;
  dragNodeId.value = nodeId;
  const node = nodes.value.find(n => n.id === nodeId);
  if (node && e.target instanceof HTMLElement) {
    const el = e.target.closest('.task-node') as HTMLElement;
    if (el) {
      dragOffset.value = {
        x: e.clientX - el.getBoundingClientRect().left,
        y: e.clientY - el.getBoundingClientRect().top,
      };
    }
  }
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', nodeId);
  }
}

function onDragEnd() {
  dragNodeId.value = null;
}

function onCanvasDrop(e: DragEvent) {
  const nodeId = dragNodeId.value;
  if (!nodeId || !canvasContainer.value) return;

  const containerRect = canvasContainer.value.getBoundingClientRect();
  const scrollLeft = canvasContainer.value.scrollLeft;
  const scrollTop = canvasContainer.value.scrollTop;

  const node = nodes.value.find(n => n.id === nodeId);
  if (node) {
    node.x = e.clientX - containerRect.left + scrollLeft - dragOffset.value.x;
    node.y = e.clientY - containerRect.top + scrollTop - dragOffset.value.y;
  }
}

onMounted(() => {
  nextTick(() => {
    if (canvasContainer.value) {
      canvasWidth.value = Math.max(canvasContainer.value.clientWidth, 1200);
      canvasHeight.value = Math.max(canvasContainer.value.clientHeight, 800);
    }
  });
});
</script>

<style scoped>
.task-node {
  position: absolute;
  min-width: 160px;
  background: #1A2236;
  border: 1.5px solid #1E293B;
  border-radius: 8px;
  padding: 12px 14px;
  cursor: grab;
  transition: box-shadow 0.15s, border-color 0.15s;
  user-select: none;
  z-index: 10;
}
.task-node:hover {
  border-color: #06B6D4;
  box-shadow: 0 0 12px rgba(6, 182, 212, 0.15);
}
.task-node-selected {
  border-color: #06B6D4;
  box-shadow: 0 0 16px rgba(6, 182, 212, 0.25);
}
.task-node-link-target {
  border-color: #3B82F6;
  cursor: crosshair;
}
.task-node-link-target:hover {
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.25);
}
.task-node-running {
  border-left: 3px solid #10B981;
}
.task-node-pending {
  border-left: 3px solid #F59E0B;
}
.task-node-failed {
  border-left: 3px solid #EF4444;
}
.task-node-success {
  border-left: 3px solid #10B981;
}
.task-node-offline {
  border-left: 3px solid #64748B;
  opacity: 0.6;
}

.connector-line {
  pointer-events: none;
}
</style>
