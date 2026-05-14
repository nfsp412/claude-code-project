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

- 常规性的新增功能,如果新增多个功能时,按照功能1功能2的方式写清晰md文件即可

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
- add and commit all changes
- 可以使用git的work tree 功能实现并行开发
    - 创建 .trees 文件
    - 执行 git worktree add .trees/ui_feature git worktree add .trees/test_feature 例如这样的命令
    - git branch -a 可以验证
    - 各自提交git后,在主分支进入claude进行合并
    - 然后进入主分支的claude后,让claude进行合并
- use 'git merge' command to merge all of the worktrees in the .trees folder and fix any conflict if there are any

##### 自定义命令

- 目录: .claude/commands/xxx.md
- 这个xxx就是可以通过斜杠调用的命令
- 通过 $ARGUMENTS 可以接收传参
- 这个文件不会像是claude.md文件一样添加到上下文中,所以如果有些要求是只需要在特定的某些会话中触发,使用这种方式就比较合适了

##### 其他tips

- shift + 1 进入 bash mode
- &
- /btw by the way
- 粘贴两次的话,会展示原内容
- [text](.claude/settings.local.json) 该文件可以定义无需询问获取权限的命令
- claude --resume 可以选择进入哪一次的会话中

### 多会话并行开发

##### 演示如何进行多会话并行开发

- 自定义一个命令,例如 [text](.claude/commands/implements-features.md) 该命令用来方便的进行功能新增
- 借助git的work tree功能实现并行开发
- 开启了多个终端后,进入多个claude命令行,然后并行开发
- 各自提交git后,在主分支进入claude进行合并;合并方式详见上文

### 钩子集成

- /hooks
- 有触发钩子的不同生命周期位置
- 演示示例
    - 选择post tool use 工具使用后触发钩子
    - 选择 Read 命令,代表执行该命令后触发钩子
    - 钩子设置为 say 'All Done'
    - 注意需要添加到 `./.claude/settings.json` 文件 或者 settings.local.json中

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

##### 钩子使用的例子

- 在PreToolUse生命周期进行分支创建
- 在PostToolUse生命周期进行打包提交测试分支

# MCP

### 概念

- 模型上下文协议
- 让claude可以访问其他的资源和系统,增强功能

### playwrite

- 添加: claude mcp add playwrite npx @playwright/mcp@latest
- 查看: /mcp
- 简单使用的提示词演示

```
using the playwright MCP server to visit http://localhost:5173/
view the '清空' button
i want change this button's color to yellow
```

### figma

- 命令行安装内置的figma插件 claude plugin install figma@claude-plugins-official
- 可以在claude中文字性描述,直接生成figma设计稿,例如下面;claude会触发两个skill figma:figma-generate-design 和 figma:figma-use

```
我正在做一个datax任务配置监控调度的web产品,请在figma中帮我设计,需要包含
- 顶部导航栏
- 侧边栏
- 右侧内容展示区域
其中顶部导航栏需要包含:
- 登录用户名称
- 所属hdfs账号名称
- logo
其中侧边栏需要包含:
- 任务监控仪表盘
- 任务管理:子菜单包含:任务明细列表;任务构建
- 调度管理
- 数据源管理
- 日志查询
- datax执行集群管理
- 资源使用情况监控仪表盘
- json格式化小工具
侧边栏每一项功能需要包含哪些具体的细节,暂时先不进行设计
整体风格:科技感，深色模式
使用Tailwind UI风格
```

- tips
    - 我有一个 JSON 结构（粘贴你的 HDFS 监控 API 返回值），请根据这个结构在 Figma 里设计一个数据卡片 这段话告诉我,可以根据数据格式,让claude去构建figma
    - 使用 Ant Design 的组件规范，为我画一个配置 Kafka 集群的表单页面 这段话告诉我,可以使用现有的ui组件库,例如Tailwind UI Ant Design

> 关于Ant Design,Tailwind UI,Element-Plus UI的区别和联系
> Ant Design 本质是组件库,React / Vue 组件 + 封装好的逻辑,统一、严谨、企业级(阿里味)
> Tailwind UI UI 模式库,HTML + Tailwind CSS 类名,现代、精致、高度可定制
> Element-Plus UI Vue 3 专属,预封装组件库 (node_modules),封装好的 CSS（通过 Props 修改）,内置（弹窗、分页、校验全自带）等交互功能

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

![alt text](static/image.png)
