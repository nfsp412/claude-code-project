<script setup lang="ts">
import { ref, onMounted, watch, provide } from 'vue';
import JsonFormatter from './components/JsonFormatter.vue';

const isDark = ref(true);

// 检测系统深色模式偏好和 localStorage
onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    isDark.value = savedTheme === 'dark';
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDark.value = true;
  }
});

// 监听主题变化并保存
watch(isDark, (newVal) => {
  localStorage.setItem('theme', newVal ? 'dark' : 'light');
});

// 切换主题
const toggleTheme = () => {
  isDark.value = !isDark.value;
};

// 提供给子组件使用
provide('isDark', isDark);
</script>

<template>
  <div id="app" :class="{ dark: isDark }">
    <!-- 页头区域 (20%) -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <svg viewBox="0 0 24 24" class="logo-icon">
            <path fill="currentColor" d="M5 3h2v2H5v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5h2v2H5c-1.07-.27-2-.9-2-2v-4a2 2 0 0 0-2-2 2 2 0 0 0 2-2V5a2 2 0 0 1 2-2m14 0a2 2 0 0 1 2 2v4a2 2 0 0 0 2 2 2 2 0 0 0-2 2v4a2 2 0 0 1-2 2h-2v-2h2v-5a2 2 0 0 1 2-2 2 2 0 0 1-2-2V5h-2V3h2M10 15l2 2 4-4"/>
          </svg>
        </div>
        <div class="header-text">
          <h1 class="header-title">JSON 格式化工具</h1>
          <p class="header-subtitle">快速、美观、易用的 JSON 处理工具</p>
        </div>
        <button class="theme-toggle" @click="toggleTheme" :title="isDark ? '切换到亮色模式' : '切换到暗黑模式'">
          <svg v-if="isDark" viewBox="0 0 24 24" class="theme-icon">
            <path fill="currentColor" d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5M2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1m18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1M11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1m0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1M5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" class="theme-icon">
            <path fill="currentColor" d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/>
          </svg>
        </button>
      </div>
    </header>

    <!-- 主体区域 (70%) -->
    <main class="main">
      <JsonFormatter />
    </main>

    <!-- 页脚区域 (10%) -->
    <footer class="footer">
      <div class="footer-content">
        <p class="footer-text">&copy; 2026 JSON Formatter. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  width: 100%;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  transition: background 0.3s ease;
}

/* 暗黑主题（默认） */
#app.dark {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
}

#app.dark::before {
  content: '';
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(138, 158, 255, 0.1) 0%, transparent 50%),
              radial-gradient(circle, rgba(16, 185, 129, 0.05) 0%, transparent 50%);
  animation: rotate 20s linear infinite;
  pointer-events: none;
  z-index: 0;
}

/* 亮色主题 */
#app:not(.dark) {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 50%, #dcdfe6 100%);
}

#app:not(.dark)::before {
  content: '';
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(64, 158, 255, 0.08) 0%, transparent 50%),
              radial-gradient(circle, rgba(103, 194, 58, 0.05) 0%, transparent 50%);
  animation: rotate 20s linear infinite;
  pointer-events: none;
  z-index: 0;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 页头区域 (20%) */
.header {
  flex: 0 0 20%;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

#app:not(.dark) .header {
  background: rgba(255, 255, 255, 0.8);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  text-align: center;
  position: relative;
  width: 100%;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon {
  width: 60px;
  height: 60px;
  color: #8a9eff;
  filter: drop-shadow(0 0 10px rgba(138, 158, 255, 0.5));
  transition: all 0.3s ease;
}

#app:not(.dark) .logo-icon {
  color: #409eff;
  filter: drop-shadow(0 0 10px rgba(64, 158, 255, 0.3));
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.header-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #8a9eff 0%, #e0e7ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.05em;
  transition: all 0.3s ease;
}

#app:not(.dark) .header-title {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-subtitle {
  font-size: 1.1rem;
  color: #a0aec0;
  font-weight: 400;
  transition: all 0.3s ease;
}

#app:not(.dark) .header-subtitle {
  color: #606266;
}

/* 主题切换按钮 - 右上角定位 */
.theme-toggle {
  position: absolute;
  right: 2rem;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  padding: 0;
}

#app:not(.dark) .theme-toggle {
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.05);
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-50%) scale(1.1);
}

#app:not(.dark) .theme-toggle:hover {
  background: rgba(0, 0, 0, 0.1);
}

.theme-icon {
  width: 22px;
  height: 22px;
  color: #e2e8f0;
  transition: all 0.3s ease;
}

#app:not(.dark) .theme-icon {
  color: #2c3e50;
}

/* 主体区域 (70%) */
.main {
  flex: 1;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem 2rem;
  position: relative;
  z-index: 1;
}

/* 页脚区域 (10%) */
.footer {
  flex: 0 0 10%;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

#app:not(.dark) .footer {
  background: rgba(255, 255, 255, 0.6);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.footer-content {
  text-align: center;
}

.footer-text {
  font-size: 0.9rem;
  color: #a0aec0;
  font-weight: 400;
  transition: all 0.3s ease;
}

#app:not(.dark) .footer-text {
  color: #606266;
}

/* Element Plus 深色模式覆盖 */
:deep(.el-button) {
  font-weight: 500;
  transition: all 0.2s ease;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #8a9eff 0%, #7a8eef 100%);
  border: none;
}

:deep(.el-button--success) {
  background: linear-gradient(135deg, #10b981 0%, #0da86e 100%);
  border: none;
}

:deep(.el-button--warning) {
  background: linear-gradient(135deg, #f97316 0%, #e96306 100%);
  border: none;
}

:deep(.el-message) {
  background: rgba(26, 26, 46, 0.95) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

:deep(.el-message__content) {
  color: #e2e8f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header {
    min-height: 100px;
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    gap: 0.75rem;
  }

  .logo-icon {
    width: 40px;
    height: 40px;
  }

  .header-title {
    font-size: 1.75rem;
  }

  .header-subtitle {
    font-size: 0.95rem;
  }

  .main {
    padding: 0.75rem 1rem;
  }

  .footer {
    min-height: 50px;
    padding: 0.75rem 1rem;
  }

  .footer-text {
    font-size: 0.8rem;
  }

  /* 移动端主题按钮位置调整 */
  .theme-toggle {
    position: static;
    transform: none;
    margin-top: 0.5rem;
  }

  .theme-toggle:hover {
    transform: scale(1.1);
  }
}
</style>
