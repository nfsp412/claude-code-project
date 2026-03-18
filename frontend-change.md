# Frontend Code Quality Tools

本文档记录了为 JSON Formatter 前端项目添加的代码质量工具。

## 添加的工具

### 1. ESLint - 代码静态分析

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

### 2. Prettier - 代码格式化

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

### 3. Husky - Git Hooks

**配置目录**: `.husky/`

在 Git 提交前自动执行代码检查。

- **pre-commit hook**: 提交前运行 `lint-staged`

### 4. lint-staged - 暂存文件检查

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

## NPM Scripts

| 命令 | 说明 |
|------|------|
| `npm run lint` | 检查并自动修复所有文件 |
| `npm run lint:check` | 仅检查所有文件（CI 使用） |
| `npm run format` | 格式化所有源文件 |
| `npm run format:check` | 检查格式（CI 使用） |
| `npm run type-check` | TypeScript 类型检查 |
| `npm run prepare` | 安装 Husky hooks（npm install 后自动运行） |

## 开发流程

### 本地开发

1. 安装依赖：
   ```bash
   cd json-parser/frontend
   npm install
   ```

2. 开发时自动检查：
   - 保存文件时自动格式化（需配置编辑器）
   - 提交时自动运行 lint 和 format

### 编辑器集成

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

### CI/CD 检查

在 CI 流程中运行：

```bash
npm run lint:check
npm run format:check
npm run type-check
npm run build
```

## 依赖版本

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

## 文件清单

```
json-parser/frontend/
├── .eslintrc.cjs          # ESLint 配置
├── .prettierrc            # Prettier 配置
├── .prettierignore        # Prettier 忽略文件
├── .husky/
│   └── pre-commit         # 提交前钩子
└── package.json           # 添加 lint/format scripts 和 lint-staged 配置
```

## 使用说明

### 首次设置

```bash
cd json-parser/frontend
npm install
# Husky 会自动通过 prepare 脚本安装
```

### 手动运行检查

```bash
# 检查并修复所有文件
npm run lint
npm run format

# 仅检查（用于 CI）
npm run lint:check
npm run format:check
```

### 提交代码

提交时会自动：
1. 检查暂存文件的 ESLint 规则
2. 自动修复可修复的问题
3. 用 Prettier 格式化代码
4. 如果有无法自动修复的错误，提交会被阻止

## 最佳实践

1. **保存时格式化**: 配置编辑器在保存时运行 Prettier
2. **小步提交**: 频繁提交，每次提交只包含相关改动
3. **本地先检查**: 提交前在本地运行 `npm run lint:check` 和 `npm run format:check`
4. **类型安全**: 避免使用 `any`，优先使用明确的类型定义
