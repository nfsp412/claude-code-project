# claude code 使用指南

### 安装指南

- 参考文档 https://docs.bigmodel.cn/cn/coding-plan/tool/claude#%E6%8E%A8%E8%8D%90%E5%AE%89%E8%A3%85%E6%96%B9%E5%BC%8F
- npm install -g @anthropic-ai/claude-code
- claude --version
- 配置api key
- npx @z_ai/coding-helper 这是GLM的自动化助手,可以手动编辑 `~/.claude/settings.json` 文件
- claude

### 内置工具

- /status 查看模型等信息
- /init 可以创建CLAUDE.md文件
    - 三个位置存放CLAUDE.md文件
    - CLAUDE.md 可以提交git,使用/init生成,当前目录下存放
    - CLAUDE.local.md 不共享,被git忽略,当前目录下存放
    - ~/.claude/CLAUDE.md 所有项目共用
    - create CLAUDE.chinese.md in Chinese 可以生成中文版
- /ide 添加IDE工具,例如vscode,需要先安装claude插件
    - 安装失败时,Cmd+Shift+P;Shell Command: Install 'code' command in PATH;重启vscode
- /model 查看使用的模型
- /help 
- /clear 清除上下文
- /compact 压缩上下文
- /mcp 查看添加的mcp服务器
- /permissions 权限设置
- /hooks 钩子

### 常用技巧

- shift+tab 按两下 进入plan mode 按一下 进入自动接受所有编辑
- 可以直接截图后复制到命令行,然后让claude进行分析
- \反斜杠,加回车enter,可以实现命令行的换行输入
- `# always answer me in Chinese` 触发上下文引用,添加到CLAUDE.md文件
- 可以结合git一起使用,无需输入git命令

### 常用提示词

- @json-parser/ 浏览这个代码库
- @json-parser/ 这个代码库是怎样执行的
- 初始化git仓库并提交
- add和commit这些更改
- 使用 playwright 这个 mcp 服务器,访问 localhost:5173 我希望格式化按钮的颜色和清空按钮的颜色一致
- think a lot: 触发深度思考,Flambéing… (thinking) 和 Doing… (thinking) 的区别
- 在代码重构时,可以参考如下的提示词写法:
    - Current behavior 
    - Desired behavior 
    - Example flow 
    - Requirements 
    - Notes 例如修改哪个文件,可以在这里指定
    - 使用两个子代理去头脑风暴可能的计划,先不要实现代码 可以触发使用两个并行子任务task去进行plan

### MCP

- 模型上下文协议
- claude code可以接入其他MCP服务器,增强功能
- 以playwright为例
    - 添加: claude mcp add playwrite npx @playwright/mcp@latest
    - 查看: /mcp
    - 使用: 使用 playwright 这个 mcp 服务器,访问 localhost:5173 我希望格式化按钮的颜色和清空按钮的颜色一致
    - 结合claude的plan一起使用,触发mcp功能

### 新增功能

- 创建 .claude/commands/xxx.md文件 该文件会自动添加到claude中,使用/可以获取到自定义的功能
- 具体功能的编写格式,可以参考 [text](.claude/commands/implements-features.md)

### 多claude运行

- 需要结合git的工作树实现,避免产生代码冲突覆盖的问题
    - git worktree add .tree/ui_feature
    - git branch -a
- 同时在多个工作树目录下打开终端,运行claude
- 各自提交git后,在主分支进入claude进行合并
    - 使用 git merge 命令合并在 .tree 目录下的所有worktree,如果有冲突则尝试修复冲突

### github集成

- 调用 /install-github-app 命令安装相关组件
    - 一般会要求你先安装github cli,可以使用 brew install gh 命令安装
    - gh auth login 
    - gh auth refresh -h github.com -s repo,workflow
- 可以实现github在线解决issue的功能,需要官方订阅或者API付费

### 钩子集成

- /hooks
- 有触发钩子的不同生命周期位置
- 演示示例
    - 选择post tool use 工具使用后触发钩子
    - 选择 Read 命令,代表执行该命令后触发钩子
    - 钩子设置为 say 'All Done'
    - 注意需要添加到 `./.claude/settings.json` 文件
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "say 'All Done'"
          }
        ]
      }
    ]
  }
}
```

