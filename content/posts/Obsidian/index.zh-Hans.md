---
title: Obsidian
date: 2026-02-16
description: Simple usage of Obsidian
summary: Simple usage of Obsidian
tags: ["Obsidian"]
---
![file-20260216220629548.webp](/img/posts/Tools/Obsidian/file-20260216220629548.webp)

# Links

[想一小时上手obsidian？这一篇就够了。【玩转Obsidian的保姆级教程】 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/428519519)


# 基本功能
[Obsidian显示大纲的方法_obsidian 大纲-CSDN博客](https://blog.csdn.net/csdn2683/article/details/138413414)


## 基本语法
### 标签
在 Obsidian 中，`#` 后面紧接内容表示 **标签（Tag）**，语法格式为：  
`#标签名`  

#### 主要特点：
1. **标签的作用**  
   - 用于分类和关联笔记（类似关键词标记）。  
   - 可以通过点击标签快速筛选相关笔记。  
   - 支持层级标签（如 `#编程/Python`）。  

2. **弹出候选框的原因**  
   - 当你输入 `#` 时，Obsidian 会**自动搜索现有标签**并显示匹配的候选列表（其他笔记用过的标签）。  
   - 这是为了帮助快速输入已有标签，避免重复创建语义相同的不同标签（如 `#python` 和 `#Python`）。  

3. **补充用法**  
   - **子标签**：用 `/` 分隔层级（如 `#学习/数学`）。  
   - **标签内不允许空格**：需用连字符或驼峰命名（如 `#时间管理` 或 `#TimeManagement`）。  
   - **标签搜索**：在搜索栏输入 `tag:#标签名` 可定位所有带该标签的笔记。  

#### 示例：
- 输入 `#健身` → 弹出包含 `#健身/跑步`、`#健身/力量训练` 等候选标签。  
- 输入 `#项目/` → 显示所有以 `#项目/` 开头的子标签。  

如果需要关闭自动补全，可在设置中调整：  
`设置 → 编辑器 → 智能补全 → 关闭标签补全`。


# 插件
直接在内置插件商店就能下载使用
## Attachment Management
![[IMG-20260215222233180.webp]]
这里新建了一个名为“Attachment”的文件夹统一管理附件，其他就默认配置，具体效果就是：
*一篇笔记相对vault目录的路径* 和 *其附件相对Attachment的路径*是一样的。

不过这个插件似乎有**神秘BUG**，改用 **‘Custom Attachment Location’** 了

## Custom Attachment Location


