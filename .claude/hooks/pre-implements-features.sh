#!/bin/bash
# Pre-hook for /implements-features command
# Fires before the Skill tool executes

# 无条件日志，验证 hook 是否被执行
echo "[$(date)] pre-hook triggered, tool=$CLAUDE_TOOL_NAME, input=$CLAUDE_TOOL_INPUT" >> /tmp/pre-hook-debug.log

SKILL_NAME=$(echo "$CLAUDE_TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('skill',''))" 2>/dev/null)

if [ "$SKILL_NAME" != "implements-features" ]; then
  exit 0
fi

# ============================================
# 在这里添加你的前置操作
# ============================================
echo "[pre-hook] implements-features 即将执行，运行前置检查..."
echo "[pre-hook] implements-features 即将执行，运行前置检查..." >> tmp.log

# 示例：检查 json-parser/frontend/ 是否存在
if [ ! -d "json-parser/frontend" ]; then
  echo "[pre-hook] 错误: json-parser/frontend/ 目录不存在" >&2
  exit 2  # 阻止执行
fi

# 示例：其他前置操作...

exit 0
