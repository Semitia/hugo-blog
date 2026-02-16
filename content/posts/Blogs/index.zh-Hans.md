---
title: Blogs
date: 2025-01-21
description: Blog configuration with common frameworks.
summary: Blog configuration with common frameworks.
tags: ["Blog", "Hugo", "Obsidian"]
---

![IMG-20250121234134792.webp](/img/posts/Tools/Blogs/IMG-20250121234134792.webp)

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