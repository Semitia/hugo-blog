---
title: Blogs
date: 2025-01-21
description: Blog configuration with common frameworks.
summary: Blog configuration with common frameworks.
tags: ["Blog", "Hugo", "Obsidian"]
---

![IMG-20250121234134792.webp](/img/Posts/Tools/Blogs/IMG-20250121234134792.webp)

# Hugo

## 环境配置

使用docker开发

```bash
docker pull hugomods/hugo:ci
```

### 创建Hugo网页项目

如果已有Hugo项目可跳过

```bash
mkdir Hugo
cd Hugo
docker run --rm -it \
    -v $(pwd):/src \
    hugomods/hugo:ci new site .
```

 拉取主题

```bash
sudo git -c http.proxy=http://127.0.0.1:7890 submodule add -b stable https://github.com/jpanther/congo.git themes/congo
```

根据主题配置文档更换网页项目内容

> https://jpanther.github.io/congo/docs/installation/#create-a-new-site

也可以继续参考文档个性化定制

> https://jpanther.github.io/congo/zh-hans/docs/getting-started/

#### congo主题

这个主题想要让文章标题侧边显示图片，图要在笔记同目录下添加**cover/thumb/feature命名**的图片；同时，必须有index.md，不能只有一个index.zh-Hans.md。

### 克隆已有仓库
除了克隆已有博客仓库，还需要克隆**主题**
这里是更新子模块：

```bash
git submodule update --init --recursive
```

## 容器开发

`docker-compose.yml` 文件(位于博客项目根目录)
**镜像选择：**
- 要指定老版本，因为这个代码有点老了；
- 要选拓展版，`exts`标签的意思是有额外工具；在这个作者这里，要选不是`reg`和`std`的。

```yaml
services:
  myHugo:
    image: hugomods/hugo:exts-0.145.0
    container_name: Hugo-container
    network_mode: host
    environment:      
      - HTTP_PROXY=http://127.0.0.1:7890  
      - HTTPS_PROXY=http://127.0.0.1:7890
    volumes:
      - .:/src  # 将yml当前目录挂载到容器的/src目录
    privileged: true  
    working_dir: /src
    stdin_open: true              
    tty: true              
    command: server -D -p 1313 --bind 0.0.0.0
```

在根目录运行，启动容器

```bash
docker compose up -d
```

此时，没有报错的情况下可以通过浏览器访问 `http://localhost:1313/`查看效果



## 常用操作

如果出现了谜之问题，比如缩略图不更新，文章不出现等，可以尝试删掉**public目录**（缓存），重新生成。

你的直觉非常敏锐！那个“隐形的联系”其实非常简单粗暴——**文件名匹配**。

在 Congo 主题中，逻辑是这样的： 当你写 `{ github = "..." }` 时，主题会去 `assets/icons/` 文件夹里找有没有叫 `github.svg` 的文件。如果有，就渲染出来；如果没有，就显示空白或方框。

所以，要实现 Bilibili、Tools（工具箱）、Games（游戏手柄）的图标，你只需要做两步：**找图标** -> **改配置**。

### 第一步：准备图标文件 (SVG)

你需要把对应的 SVG 文件放到你的博客根目录下的 `assets/icons/` 文件夹里（如果没有 `icons` 文件夹就新建一个）。

**操作流程：**

1. **找到 `assets` 文件夹**：在你的 `semitia-blog` 根目录下（注意：**不要**去 `themes/congo/assets`，要在你自己的根目录下找，这样升级主题不会丢文件）。
    
2. **新建 `icons` 文件夹**：路径应为 `你的博客根目录/assets/icons/`。
    
3. **下载并放入 SVG**：
    
    - **Bilibili**: 去 下载 Bilibili 的 SVG，重命名为 **`bilibili.svg`**，放入上述文件夹。
        
    - **Tools**: 找一个工具箱图标（推荐 ），下载 SVG，重命名为 **`tools.svg`**，放入文件夹。
        
    - **Games**: 找一个游戏手柄图标，重命名为 **`gamepad.svg`**，放入文件夹。
        

_(小提示：为了让图标颜色随主题变化，你可以用记事本打开 SVG 文件，把里面的 `fill="..."` 属性删掉，或者改成 `fill="currentColor"`。Congo 会自动给它们上色。)_

### 第二步：修改 `languages.zh-Hans.toml`

现在文件有了，你只需要在配置文件里用**文件名（不带后缀）**作为 key 即可。

修改你的配置如下：

### 为什么之前的 GitHub 能显示？

因为 Congo 主题的文件夹里（`themes/congo/assets/icons/`）已经内置了 `github.svg`、`youtube.svg` 等常用图标。Hugo 的查找逻辑是：**先找你自己根目录下的 `assets`，找不到再去主题目录找。**

所以，只要你放入了同名的 SVG，你甚至可以覆盖掉默认的 GitHub 图标！

### 总结

1. **文件即钥匙**：文件名叫什么，配置文件里的 key 就写什么。
    
2. **位置**：放进 `assets/icons/`。
    

快去试试把 Bilibili 的小电视点亮吧！📺



## vercel

### 建立vercel项目

在Hugo仓库添加vercel的配置文件

将Hugo仓库上传到github，之后在Vercel上绑定github账号

在vercel新建项目(new project)，选择Hugo仓库

Framework Preset 可以直接选择Hugo

Root Directory 不用修改


### 绑定域名

在Hugo项目管理中点击Domain，添加域名。

按照vercel给出的配置，在域名提供商那里修改域名DNS配置即可。

## 自动部署脚本

目前使用自动脚本将obsidian特定文件夹下的笔记修改同步到hugo目录，不过如果想给类似`post`的目录添加`_index.md`页面，需要将笔记平铺在其同级，如
```
|-content
| |-post
| |-_index.md
| |-note_dir
| | |-index.md
| | |-thumb.jpg
```

同时发现这样才能正常显示文章summary
