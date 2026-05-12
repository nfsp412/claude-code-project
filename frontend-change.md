# Frontend Changes - 跳转claude 按钮

## 修改文件

### `json-parser/frontend/src/components/JsonFormatter.vue`

1. **导入 Link 图标**: 从 `@element-plus/icons-vue` 导入 `Link` 图标
2. **新增 `goToClaude` 方法**: 点击按钮时在新标签页打开 `https://claude.ai`
3. **模板新增按钮**: 在输出区域的按钮组中添加红色 "跳转claude" 按钮
4. **样式**: 新增 `.claude-btn` 样式类，背景色 `#ef4444`，hover 时 `#dc2626`
