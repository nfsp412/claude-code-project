<template>
  <div class="p-6 flex flex-col gap-4">
    <!-- Breadcrumb + Title -->
    <div class="flex flex-col gap-1">
      <div class="flex items-center gap-2 text-xs text-dx-text-muted">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
        </svg>
        <span>/</span><span class="text-dx-text-muted">任务管理</span><span>/</span><span class="text-dx-accent">任务构建</span>
      </div>
      <h1 class="text-xl font-bold text-dx-text-primary">任务构建</h1>
    </div>

    <!-- Step Progress Bar -->
    <div class="bg-dx-card border border-dx-border rounded-lg p-6">
      <div class="flex items-center px-5">
        <div v-for="(step, idx) in steps" :key="step.key" class="flex items-center flex-1 last:flex-[0]">
          <div class="flex flex-col items-center gap-2 flex-shrink-0">
            <div
              class="w-7 h-7 rounded-full flex items-center justify-center text-[13px] font-semibold border-2 transition-all duration-300"
              :class="stepCircleClass(idx)"
            >
              <svg v-if="idx < currentStep" class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
              </svg>
              <span v-else>{{ idx + 1 }}</span>
            </div>
            <span
              class="text-[11px] font-medium whitespace-nowrap leading-tight transition-colors duration-300"
              :class="stepLabelClass(idx)"
            >{{ step.label }}</span>
          </div>
          <div
            v-if="idx < steps.length - 1"
            class="flex-1 h-0.5 mx-2 mb-6 transition-colors duration-300"
            :class="idx < currentStep ? 'bg-dx-accent' : 'bg-dx-border'"
          />
        </div>
      </div>
    </div>

    <!-- Step Content -->
    <div class="bg-dx-card border border-dx-border rounded-lg p-6">
      <!-- ========== STEP 1: Reader ========== -->
      <div v-if="currentStep === 0">
        <div class="flex items-center gap-3 mb-6">
          <div class="w-8 h-8 rounded-lg bg-cyan-500/10 flex items-center justify-center">
            <svg class="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7M4 7c0-2 1-3 3-3h10c2 0 3 1 3 3M4 7h16M9 21v-6H6m12 0h-3v6"/></svg>
          </div>
          <div>
            <h2 class="text-base font-semibold text-dx-text-primary">步骤 1: 构建 Reader</h2>
            <p class="text-xs text-dx-text-muted">配置数据读取源 — 从源数据库读取数据</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-x-6 gap-y-4">
          <!-- 数据库源 -->
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">数据库源 <span class="text-red-400">*</span></label>
            <select v-model="form.reader.source" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary focus:outline-none focus:border-dx-accent transition-colors">
              <option value="" disabled>请选择数据库源</option>
              <option v-for="s in readerSources" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <!-- 数据库表名 -->
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">数据库表名 <span class="text-red-400">*</span></label>
            <select v-model="form.reader.table" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary focus:outline-none focus:border-dx-accent transition-colors">
              <option value="" disabled>请选择数据库表</option>
              <option v-for="t in readerTables" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>
          <!-- SQL语句 -->
          <div class="col-span-2 flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">SQL 语句 <span class="text-dx-text-muted">(选填)</span></label>
            <textarea v-model="form.reader.sql" rows="3" placeholder="请输入自定义查询 SQL, 例如: SELECT * FROM user_behavior_log WHERE dt = '${dt}'" class="w-full px-3 py-2 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors resize-none" />
            <span class="text-2xs text-dx-text-muted">支持 $&#123;变量名&#125; 格式的变量替换</span>
          </div>
          <!-- 切分字段 -->
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">切分字段 <span class="text-dx-text-muted">(选填)</span></label>
            <input v-model="form.reader.splitField" type="text" placeholder="例如: id" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" />
            <span class="text-2xs text-dx-text-muted">用于并行读取的切分键, 建议选择主键或索引字段</span>
          </div>
          <!-- WHERE条件 -->
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">WHERE 条件 <span class="text-dx-text-muted">(选填)</span></label>
            <input v-model="form.reader.where" type="text" placeholder="例如: status = 1 AND is_deleted = 0" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" />
          </div>
        </div>

        <!-- 表字段 -->
        <FieldCheckboxGrid
          side="reader"
          :fields="readerFields"
          :model-value="form.reader.selectedFields"
          @update:model-value="form.reader.selectedFields = $event"
        />
      </div>

      <!-- ========== STEP 2: Writer ========== -->
      <div v-if="currentStep === 1">
        <div class="flex items-center gap-3 mb-6">
          <div class="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center">
            <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7M4 7c0-2 1-3 3-3h10c2 0 3 1 3 3M4 7h16"/></svg>
          </div>
          <div>
            <h2 class="text-base font-semibold text-dx-text-primary">步骤 2: 构建 Writer</h2>
            <p class="text-xs text-dx-text-muted">配置数据写入目标 — 将数据写入目标数据库</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-x-6 gap-y-4">
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">数据库源 <span class="text-red-400">*</span></label>
            <select v-model="form.writer.source" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary focus:outline-none focus:border-dx-accent transition-colors">
              <option value="" disabled>请选择数据库源</option>
              <option v-for="s in writerSources" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">数据库表名 <span class="text-red-400">*</span></label>
            <select v-model="form.writer.table" class="h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary focus:outline-none focus:border-dx-accent transition-colors">
              <option value="" disabled>请选择数据库表</option>
              <option v-for="t in writerTables" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>
          <div class="col-span-2 flex flex-col gap-1.5">
            <label class="text-xs font-medium text-dx-text-secondary">前置 SQL <span class="text-dx-text-muted">(选填)</span></label>
            <textarea v-model="form.writer.preSql" rows="2" placeholder="例如: TRUNCATE TABLE dw_user_behavior_agg" class="w-full px-3 py-2 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary font-mono placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors resize-none" />
            <span class="text-2xs text-dx-text-muted">数据写入前执行的 SQL 语句</span>
          </div>
        </div>

        <FieldCheckboxGrid
          side="writer"
          :fields="writerFields"
          :model-value="form.writer.selectedFields"
          @update:model-value="form.writer.selectedFields = $event"
        />
      </div>

      <!-- ========== STEP 3: Field Mapping ========== -->
      <div v-if="currentStep === 2">
        <div class="flex items-center gap-3 mb-6">
          <div class="w-8 h-8 rounded-lg bg-amber-500/10 flex items-center justify-center">
            <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
          </div>
          <div>
            <h2 class="text-base font-semibold text-dx-text-primary">步骤 3: 字段顺序映射</h2>
            <p class="text-xs text-dx-text-muted">映射 Reader 和 Writer 之间的字段对应关系</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-6">
          <!-- Reader fields -->
          <div class="bg-dx-input border border-dx-border rounded-lg p-4">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <div class="w-6 h-6 rounded bg-cyan-500/10 flex items-center justify-center">
                  <svg class="w-3.5 h-3.5 text-cyan-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7M4 7c0-2 1-3 3-3h10c2 0 3 1 3 3"/></svg>
                </div>
                <h3 class="text-sm font-semibold text-dx-text-primary">Reader 字段</h3>
                <span class="text-2xs text-dx-text-muted">({{ form.reader.table || '未选择表' }})</span>
              </div>
              <label class="flex items-center gap-2 text-xs text-dx-text-muted cursor-pointer select-none">
                <input type="checkbox" class="checkbox-custom" :checked="mappingReaderAll" @change="toggleMappingReaderAll"> 全选
              </label>
            </div>
            <div class="flex flex-col gap-1">
              <div
                v-for="(f, i) in readerFields"
                :key="f.name"
                class="flex items-center gap-2 px-3 py-2 rounded hover:bg-dx-card-hover transition-colors cursor-pointer"
                @click="toggleMappingField('reader', f.name)"
              >
                <span class="text-2xs text-dx-text-muted w-5">{{ i + 1 }}</span>
                <input type="checkbox" class="checkbox-custom" :checked="form.mapping.reader.includes(f.name)" @click.stop @change="toggleMappingField('reader', f.name)" />
                <span class="text-xs text-dx-text-primary">{{ f.name }}</span>
                <span class="text-2xs text-dx-text-muted ml-auto">{{ f.type }}</span>
              </div>
            </div>
          </div>

          <!-- Writer fields -->
          <div class="bg-dx-input border border-dx-border rounded-lg p-4">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <div class="w-6 h-6 rounded bg-purple-500/10 flex items-center justify-center">
                  <svg class="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7"/></svg>
                </div>
                <h3 class="text-sm font-semibold text-dx-text-primary">Writer 字段</h3>
                <span class="text-2xs text-dx-text-muted">({{ form.writer.table || '未选择表' }})</span>
              </div>
              <label class="flex items-center gap-2 text-xs text-dx-text-muted cursor-pointer select-none">
                <input type="checkbox" class="checkbox-custom" :checked="mappingWriterAll" @change="toggleMappingWriterAll"> 全选
              </label>
            </div>
            <div class="flex flex-col gap-1">
              <div
                v-for="(f, i) in writerFields"
                :key="f.name"
                class="flex items-center gap-2 px-3 py-2 rounded hover:bg-dx-card-hover transition-colors cursor-pointer"
                @click="toggleMappingField('writer', f.name)"
              >
                <span class="text-2xs text-dx-text-muted w-5">{{ i + 1 }}</span>
                <input type="checkbox" class="checkbox-custom" :checked="form.mapping.writer.includes(f.name)" @click.stop @change="toggleMappingField('writer', f.name)" />
                <span class="text-xs text-dx-text-primary">{{ f.name }}</span>
                <span class="text-2xs text-dx-text-muted ml-auto">{{ f.type }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========== STEP 4: Build ========== -->
      <div v-if="currentStep === 3">
        <div class="flex items-center gap-3 mb-6">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center">
            <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div>
            <h2 class="text-base font-semibold text-dx-text-primary">步骤 4: 构建完成</h2>
            <p class="text-xs text-dx-text-muted">设置任务名称并生成 DataX 配置 JSON</p>
          </div>
        </div>

        <div class="flex flex-col gap-1.5 mb-4">
          <label class="text-xs font-medium text-dx-text-secondary">任务名称 <span class="text-red-400">*</span></label>
          <input v-model="form.taskName" type="text" placeholder="请输入任务名称" class="w-80 h-9 px-3 rounded-md bg-dx-input border border-dx-border text-sm text-dx-text-primary placeholder:text-dx-text-muted/50 focus:outline-none focus:border-dx-accent transition-colors" />
        </div>

        <button
          class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5 mb-4"
          @click="buildJson"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 3H7a2 2 0 00-2 2v2.5c0 1.5-1 2-1 2s1 .5 1 2V14a2 2 0 002 2h1"/><path d="M16 3h1a2 2 0 012 2v2.5c0 1.5 1 2 1 2s-1 .5-1 2V14a2 2 0 01-2 2h-1"/>
          </svg>
          构建 JSON
        </button>

        <!-- Placeholder -->
        <div v-if="!builtJson" class="bg-dx-input border border-dx-border border-dashed rounded-lg p-10 flex flex-col items-center justify-center text-center">
          <svg class="w-10 h-10 text-dx-text-muted mb-3" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 3H7a2 2 0 00-2 2v2.5c0 1.5-1 2-1 2s1 .5 1 2V14a2 2 0 002 2h1m8-14h1a2 2 0 012 2v2.5c0 1.5 1 2 1 2s-1 .5-1 2V14a2 2 0 01-2 2h-1"/></svg>
          <p class="text-sm text-dx-text-muted">输入任务名称后, 点击 "构建 JSON" 按钮</p>
          <p class="text-xs text-dx-text-muted mt-1">将自动生成 DataX 任务配置 JSON</p>
        </div>

        <!-- JSON output -->
        <div v-else class="bg-[#0c1222] border border-dx-border rounded-lg p-4 font-mono text-xs text-dx-text-secondary leading-relaxed overflow-auto max-h-96 whitespace-pre">{{ builtJson }}</div>
      </div>

      <!-- Nav Buttons -->
      <div class="flex justify-end gap-3 mt-6 pt-5 border-t border-dx-border">
        <button
          v-if="currentStep > 0"
          class="h-9 px-5 rounded-md border border-dx-border text-sm text-dx-text-secondary hover:bg-dx-card-hover hover:text-dx-text-primary transition-colors"
          @click="prevStep"
        >
          上一步
        </button>
        <button
          v-if="currentStep < 3"
          class="h-9 px-5 rounded-md bg-dx-accent hover:bg-cyan-500 text-white text-sm font-medium transition-colors flex items-center gap-1.5"
          @click="nextStep"
        >
          下一步
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
        </button>
        <button
          v-if="currentStep === 3"
          class="h-9 px-5 rounded-md bg-dx-success hover:bg-emerald-600 text-white text-sm font-medium transition-colors flex items-center gap-1.5"
          @click="handleFinish"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
          完成
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import FieldCheckboxGrid from '@/components/task/FieldCheckboxGrid.vue';

// --- Types ---
interface FieldDef {
  name: string;
  type: string;
}

// --- Step navigation ---
const steps = [
  { key: 'reader', label: '构建 Reader' },
  { key: 'writer', label: '构建 Writer' },
  { key: 'mapping', label: '字段顺序映射' },
  { key: 'build', label: '构建完成' },
];
const currentStep = ref(0);

function nextStep() { if (currentStep.value < 3) currentStep.value++; }
function prevStep() { if (currentStep.value > 0) currentStep.value--; }

function stepCircleClass(idx: number) {
  if (idx < currentStep.value) return 'border-dx-success bg-dx-success text-white';
  if (idx === currentStep.value) return 'border-dx-accent bg-dx-accent text-white';
  return 'border-dx-border bg-dx-card text-dx-text-muted';
}
function stepLabelClass(idx: number) {
  if (idx < currentStep.value) return 'text-dx-success';
  if (idx === currentStep.value) return 'text-dx-accent font-semibold';
  return 'text-dx-text-muted';
}

// --- Data sources ---
const readerSources = ['mysql_analytics (MySQL 8.0)', 'pg_orders (PostgreSQL 15)', 'mongo_products (MongoDB 7.0)', 'hive_user_profile (Hive 3.1)'];
const readerTables = ['user_behavior_log', 'order_detail', 'product_info'];
const writerSources = ['clickhouse_ads (ClickHouse 24)', 'pg_datawarehouse (PostgreSQL 15)', 'hive_user_profile (Hive 3.1)', 'hdfs_datalake (HDFS 3.3)'];
const writerTables = ['dw_user_behavior_agg', 'dw_order_metrics'];

const readerFields: FieldDef[] = [
  { name: 'id', type: 'BIGINT' }, { name: 'user_id', type: 'BIGINT' },
  { name: 'event_type', type: 'VARCHAR' }, { name: 'page_url', type: 'VARCHAR' },
  { name: 'event_time', type: 'DATETIME' }, { name: 'duration_ms', type: 'INT' },
  { name: 'device_type', type: 'VARCHAR' }, { name: 'ip_address', type: 'VARCHAR' },
  { name: 'extra_data', type: 'JSON' }, { name: 'raw_log', type: 'TEXT' },
  { name: 'created_at', type: 'DATETIME' }, { name: 'updated_at', type: 'DATETIME' },
];
const writerFields: FieldDef[] = [...readerFields];

const allReaderFieldNames = readerFields.map((f) => f.name);
const allWriterFieldNames = writerFields.map((f) => f.name);

// --- Form model ---
const form = reactive({
  taskName: '',
  reader: {
    source: '',
    table: '',
    sql: '',
    splitField: '',
    where: '',
    selectedFields: allReaderFieldNames.filter((_, i) => i < 10),
  },
  writer: {
    source: '',
    table: '',
    preSql: '',
    selectedFields: allWriterFieldNames.filter((_, i) => i < 10),
  },
  mapping: {
    reader: allReaderFieldNames.filter((_, i) => i < 10),
    writer: allWriterFieldNames.filter((_, i) => i < 10),
  },
});

// --- Step 3 mapping ---
const mappingReaderAll = computed(() => form.mapping.reader.length === readerFields.length);
const mappingWriterAll = computed(() => form.mapping.writer.length === writerFields.length);

function toggleMappingReaderAll() {
  form.mapping.reader = mappingReaderAll.value ? [] : [...allReaderFieldNames];
}
function toggleMappingWriterAll() {
  form.mapping.writer = mappingWriterAll.value ? [] : [...allWriterFieldNames];
}
function toggleMappingField(side: 'reader' | 'writer', name: string) {
  const list = form.mapping[side];
  const idx = list.indexOf(name);
  if (idx > -1) list.splice(idx, 1);
  else list.push(name);
}

// --- JSON Build ---
const builtJson = ref('');

function buildJson() {
  const job = {
    job: {
      setting: { speed: { channel: 3 } },
      content: [
        {
          reader: {
            name: 'mysqlreader',
            parameter: {
              username: 'root',
              password: '***',
              column: form.mapping.reader,
              connection: [{ table: [form.reader.table || 'user_behavior_log'], jdbcUrl: ['jdbc:mysql://10.23.45.101:3306/analytics'] }],
            },
          },
          writer: {
            name: 'clickhousewriter',
            parameter: {
              username: 'default',
              password: '***',
              column: form.mapping.writer,
              connection: [{ table: [form.writer.table || 'dw_user_behavior_agg'], jdbcUrl: ['jdbc:clickhouse://10.23.45.201:8123/ads'] }],
            },
          },
        },
      ],
    },
  };
  builtJson.value = JSON.stringify(job, null, 2);
}

function handleFinish() {
  if (!form.taskName) return;
  console.log('Task created:', form.taskName, builtJson.value);
}
</script>

<style scoped>
.checkbox-custom {
  appearance: none;
  width: 16px;
  height: 16px;
  border: 1.5px solid #64748b;
  border-radius: 3px;
  background: transparent;
  cursor: pointer;
  transition: 0.15s;
  position: relative;
  flex-shrink: 0;
}
.checkbox-custom:checked {
  background: #06b6d4;
  border-color: #06b6d4;
}
.checkbox-custom:checked::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 5px;
  height: 9px;
  border: solid #fff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
</style>
