# Frontend Changes

## 新增"跳转deepseek"按钮

**文件**: `json-parser/frontend/src/components/JsonFormatter.vue`

### 变更内容

1. **新增按钮** (输入区域 button-group): 
   - 白色背景 (`#ffffff`), 深色文字 (`#1a1a2e`)
   - 文字: "跳转deepseek"
   - 图标: Link (来自 @element-plus/icons-vue)
   - 点击时通过 `window.open` 在新标签页打开 https://www.deepseek.com/

2. **新增方法**: `goDeepSeek()` - 使用 `window.open('https://www.deepseek.com/', '_blank')` 跳转到 DeepSeek 官网

3. **新增样式**: `.deepseek-btn` - 白色按钮，hover 时变为浅灰 (`#e2e8f0`)
