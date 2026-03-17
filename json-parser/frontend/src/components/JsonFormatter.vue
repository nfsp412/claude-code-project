<script setup lang="ts">
import { ref, watch } from 'vue';
import { jsonApi } from '../api/json';
import { THEME } from '../constants/theme';
import { DocumentCopy, DocumentDelete, MagicStick, Minus } from '@element-plus/icons-vue';
import { ElMessage, ElSelect, ElOption } from 'element-plus';
import { jsonSamples } from '../data/samples';

const input = ref('');
const selectedSample = ref('');
const output = ref('');
const isValid = ref(true);
const errorMessage = ref('');
const indent = ref(2);

// 状态：大小和行数
const inputSize = ref(0);
const inputLineCount = ref(0);
const outputSize = ref(0);
const outputLineCount = ref(0);

// 本地计算方法（用于实时统计，不调用 API）
const calculateStats = (text: string) => {
  return {
    size: new Blob([text]).size,
    lines: text ? text.split('\n').length : 0
  };
};

// 监听输入变化，更新统计
watch(input, (newVal) => {
  const stats = calculateStats(newVal);
  inputSize.value = stats.size;
  inputLineCount.value = stats.lines;
  // 实时验证
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

// 监听输出变化，更新统计
watch(output, (newVal) => {
  const stats = calculateStats(newVal);
  outputSize.value = stats.size;
  outputLineCount.value = stats.lines;
});

// 格式化 JSON
const formatJson = async () => {
  // 空输入时不执行任何操作，不显示错误
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

// 压缩 JSON
const minifyJson = async () => {
  // 空输入时不执行任何操作，不显示错误
  if (!input.value || !input.value.trim()) {
    return;
  }
  try {
    const result = await jsonApi.validate(input.value);
    if (result.valid) {
      output.value = await jsonApi.minify(input.value);
      isValid.value = true;
      errorMessage.value = '';
    } else {
      isValid.value = false;
      errorMessage.value = result.error || 'JSON 格式无效';
    }
  } catch (e: any) {
    isValid.value = false;
    errorMessage.value = e.message || '压缩失败';
  }
};

// 清空内容
const clearAll = () => {
  input.value = '';
  output.value = '';
  isValid.value = true;
  errorMessage.value = '';
};

// 复制输出
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

// 处理输入变化（验证已在 watch 中处理）
const handleInputChange = () => {
  // watch 会自动处理验证和统计
};

// 加载样例数据
const loadSample = (sampleKey: string) => {
  if (sampleKey) {
    input.value = jsonSamples[sampleKey as keyof typeof jsonSamples].data;
    selectedSample.value = '';
    handleInputChange();
  }
};
</script>

<template>
  <div class="json-formatter">
    <!-- 输入区域 -->
    <div class="formatter-section input-section">
      <div class="section-header">
        <h3 class="section-title">输入</h3>
        <div class="header-right">
          <el-select
            v-model="selectedSample"
            placeholder="加载样例"
            class="sample-select"
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
          :icon="DocumentDelete"
          class="clear-btn"
          @click="clearAll"
        >
          清空
        </el-button>
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
          type="warning"
          :icon="Minus"
          class="minify-btn"
          @click="minifyJson"
        >
          压缩
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
  </div>
</template>

<style scoped>
.json-formatter {
  display: flex;
  gap: 2rem;
  width: 100%;
  height: 100%;
  padding: 1rem;
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

:deep(.sample-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  box-shadow: none;
}

:deep(.sample-select .el-input__inner) {
  color: #e2e8f0;
}

:deep(.sample-select .el-input__inner::placeholder) {
  color: #a0aec0;
}

.stat {
  font-size: 0.85rem;
  color: #a0aec0;
  background: rgba(160, 174, 192, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
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
  transition: border-color 0.2s;
}

.json-editor:focus {
  border-color: #8a9eff;
}

.json-editor::placeholder {
  color: #4a5568;
}

.error-message {
  color: #f87171;
  font-size: 0.9rem;
  padding: 0.5rem;
  background: rgba(248, 113, 113, 0.1);
  border-radius: 0.25rem;
  border-left: 3px solid #f87171;
}

.button-group {
  display: flex;
  gap: 0.75rem;
}

.format-btn {
  background-color: #a0aec0 !important;
  border-color: #a0aec0 !important;
  color: #fff !important;
}

.format-btn:hover {
  background-color: #909eb0 !important;
  border-color: #909eb0 !important;
}

.clear-btn {
  background-color: #a0aec0 !important;
  border-color: #a0aec0 !important;
  color: #fff !important;
}

.clear-btn:hover {
  background-color: #909eb0 !important;
  border-color: #909eb0 !important;
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
  background-color: #10b981 !important;
  border-color: #10b981 !important;
  color: #fff !important;
}

.copy-btn:hover {
  background-color: #0da86e !important;
  border-color: #0da86e !important;
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
