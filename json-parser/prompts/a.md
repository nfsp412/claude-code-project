
> @json-parser/frontend/ 该项目中,需要将页面上的压缩按钮的功能,进行如下的修改

# current behavior

- 点击'压缩'按钮后,会压缩json字符串,但是再次点击该按钮,没有触发任何事情

# desired behavior

- 再次点击'压缩'按钮,应该恢复到被压缩之前的样子

# example flow 

- 用户第一次点击'压缩'按钮,json被压缩
- 用户第二次点击'压缩'按钮,页面上应该展示的是json被压缩之前的样子

# requirements 

- 参考上述的内容,完成这个'压缩'按钮重复点击的功能

# notes 

- 不要修改 @json-parser/backend/ 后端的代码,应该全部由前端来实现该功能

use two parallel subagents to brainstorm possible plan. do not implements any code