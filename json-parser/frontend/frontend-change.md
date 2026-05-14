# Frontend Changes

## 2026-05-15 — 新增绿色测试按钮

### 修改文件

1. **`src/components/JsonFormatter.vue`** (修改)
   - 输入区域按钮组新增绿色 **"测试按钮2"** 按钮
   - `test-btn-2` 样式：绿色背景 (`#22c55e`) + 白色文字 + hover 加深效果

---

## 2026-05-15 — 新增黄色测试按钮

### 修改文件

1. **`src/components/JsonFormatter.vue`** (修改)
   - 输入区域按钮组新增黄色 **"测试按钮1"** 按钮
   - `test-btn-1` 样式：黄色背景 (`#facc15`) + 深色文字 + hover 加深效果

---

## 2026-05-12 — 新增烟花特效按钮

### 修改文件

1. **`src/components/Fireworks.vue`** (新建)
   - Canvas 烟花粒子动画组件
   - 火箭上升 → 爆炸粒子效果
   - 多色粒子 + 发光拖尾
   - 全屏 overlay，pointer-events: none 不阻挡页面交互
   - 支持多次触发叠加效果

2. **`src/components/JsonFormatter.vue`** (修改)
   - 引入 `Fireworks` 组件
   - 新增 `fireworksRef` 模板引用
   - 在输入区域按钮组末尾新增绿色 **"放烟花"** 按钮
   - `fireworks-btn` 样式：绿色渐变 + 发光阴影 + hover 上浮效果
