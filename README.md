# claude code 使用指南

### claude code是什么

- cli agentic coding assistant
- 组件:一个大模型model,一组工具tools,以及运行工具的环境;以及其他功能:例如让模型有记忆力
- MCP:模型连接协议;内置tools,还能通过MCP扩展tools
![alt text](static/image-1.png)
- 不索引代码库:代理式搜索;无需把所有代码加入上下文,也无需离开当前的本地环境系统 

### 安装指南

- 参考文档 https://docs.bigmodel.cn/cn/coding-plan/tool/claude#%E6%8E%A8%E8%8D%90%E5%AE%89%E8%A3%85%E6%96%B9%E5%BC%8F
- npm install -g @anthropic-ai/claude-code
- claude --version
- 配置api key
- npx @z_ai/coding-helper 这是GLM的自动化助手,可以手动编辑 `~/.claude/settings.json` 文件
- claude进入命令行

### CLAUDE.md文件

- /init 可以创建CLAUDE.md文件;实际上这个命令就是浏览整个代码库,然后添加了关键性的内容;可以重复调用;可以嵌套性的创建多个不同的CLAUDE.md文件
- 三个位置存放CLAUDE.md文件
- CLAUDE.md 可以提交git,使用/init生成,当前目录下存放
- CLAUDE.local.md 不共享,被git忽略,当前目录下存放
- ~/.claude/CLAUDE.md 所有项目共用
- 该文件包含了以下几部分内容:
  - Project Overview
  - Development Commands
  - Architecture 架构图
  - 可能有 API Endpoints 即接口文档
  - Key Conventions 关键性的事先约定
- 使用例如 `#use uv to run python files` 可以将内容添加到CLAUDE.md文件的Key Conventions中
- 例如`Always don't run the server. i will start it by myself`可以不让claude自行启动服务器,而是由我们自己去启动

### 常用命令

- 使用/可以调用常用命令
- /status 查看模型等信息
- /init 可以创建CLAUDE.md文件
- /ide 添加IDE工具,例如vscode,需要先安装claude插件
    - 安装失败时,Cmd+Shift+P;Shell Command: Install 'code' command in PATH;重启vscode
    - 能够获取我当前窗口展示的文件所在的上下文环境
- /model 查看使用的模型
- /help 
- /clear 清除会话的上下文
- /compact 压缩会话的上下文,保留摘要
- /mcp 查看添加的mcp服务器
- /permissions 权限设置
- /hooks 钩子

### 使用技巧

##### 基础提示词

- give me an overview of this codebase
- @json-parser/ give me an overview of this codebase
- trace the process of handling a user‘s query from frontend to backend 追踪前后端的处理流程
- draw a diagram that illustrates this flow 画出流程图,可以借助D3.js或者Recharts等工具实现网页流程图的效果
- how do i run this application 给出运行程序的方式

##### 增删改查

- 基础
  - shift+tab 按两下 进入plan mode 按一下 进入自动接受所有编辑
  - 使用@引用文件;代码修改时,如果能正确引用文件,效率会更高效
  - \反斜杠,加回车enter,可以实现命令行的换行输入
- 修改
  - 可以直接截图后复制到命令行,然后让claude进行分析;前提是大模型需要支持
  - 结合playwright可以无需手动截图了,自动去修改什么内容,很方便
- 新增
  - 新增功能时,提示词可以参考这样写
```
总结性的标题,可以引用具体的文件
* 第一点:可以使用Functionality
 - input 输入的样子
 - output 应该输出的样子
* 第二点等等
```
  - 如果提示词很多,功能很复杂,重构性的内容时,可以写入一个md文件,提示词参考如下
```
总结性的标题
current behavior
desired behavior
example flow 示例流程,例如一个前后端交互的接口,具体的业务逻辑是什么样子的
requirements 一些具体的要求,比如希望本次更新完成的内容
notes 一些注意事项,例如是否应该写测试用例,应该修改哪些文件等
如果需要brainstorm,可以最后加上:
use two parallel subagents to brainstorm possible plan. do not implements any code
```
- 测试
  - 可以参考如下的提示词写法,去完善测试用例
  - think a lot 这句话触发了深度思考吗?
  - 也可以同时粘贴上报错信息,然后同步进行测试用例的完善
```
@json-parser/backend/ in this project,i need you to: 
1. write tests to evaluate @json-parser/backend/app/utils/json_utils.py correct
think a lot
```

##### 结合git

- 可以直接和git进行交互;无需再输入git命令
- add and commit this changes

##### 其他tips

- shift + 1 进入 bash mode
- &
- /btw by the way
- 粘贴两次的话,会展示原内容

### MCP

##### 概念

- 模型上下文协议
- 让claude可以访问其他的资源和系统,增强功能

##### 使用演示

- 添加: claude mcp add playwrite npx @playwright/mcp@latest
- 查看: /mcp
- 简单使用的提示词演示
```
using the playwright MCP server to visit http://localhost:5173/ 
view the '清空' button
i want change this button's color to yellow
```

### 多agent

TODO

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

### jupyter操作

- 可以将jupyter文件直接转换成仪表盘
- 使用streamlit转换成仪表盘

### figma操作

- 添加figma的mcp服务器 claude mcp add --transport http figma-dev-mode-mcp-server http://localhost:3000/mcp
- 需要专业版账号

# skill使用指南

### 概述

- skill的name和description在agent的context中,但是直到用户的请求匹配到了description才会加载这个skill
- 读写文件目录的权限,以及一个批处理工具去执行代码
- 打包zip
- 渐进式披露:避免污染context,只加载必要的数据
```
create-table-skill/
├── SKILL.md
│   ├── name
│   ├── description
├── references
│   ├── a.md
├── scripts
│   ├── b.sh
├── assets
```

### 结合tools,MCP,子agent使用

![alt text](image.png)
