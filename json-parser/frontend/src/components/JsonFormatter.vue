<script setup lang="ts">
import { ref, watch, inject, computed } from 'vue';
import { jsonApi } from '../api/json';
import { DocumentCopy, DocumentDelete, MagicStick, Minus, RefreshRight, Select } from '@element-plus/icons-vue';
import { ElMessage, ElSelect, ElOption } from 'element-plus';
import { jsonSamples } from '../data/samples';
import type { ContentValidateResult, ColumnMismatch } from '../types';

// 注入主题状态
const isDark = inject('isDark', ref(true));
const isDarkMode = computed(() => isDark.value);

const input = ref('');
const selectedSample = ref('');
const output = ref('');
const isValid = ref(true);
const errorMessage = ref('');
const indent = ref<string | number>(2);
const isMinified = ref(false);
const preMinifyOutput = ref('');

const inputSize = ref(0);
const inputLineCount = ref(0);
const outputSize = ref(0);
const outputLineCount = ref(0);

// 字段校验弹窗状态
const columnDialogVisible = ref(false);
const columnValidateResults = ref<ContentValidateResult[]>([]);

const calculateStats = (text: string) => {
  return {
    size: new Blob([text]).size,
    lines: text ? text.split('\n').length : 0
  };
};

watch(input, (newVal) => {
  isMinified.value = false;
  const stats = calculateStats(newVal);
  inputSize.value = stats.size;
  inputLineCount.value = stats.lines;
  if (newVal) {
    jsonApi.validate(newVal).then(result => {
      isValid.value = result.valid;
      errorMessage.value = result.error || '';
    }).catch(() => {
      isValid.value = false;
    });
  } else {
    isValid.value = true;
    errorMessage.value = '';
  }
}, { immediate: true });

watch(output, (newVal) => {
  const stats = calculateStats(newVal);
  outputSize.value = stats.size;
  outputLineCount.value = stats.lines;
});

const formatJson = async () => {
  isMinified.value = false;
  if (!input.value || !input.value.trim()) {
    return;
  }
  try {
    const result = await jsonApi.validate(input.value);
    if (result.valid) {
      output.value = await jsonApi.format(input.value, indent.value);
      isValid.value = true;
      errorMessage.value = '';
    } else {
      isValid.value = false;
      errorMessage.value = result.error || 'JSON 格式无效';
    }
  } catch (e: any) {
    isValid.value = false;
    errorMessage.value = e.message || '格式化失败';
  }
};

const minifyJson = async () => {
  if (!input.value || !input.value.trim()) {
    return;
  }

  if (isMinified.value) {
    output.value = preMinifyOutput.value;
    isMinified.value = false;
    isValid.value = true;
    errorMessage.value = '';
    return;
  }

  preMinifyOutput.value = output.value;

  try {
    const result = await jsonApi.validate(input.value);
    if (result.valid) {
      output.value = await jsonApi.minify(input.value);
      isValid.value = true;
      errorMessage.value = '';
      isMinified.value = true;
    } else {
      isValid.value = false;
      errorMessage.value = result.error || 'JSON 格式无效';
    }
  } catch (e: any) {
    isValid.value = false;
    errorMessage.value = e.message || '压缩失败';
  }
};

const clearAll = () => {
  isMinified.value = false;
  input.value = '';
  output.value = '';
  isValid.value = true;
  errorMessage.value = '';
};

const copyOutput = async () => {
  if (!output.value) {
    ElMessage.warning('没有可复制的内容');
    return;
  }
  try {
    await navigator.clipboard.writeText(output.value);
    ElMessage.success('已复制到剪贴板');
  } catch (e) {
    ElMessage.error('复制失败');
  }
};

const handleInputChange = () => {
  // watch 会自动处理验证和统计
};

const loadSample = (sampleKey: string) => {
  if (sampleKey) {
    input.value = jsonSamples[sampleKey as keyof typeof jsonSamples].data;
    selectedSample.value = '';
    handleInputChange();
  }
};

const validateColumns = async () => {
  if (!input.value || !input.value.trim()) {
    ElMessage.warning('请先输入 JSON');
    return;
  }
  try {
    const result = await jsonApi.validateColumns(input.value);
    if (result.valid) {
      ElMessage.success('字段校验通过：Reader 与 Writer 字段顺序一致');
    } else {
      columnValidateResults.value = result.results;
      columnDialogVisible.value = true;
    }
  } catch (e: any) {
    const detail = e.response?.data?.detail || e.message || '字段校验失败';
    ElMessage.error(detail);
  }
};

const getMismatchStatus = (m: ColumnMismatch): string => {
  if (m.reader_field === null) return 'Writer 多余';
  if (m.writer_field === null) return 'Reader 多余';
  return '不一致';
};
</script>

<template>
  <div class="json-formatter" :class="{ 'light-theme': !isDarkMode }">
    <!-- 输入区域 -->
    <div class="formatter-section input-section">
      <div class="section-header">
        <h3 class="section-title">输入</h3>
        <div class="header-right">
          <el-select
            v-model="selectedSample"
            placeholder="加载样例"
            class="sample-select"
            popper-class="glass-popper"
            @change="loadSample"
          >
            <el-option
              v-for="(sample, key) in jsonSamples"
              :key="key"
              :label="sample.name"
              :value="key"
            />
          </el-select>
          <div class="stats">
            <span class="stat">{{ inputSize }} bytes</span>
            <span class="stat">{{ inputLineCount }} 行</span>
          </div>
        </div>
      </div>
      <div class="editor-container">
        <textarea
          v-model="input"
          class="json-editor"
          placeholder="在此粘贴或输入 JSON..."
          @input="handleInputChange"
        ></textarea>
      </div>
      <div v-if="!isValid" class="error-message">
        {{ errorMessage }}
      </div>
      <div class="action-row">
        <el-select v-model="indent" placeholder="选择缩进" class="indent-select" popper-class="glass-popper">
          <el-option label="1 个制表符" value="tab" />
          <el-option label="2 个空格" :value="2" />
          <el-option label="4 个空格" :value="4" />
          <el-option label="8 个空格" :value="8" />
        </el-select>
        <div class="button-group">
          <el-button
            type="primary"
            :icon="MagicStick"
            class="format-btn"
            @click="formatJson"
          >
            格式化
          </el-button>
          <el-button
            :icon="Select"
            class="validate-col-btn"
            @click="validateColumns"
          >
            字段校验
          </el-button>
          <el-button
            :icon="DocumentDelete"
            class="clear-btn"
            @click="clearAll"
          >
            清空
          </el-button>
        </div>
      </div>
    </div>

    <!-- 输出区域 -->
    <div class="formatter-section output-section">
      <div class="section-header">
        <h3 class="section-title">输出</h3>
        <div class="stats">
          <span class="stat">{{ outputSize }} bytes</span>
          <span class="stat">{{ outputLineCount }} 行</span>
        </div>
      </div>
      <div class="editor-container">
        <textarea
          v-model="output"
          class="json-editor"
          placeholder="格式化后的 JSON 将显示在这里..."
          readonly
        ></textarea>
      </div>
      <div class="button-group">
        <el-button
          :type="isMinified ? 'info' : 'warning'"
          :icon="isMinified ? RefreshRight : Minus"
          class="minify-btn"
          @click="minifyJson"
        >
          {{ isMinified ? '还原' : '压缩' }}
        </el-button>
        <el-button
          type="success"
          :icon="DocumentCopy"
          class="copy-btn"
          @click="copyOutput"
        >
          复制
        </el-button>
      </div>
    </div>

    <!-- 字段校验结果弹窗 -->
    <el-dialog
      v-model="columnDialogVisible"
      title="字段校验结果"
      width="700px"
      class="column-dialog"
    >
      <div v-for="r in columnValidateResults" :key="r.index" class="content-result">
        <div class="content-result-header">
          <span class="content-index">Content [{{ r.index }}]</span>
          <span :class="['content-status', r.valid ? 'status-pass' : 'status-fail']">
            {{ r.valid ? '通过' : '不通过' }}
          </span>
          <span class="content-count">
            Reader: {{ r.reader_count }} 个字段 / Writer: {{ r.writer_count }} 个字段
          </span>
        </div>
        <el-table
          v-if="r.mismatches.length > 0"
          :data="r.mismatches"
          stripe
          size="small"
          class="mismatch-table"
        >
          <el-table-column prop="position" label="位置" width="70" align="center" />
          <el-table-column label="Reader 字段">
            <template #default="{ row }">
              <span :class="{ 'field-missing': row.reader_field === null }">
                {{ row.reader_field ?? '(缺失)' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="Writer 字段">
            <template #default="{ row }">
              <span :class="{ 'field-missing': row.writer_field === null }">
                {{ row.writer_field ?? '(缺失)' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="120" align="center">
            <template #default="{ row }">
              <el-tag :type="row.reader_field === null || row.writer_field === null ? 'warning' : 'danger'" size="small">
                {{ getMismatchStatus(row) }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.json-formatter {
  display: flex;
  gap: 2rem;
  width: 100%;
  height: 100%;
  padding: 1rem;
  transition: all 0.3s ease;
}

/* 亮色主题 */
.json-formatter.light-theme {
  background: rgba(255, 255, 255, 0.5);
}

.formatter-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #e2e8f0;
  transition: all 0.3s ease;
}

.json-formatter.light-theme .section-title {
  color: #2c3e50;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stats {
  display: flex;
  gap: 1rem;
}

.sample-select {
  width: 120px;
}

:deep(.sample-select .el-input .el-input__wrapper) {
  background: rgba(37, 37, 56, 0.7) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: none !important;
  border-radius: 6px;
  transition: all 0.2s ease;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

:deep(.sample-select .el-input .el-input__wrapper:hover) {
  background: rgba(42, 42, 64, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
}

:deep(.sample-select .el-input .el-input__wrapper.is-focus) {
  border-color: #7070a0 !important;
  box-shadow: 0 0 0 2px rgba(112, 112, 160, 0.2) !important;
}

:deep(.sample-select .el-input .el-input__inner) {
  color: #e2e8f0;
}

:deep(.sample-select .el-input .el-input__inner::placeholder) {
  color: #a0aec0;
}

/* 亮色主题下的下拉框 */
.json-formatter.light-theme :deep(.sample-select .el-input .el-input__wrapper) {
  background: #ffffff !important;
  border: 1px solid #dcdfe6 !important;
}

.json-formatter.light-theme :deep(.sample-select .el-input .el-input__wrapper:hover) {
  border-color: #409eff !important;
}

.json-formatter.light-theme :deep(.sample-select .el-input .el-input__wrapper.is-focus) {
  border-color: #409eff !important;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2) !important;
}

.json-formatter.light-theme :deep(.sample-select .el-input .el-input__inner) {
  color: #2c3e50;
}

.json-formatter.light-theme :deep(.sample-select .el-input .el-input__inner::placeholder) {
  color: #a8abb2;
}

.stat {
  font-size: 0.85rem;
  color: #a0aec0;
  background: rgba(160, 174, 192, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  transition: all 0.3s ease;
}

.json-formatter.light-theme .stat {
  color: #606266;
  background: rgba(96, 98, 102, 0.1);
}

.editor-container {
  flex: 1;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.json-editor {
  width: 100%;
  height: 100%;
  min-height: 300px;
  background: #1a1a2e;
  color: #e2e8f0;
  border: 1px solid #2d3748;
  border-radius: 0.5rem;
  padding: 1rem;
  font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
  resize: none;
  outline: none;
  transition: all 0.2s;
}

.json-editor:focus {
  border-color: #8a9eff;
}

.json-editor::placeholder {
  color: #4a5568;
}

/* 亮色主题下的编辑器 */
.json-formatter.light-theme .json-editor {
  background: #ffffff;
  color: #2c3e50;
  border: 1px solid #dcdfe6;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.json-formatter.light-theme .json-editor:focus {
  border-color: #409eff;
}

.json-formatter.light-theme .json-editor::placeholder {
  color: #c0c4cc;
}

.error-message {
  color: #f87171;
  font-size: 0.9rem;
  padding: 0.5rem;
  background: rgba(248, 113, 113, 0.1);
  border-radius: 0.25rem;
  border-left: 3px solid #f87171;
  transition: all 0.3s ease;
}

.json-formatter.light-theme .error-message {
  background: rgba(245, 108, 108, 0.1);
}

.action-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.indent-select {
  width: 150px;
}

:deep(.indent-select .el-input .el-input__wrapper) {
  background: rgba(37, 37, 56, 0.7) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: none !important;
  border-radius: 6px;
  transition: all 0.2s ease;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

:deep(.indent-select .el-input .el-input__wrapper:hover) {
  background: rgba(42, 42, 64, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
}

:deep(.indent-select .el-input .el-input__wrapper.is-focus) {
  border-color: #7070a0 !important;
  box-shadow: 0 0 0 2px rgba(112, 112, 160, 0.2) !important;
}

:deep(.indent-select .el-input .el-input__inner) {
  color: #e2e8f0;
}

/* 亮色主题下的缩进选择器 */
.json-formatter.light-theme :deep(.indent-select .el-input .el-input__wrapper) {
  background: #ffffff !important;
  border: 1px solid #dcdfe6 !important;
}

.json-formatter.light-theme :deep(.indent-select .el-input .el-input__wrapper:hover) {
  border-color: #409eff !important;
}

.json-formatter.light-theme :deep(.indent-select .el-input .el-input__wrapper.is-focus) {
  border-color: #409eff !important;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2) !important;
}

.json-formatter.light-theme :deep(.indent-select .el-input .el-input__inner) {
  color: #2c3e50;
}

.button-group {
  display: flex;
  gap: 0.75rem;
}

.format-btn {
  background-color: #3b82f6 !important;
  border-color: #3b82f6 !important;
  color: #fff !important;
}

.format-btn:hover {
  background-color: #2563eb !important;
  border-color: #2563eb !important;
}

.validate-col-btn {
  background-color: #8b5cf6 !important;
  border-color: #8b5cf6 !important;
  color: #fff !important;
}

.validate-col-btn:hover {
  background-color: #7c3aed !important;
  border-color: #7c3aed !important;
}

.clear-btn {
  background-color: #e6a23c !important;
  border-color: #e6a23c !important;
  color: #fff !important;
}

.clear-btn:hover {
  background-color: #cf9236 !important;
  border-color: #cf9236 !important;
}

.minify-btn {
  background-color: #f97316 !important;
  border-color: #f97316 !important;
  color: #fff !important;
}

.minify-btn:hover {
  background-color: #e96306 !important;
  border-color: #e96306 !important;
}

.copy-btn {
  background-color: #f87171 !important;
  border-color: #f87171 !important;
  color: #fff !important;
}

.copy-btn:hover {
  background-color: #ef4444 !important;
  border-color: #ef4444 !important;
}

/* 字段校验弹窗 - 暗黑主题 */
:deep(.column-dialog .el-dialog) {
  background: #1e1e30 !important;
  border: 1px solid #2d3748;
  border-radius: 12px;
}

:deep(.column-dialog .el-dialog__header) {
  border-bottom: 1px solid #2d3748;
  padding: 16px 20px;
}

:deep(.column-dialog .el-dialog__title) {
  color: #e2e8f0;
  font-weight: 600;
}

:deep(.column-dialog .el-dialog__body) {
  padding: 20px;
  color: #e2e8f0;
}

:deep(.column-dialog .el-dialog__headerbtn .el-dialog__close) {
  color: #a0aec0;
}

/* 亮色主题下的弹窗 */
.json-formatter.light-theme :deep(.column-dialog .el-dialog) {
  background: #ffffff !important;
  border: 1px solid #e4e7ed;
}

.json-formatter.light-theme :deep(.column-dialog .el-dialog__header) {
  border-bottom: 1px solid #e4e7ed;
}

.json-formatter.light-theme :deep(.column-dialog .el-dialog__title) {
  color: #2c3e50;
}

.json-formatter.light-theme :deep(.column-dialog .el-dialog__body) {
  color: #2c3e50;
}

.json-formatter.light-theme :deep(.column-dialog .el-dialog__headerbtn .el-dialog__close) {
  color: #606266;
}

.content-result {
  margin-bottom: 1.5rem;
}

.content-result:last-child {
  margin-bottom: 0;
}

.content-result-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.content-index {
  font-weight: 600;
  color: #e2e8f0;
  transition: all 0.3s ease;
}

.json-formatter.light-theme .content-index {
  color: #2c3e50;
}

.content-status {
  font-size: 0.8rem;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.status-pass {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.status-fail {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.content-count {
  font-size: 0.8rem;
  color: #a0aec0;
  margin-left: auto;
  transition: all 0.3s ease;
}

.json-formatter.light-theme .content-count {
  color: #606266;
}

.field-missing {
  color: #a0aec0;
  font-style: italic;
  transition: all 0.3s ease;
}

.json-formatter.light-theme .field-missing {
  color: #909399;
}

:deep(.mismatch-table) {
  --el-table-bg-color: #1a1a2e;
  --el-table-tr-bg-color: #1a1a2e;
  --el-table-header-bg-color: #252538;
  --el-table-row-hover-bg-color: #252538;
  --el-table-border-color: #2d3748;
  --el-table-text-color: #e2e8f0;
  --el-table-header-text-color: #a0aec0;
  --el-fill-color-lighter: #252538;
  border-radius: 8px;
  overflow: hidden;
}

/* 亮色主题下的表格 */
.json-formatter.light-theme :deep(.mismatch-table) {
  --el-table-bg-color: #ffffff;
  --el-table-tr-bg-color: #ffffff;
  --el-table-header-bg-color: #f5f7fa;
  --el-table-row-hover-bg-color: #f5f7fa;
  --el-table-border-color: #e4e7ed;
  --el-table-text-color: #2c3e50;
  --el-table-header-text-color: #606266;
  --el-fill-color-lighter: #f5f7fa;
}

/* 响应式布局 */
@media (max-width: 1000px) {
  .json-formatter {
    flex-direction: column;
    gap: 1.5rem;
  }

  .formatter-section {
    min-height: 300px;
  }

  .button-group {
    flex-wrap: wrap;
  }

  .json-editor {
    min-height: 200px;
  }

  .header-right {
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
  }

  .sample-select {
    width: 100px;
  }
}
</style>
