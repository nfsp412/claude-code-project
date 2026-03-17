# claude code 使用指南

### 安装指南

- 参考文档 https://docs.bigmodel.cn/cn/coding-plan/tool/claude#%E6%8E%A8%E8%8D%90%E5%AE%89%E8%A3%85%E6%96%B9%E5%BC%8F
- npm install -g @anthropic-ai/claude-code
- claude --version
- 配置api key
- npx @z_ai/coding-helper
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
