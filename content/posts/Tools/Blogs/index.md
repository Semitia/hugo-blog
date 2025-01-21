---
title: Blogs
date: 2025-01-21
description: Blog configuration with common frameworks.
summary: Blog configuration with common frameworks.
tags: ["Blog", "Hugo"]
---

![IMG-20250121234134792.png](/img/posts/Tools/Blogs/IMG-20250121234134792.png)

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


### 容器开发

docker compose 文件

```yaml
services:
  myHugo:
    image: hugomods/hugo:reg-exts
    container_name: Hugo-container
    network_mode: host
    environment:       
      - HTTP_PROXY=http://127.0.0.1:7890  
      - HTTPS_PROXY=http://127.0.0.1:7890
    volumes:
      - ~/Blogs/Hugo:/src
    privileged: true  
    working_dir: /src
    stdin_open: true              
    tty: true              
    command: server -D -p 1313 --bind 0.0.0.0
```

启动容器

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
![[IMG-20250114162457070.png]]

### 绑定域名

在Hugo项目管理中点击Domain，添加域名。
按照vercel给出的配置，在域名提供商那里修改域名DNS配置即可。

![[IMG-20250114162457092.png]]![[IMG-20250114162457143.png]]


## 自动部署脚本
