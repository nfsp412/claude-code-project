# 前端变更：暗黑/亮色主题切换功能

## 概述
为 JSON 格式化工具添加了暗黑/亮色主题切换功能，用户可以通过页面右上角的按钮在两种主题之间切换。

## 变更内容

### 1. `src/constants/theme.ts`
- 添加了 `themeColors` 对象，定义了暗黑和亮色主题的颜色配置
- 暗黑主题：深色背景 (#1a1a2e)，浅色文本 (#e2e8f0)
- 亮色主题：浅色背景 (#f5f7fa)，深色文本 (#2c3e50)

### 2. `src/App.vue`
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

### 3. `src/components/JsonFormatter.vue`
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

## 技术细节

### 主题持久化
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

### 主题传递
```typescript
// App.vue 提供
provide('isDark', isDark);

// JsonFormatter.vue 注入
const isDark = inject('isDark', ref(true));
const isDarkMode = computed(() => isDark.value);
```

### CSS 变量覆盖模式
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

## 用户体验
- 默认使用暗黑模式
- 自动记住用户选择
- 平滑的过渡动画
- 响应式设计：移动端主题按钮位置自动调整

## 兼容性
- 支持现代浏览器
- 支持系统深色模式检测
- 移动端自适应布局
