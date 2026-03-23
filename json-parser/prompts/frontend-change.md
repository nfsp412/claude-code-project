# 前端变更说明

本文档记录了 JSON Formatter 前端项目的所有重要变更。

---

## 1. 暗黑/亮色主题切换功能

### 概述
为 JSON 格式化工具添加了暗黑/亮色主题切换功能，用户可以通过页面右上角的按钮在两种主题之间切换。

### 变更内容

#### 1.1 `src/constants/theme.ts`
- 添加了 `themeColors` 对象，定义了暗黑和亮色主题的颜色配置
- 暗黑主题：深色背景 (#1a1a2e)，浅色文本 (#e2e8f0)
- 亮色主题：浅色背景 (#f5f7fa)，深色文本 (#2c3e50)

#### 1.2 `src/App.vue`
**新增功能：**
- 添加主题状态 `isDark` (默认 `true`，暗黑模式)
- 支持从 `localStorage` 读取用户偏好
- 支持检测系统深色模式偏好
- 主题切换时自动保存到 `localStorage`
- 添加 `provide('isDark', isDark)` 向子组件提供主题状态

**UI 变更：**
- 在页头右上角添加主题切换按钮
  - 暗黑模式下显示太阳图标 (Sunny)
  - 亮色模式下显示月亮图标 (Moon)
  - 按钮使用圆形设计，带有毛玻璃效果
  - 悬停时有缩放动画效果

**样式变更：**
- 添加 `.dark` 和 `:not(.dark)` 选择器区分两种主题
- 暗黑主题：深蓝渐变背景，紫色点缀
- 亮色主题：浅灰渐变背景，蓝色点缀
- 所有颜色过渡添加 `transition: all 0.3s ease` 动画

#### 1.3 `src/components/JsonFormatter.vue`
**新增功能：**
- 通过 `inject('isDark')` 获取父组件的主题状态
- 添加 `isDarkMode` 计算属性
- 根元素添加 `light-theme` 类用于样式控制

**样式变更：**
- 所有主要样式添加亮色主题覆盖
- 编辑器区域：亮色主题下使用白色背景和深色文本
- 下拉选择器：亮色主题下使用白色背景和 Element Plus 默认样式
- 统计标签：亮色主题下调整颜色
- 弹窗：亮色主题下使用白色背景
- 表格：亮色主题下使用浅灰色表头
- 所有过渡添加动画效果

### 技术细节

#### 主题持久化
```typescript
// 读取保存的主题或系统偏好
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
  isDark.value = savedTheme === 'dark';
}

// 保存主题变化
watch(isDark, (newVal) => {
  localStorage.setItem('theme', newVal ? 'dark' : 'light');
});
```

#### 主题传递
```typescript
// App.vue 提供
provide('isDark', isDark);

// JsonFormatter.vue 注入
const isDark = inject('isDark', ref(true));
const isDarkMode = computed(() => isDark.value);
```

#### CSS 变量覆盖模式
使用 `.light-theme` 类选择器覆盖暗黑主题样式：
```css
.json-formatter.light-theme .section-title {
  color: #2c3e50;
}

.json-formatter.light-theme .json-editor {
  background: #ffffff;
  color: #2c3e50;
}
```

### 用户体验
- 默认使用暗黑模式
- 自动记住用户选择
- 平滑的过渡动画
- 响应式设计：移动端主题按钮位置自动调整

### 兼容性
- 支持现代浏览器
- 支持系统深色模式检测
- 移动端自适应布局

---

## 2. 代码质量工具

本文档记录了为 JSON Formatter 前端项目添加的代码质量工具。

### 添加的工具

#### 2.1 ESLint - 代码静态分析

**配置文件**: `.eslintrc.cjs`

用于检测代码中的潜在问题和不良编程习惯。

- **规则集**:
  - `eslint:recommended` - ESLint 推荐规则
  - `@typescript-eslint/recommended` - TypeScript 推荐规则
  - `vue/vue3-recommended` - Vue 3 推荐规则
  - `prettier` - 与 Prettier 集成，禁用冲突规则

- **关键规则**:
  - `vue/multi-word-component-names`: off - 允许单字组件名
  - `@typescript-eslint/no-explicit-any`: warn - 警告使用 any 类型
  - `@typescript-eslint/no-unused-vars`: error - 禁止未使用的变量（下划线开头的参数除外）

#### 2.2 Prettier - 代码格式化

**配置文件**: `.prettierrc`

确保团队代码风格一致。

- **配置**:
  - `semi`: true - 使用分号
  - `singleQuote`: true - 使用单引号
  - `tabWidth`: 2 - 2 空格缩进
  - `trailingComma`: "es5" - ES5 允许的尾随逗号
  - `printWidth`: 100 - 每行最大字符数 100
  - `bracketSpacing`: true - 对象字面量括号内加空格
  - `arrowParens`: always - 箭头函数参数始终加括号
  - `vueIndentScriptAndStyle`: true - Vue 文件中 script/style 标签缩进

**忽略文件**: `.prettierignore`

#### 2.3 Husky - Git Hooks

**配置目录**: `.husky/`

在 Git 提交前自动执行代码检查。

- **pre-commit hook**: 提交前运行 `lint-staged`

#### 2.4 lint-staged - 暂存文件检查

**配置位置**: `package.json`

仅对 Git 暂存区的文件运行检查，提高效率。

```json
"lint-staged": {
  "*.{vue,ts,tsx}": [
    "eslint --fix",
    "prettier --write"
  ]
}
```

### NPM Scripts

| 命令 | 说明 |
|------|------|
| `npm run lint` | 检查并自动修复所有文件 |
| `npm run lint:check` | 仅检查所有文件（CI 使用） |
| `npm run format` | 格式化所有源文件 |
| `npm run format:check` | 检查格式（CI 使用） |
| `npm run type-check` | TypeScript 类型检查 |
| `npm run prepare` | 安装 Husky hooks（npm install 后自动运行） |

### 开发流程

#### 本地开发

1. 安装依赖：
   ```bash
   cd json-parser/frontend
   npm install
   ```

2. 开发时自动检查：
   - 保存文件时自动格式化（需配置编辑器）
   - 提交时自动运行 lint 和 format

#### 编辑器集成

**VS Code 推荐设置** (`.vscode/settings.json`):

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": ["typescript", "vue"]
}
```

#### CI/CD 检查

在 CI 流程中运行：

```bash
npm run lint:check
npm run format:check
npm run type-check
npm run build
```

### 依赖版本

| 包 | 版本 |
|----|------|
| eslint | ^8.57.0 |
| @typescript-eslint/eslint-plugin | ^7.0.0 |
| @typescript-eslint/parser | ^7.0.0 |
| eslint-plugin-vue | ^9.21.0 |
| eslint-config-prettier | ^9.1.0 |
| prettier | ^3.2.5 |
| husky | ^9.0.11 |
| lint-staged | ^15.2.2 |

### 文件清单

```
json-parser/frontend/
├── .eslintrc.cjs          # ESLint 配置
├── .prettierrc            # Prettier 配置
├── .prettierignore        # Prettier 忽略文件
├── .husky/
│   └── pre-commit         # 提交前钩子
└── package.json           # 添加 lint/format scripts 和 lint-staged 配置
```

### 使用说明

#### 首次设置

```bash
cd json-parser/frontend
npm install
# Husky 会自动通过 prepare 脚本安装
```

#### 手动运行检查

```bash
# 检查并修复所有文件
npm run lint
npm run format

# 仅检查（用于 CI）
npm run lint:check
npm run format:check
```

#### 提交代码

提交时会自动：
1. 检查暂存文件的 ESLint 规则
2. 自动修复可修复的问题
3. 用 Prettier 格式化代码
4. 如果有无法自动修复的错误，提交会被阻止

### 最佳实践

1. **保存时格式化**: 配置编辑器在保存时运行 Prettier
2. **小步提交**: 频繁提交，每次提交只包含相关改动
3. **本地先检查**: 提交前在本地运行 `npm run lint:check` 和 `npm run format:check`
4. **类型安全**: 避免使用 `any`，优先使用明确的类型定义
