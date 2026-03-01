---
title: Docker Note
date: 2025-01-21
description: Practical usage of Docker.
summary: Practical usage of Docker.
tags: ["Docker"]
---

![IMG-20250121235045541.webp](/img/Posts/Tools/Docker%20Note/IMG-20250121235045541.webp)

## 安装与配置

---

### 1. 安装 Docker

#### 步骤 1：更新系统包

确保系统的包是最新的：

```bash
sudo apt update
sudo apt upgrade -y
```

#### 步骤 2：安装 Docker

运行以下命令以安装 Docker：

```bash
sudo apt install docker.io -y
```

#### 步骤 3（可选）：启动和设置 Docker 服务

启动 Docker 并将其设置为开机自启动：

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

#### 步骤 4：验证 Docker 是否安装成功

运行以下命令检查 Docker 版本：

```bash
docker --version
```

输出类似于 `Docker version xx.xx.xx` 表示安装成功。

### 配置 Docker 使用代理

创建配置文件并添加代理设置：

1. 创建或编辑 Docker 服务的配置文件：
   
   ```bash
   sudo mkdir -p /etc/systemd/system/docker.service.d 
   sudo gedit /etc/systemd/system/docker.service.d/http-proxy.conf
   ```

2. 在 `http-proxy.conf` 文件中添加以下内容：
   
   ```bash
   [Service] 
   Environment="HTTP_PROXY=http://127.0.0.1:7890/" 
   Environment="HTTPS_PROXY=http://127.0.0.1:7890/" 
   Environment="NO_PROXY=localhost,127.0.0.1"
   ```

3. 重新加载系统守护进程配置并重启 Docker 服务：
   
   ```bash
   sudo systemctl daemon-reload 
   sudo systemctl restart docker
   ```

### 添加用户组

避免每次使用docker都需要sudo

[Post-installation steps | Docker Docs](https://docs.docker.com/engine/install/linux-postinstall/)

用户名似乎需要小写

```bash
alexavier@alexavier:~$ sudo usermod -aG docker Alexavier
usermod：用户“Alexavier”不存在
alexavier@alexavier:~$ sudo usermod -aG docker alexavier
```

配置完似乎还需要重启/重新登录一下vscode插件才能用

## 常用操作

### 拉取镜像

```bash
docker pull osrf/ros:noetic-desktop-full
```

### 查看本地镜像

```bash
docker images
```

### 查看运行中的容器

```bash
docker ps
```

### 查看所有容器（包括已停止的容器）

```bash
docker ps -a
```

### 启动容器

如果多个容器共用同一个镜像，镜像的只读部分会被共享，**不会重复占用空间**。

```bash
docker run -it my_noetic:7_26 /bin/bash

docker run -it --network host my_noetic:7_26 /bin/bash

docker run -it --network host -v ~/SumResearch_2024/Repo/Host/ROS1_ws:/root/ROS1_ws my_noetic:latest /bin/bash

docker run -it --network host -v ~/SumResearch_2024/Repo/Host/ROS1_ws:/root/ROS1_ws -v ~/SumResearch_2024/Repo/RDKx5:/root/RDKx5 arm_noetic:latest

docker run -it --network host -v ~/SumResearch_2024/Repo/Host/ROS1_ws:/root/ROS1_ws -v ~/SumResearch_2024/Repo/RDKx5:/root/RDKx5 --privileged --device /dev/ttyUSB0 arm_noetic:latest
```

### 启动新的shell会话

找到运行中的容器ID或者容器名，假如为my_noetic_container

```bash
docker exec -it my_noetic_container /bin/bash
```

### 关闭容器

```bash
docker kill <container_name_or_id>
```

### 保存容器为镜像

```bash
docker commit youthful_khayyam airbot_img:latest
```

### 查看容器的空间占用

```bash
docker system df
```

### 查看镜像信息

```bash
docker inspect b56b435576e8
```

### 本地保存和加载 Docker 镜像

将 Docker 镜像保存为一个文件，然后在其他地方加载这个文件。

##### 保存镜像

使用 `docker save` 命令将镜像保存为 tar 文件：

```bash
docker save -o my-ubuntu-image.tar my-ubuntu-image
```

##### 加载镜像

```bash
docker load -i my-ubuntu-image.tar
```

### 删除镜像和容器

- **删除容器**：
  
  ```bash
  docker rm <container_id_or_name>
  ```

- **删除镜像**：
  
  ```bash
  docker rmi <image_id_or_repository:tag>
  ```

### 文件操作

#### 复制到容器

```bash
docker cp ~/SumResearch_2024/Repo/Host/ROS1_ws youthful_khayyam:/home/
```

## GUI配置

### 主机

安装x11

```bash
sudo apt update
sudo apt install xserver-xorg xauth
```

验证功能

```bash
xeyes
```

授予权限

```bash
xhost +local:
```



### 容器

建议使用compose打开容器，具体内容可参考后面的

安装x11

```bash
apt update
apt install -y x11-apps
```

测试

```bash
xeyes
```



## Dockerfile

### 文件示例

Dockerfile 是一个文本文件，包含了一系列指令，用于定义如何构建 Docker 镜像。假设你想要创建一个包含基本 Ubuntu 系统的 Docker 镜像，可以创建一个简单的 Dockerfile：

```Dockerfile
# 使用官方的 Ubuntu 镜像作为基础镜像
FROM ubuntu:20.04

# 维护者信息
LABEL maintainer="your_email@example.com"

# 更新包列表并安装一些基础工具
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    git \
    && apt-get clean

# 设置工作目录
WORKDIR /root

# 复制你的系统配置文件（可选）
# COPY my_config_file /root/my_config_file

# 安装其他软件或进行其他配置（根据需要）
# RUN ...

# 默认命令
CMD ["bash"]
```

你可以根据自己的需求在 Dockerfile 中添加更多指令，例如安装其他软件、复制文件等。

### 使用 Docker 构建镜像

在 Dockerfile 所在的目录，打开终端并运行以下命令构建 Docker 镜像：

```bash
docker build -t my-ubuntu-image .
```

其中 `my-ubuntu-image` 是你给镜像指定的名字，`.` 表示 Dockerfile 在当前目录。

 

## Docker Compose

Docker Compose 使用一个 YAML 文件来定义和管理多个容器，从而简化命令行操作。

### 旧版内容（ubuntu 24.04及以后不用看）
#### 安装

[Docker Compose 的官方文档](https://docs.docker.com/compose/install/)

[Docker Compose | 菜鸟教程](https://www.runoob.com/docker/docker-compose.html)

#### 使用方法

在项目根目录下创建一个 `docker-compose.yml` 文件，并在其中添加以下内容：

```yaml
version: '3.8'

services:
  arm_noetic:
    image: arm_noetic:latest
    container_name: arm_noetic_container
    network_mode: host
    volumes:
      - ~/SumResearch_2024/Repo/Host/ROS1_ws:/root/ROS1_ws
      - ~/SumResearch_2024/Repo/RDKx5:/root/RDKx5
    privileged: true
    devices:
      - "/dev/ttyUSB0:/dev/ttyUSB0"
    stdin_open: true
    tty: true
```

在这个文件中：

- `version` 指定了 Docker Compose 文件的版本。
- `services` 部分定义了一个服务（即容器），这里命名为 `arm_noetic`。
- `image` 指定了要使用的 Docker 镜像。
- `container_name` 为容器指定了一个名字。
- `network_mode` 设置为 `host`，与 `--network host` 参数相同。
- `volumes` 定义了需要挂载的卷。
- `privileged` 设置为 `true`，使容器具有特权。
- `devices` 部分指定了需要共享的设备。
- `stdin_open` 和 `tty` 设置为 `true`，以启用交互模式。

在 `docker-compose.yml` 所在的目录下，使用以下命令以后台模式启动容器：

```sh
docker-compose up -d
```



### 安装

  在使用24.04的时候，`docker-compose` 用不了，因为 `docker-compose` 1.x 版本依赖 `distutils`，而 `distutils` 在Python 3.12 中被移除。新版 `docker-compose` 已转为使用 Go 实现 (`docker-compose-plugin`)，不再依赖 Python。所以使用新版的 **'docker compose plugin'**
  
```bash
sudo apt remove docker-compose
sudo apt update 
sudo apt install -y ca-certificates curl gnupg lsb-release

# 添加docker官方 GPG 密钥
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg 
sudo chmod a+r /etc/apt/keyrings/docker.gpg 

# 添加 Docker 软件源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null 

# 更新&验证
sudo apt update
sudo apt install docker-compose-plugin
docker compose version
```

新版命令中间没有连字符，是 `docker compose`，而不是 `docker-compose`

相应的，compose 具体内容似乎也要稍微修改（文件名不变）

```yml
version: '3.8'

services:
	graspnet:
		image: nvidia/cuda:12.1.0-devel-ubuntu22.04 # 使用你下载的镜像
		container_name: graspnet-container
		network_mode: host
		environment:
			- NVIDIA_VISIBLE_DEVICES=all # 显示所有 GPU（可指定 GPU）
			- NVIDIA_DRIVER_CAPABILITIES=all
			- DISPLAY=${DISPLAY} # 支持可视化
			- QT_X11_NO_MITSHM=1 # 防止 Qt 报错
			- HTTP_PROXY=http://127.0.0.1:7890 # Clash 代理端口
			- HTTPS_PROXY=http://127.0.0.1:7890
		volumes:
			- ~/graspnet:/workspace # 挂载本地 ~/graspnet 到容器内 /workspace
			- /media/user/disk/dataset/graspnet:/workspace/dataset
			- /tmp/.X11-unix:/tmp/.X11-unix # 共享 X11 的 Unix socket，支持 GUI
		privileged: true
		working_dir: /workspace # 容器内的默认工作目录
		stdin_open: true # 支持交互式会话
		tty: true # 启用终端
		deploy:
			resources:
				reservations:
					devices:
						- capabilities: [gpu]
```

### 命令
新版命令也发生了细微变化，少了连字符，在 `docker-compose.yml` 所在的目录下执行

```bash
docker compose up -d
```

**注意**，这个方法会删除已有的同名容器，并用镜像**重新创建**容器。如果只是启动**已经存在但处于停止状态**的容器，使用以下命令：

```bash
docker compose start
```

```bash
# 查看容器是否活着：
docker compose ps
# 查看实时日志：
docker compose logs -f
# 停止服务：
docker compose down
```

## 容器内使用显卡

为了支持 GPU，需要安装 NVIDIA Container Toolkit。

#### 设置 NVIDIA Docker 存储库

添加 NVIDIA 的 GPG 密钥和存储库：

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```

#### 安装 NVIDIA Container Toolkit

更新包列表并安装：

```bash
sudo apt update
sudo apt install -y nvidia-docker2
# 下载太慢也可以走代理
sudo apt -o Acquire::http::Proxy="http://127.0.0.1:7890" \
         -o Acquire::https::Proxy="http://127.0.0.1:7890" install -y nvidia-docker2
```

#### 重启 Docker 服务

```bash
sudo systemctl restart docker
```

#### 验证 NVIDIA Docker 是否可用

运行以下命令检查 GPU 是否可以被 Docker 访问：

```bash
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi

# 监控GPU使用情况
sudo apt install gpustat
gpustat --watch
```

如果显示GPU 信息，说明安装成功。

#### Ubuntu 24.04版本
目前（2024.12.15）NVIDIA Container Toolkit 还不支持 ubuntu 24.04,不过也能下载，参考:
> https://www.server-world.info/en/note?os=Ubuntu_24.04&p=nvidia&f=3

总结一下
```bash
# 更新依赖和系统
sudo apt update
sudo apt install -y curl apt-transport-https ca-certificates software-properties-common

# 添加 NVIDIA GPG 公钥
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-toolkit.gpg

# 添加 NVIDIA 容器工具包源
curl -fsSL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
sudo tee /etc/apt/sources.list.d/nvidia-toolkit.list
sudo sed -i -e "s/^deb/deb [signed-by=\/usr\/share\/keyrings\/nvidia-toolkit.gpg]/g" /etc/apt/sources.list.d/nvidia-toolkit.list

# 更新包索引和安装工具包
sudo apt update
sudo apt install -y nvidia-container-toolkit

# 重启 Docker 并测试
sudo systemctl restart docker
sudo docker run --rm --gpus all nvidia/cuda:12.3.0-runtime-ubuntu22.04 nvidia-smi
```

---

### 拉取 CUDA 11.8 镜像

https://hub.docker.com/r/nvidia/cuda/tags

选择适合的镜像并运行：

```bash
sudo docker pull nvidia/cuda:11.8.0-base-ubuntu22.04
```

---

### 运行容器

使用 CUDA 镜像启动容器并验证 CUDA 是否可用：

```bash
docker run --rm --gpus all -it nvidia/cuda:11.8-base-ubuntu22.04 bash
```

或者用compose

```yaml
version: '3.8'

services:
  graspnet:
    image: pytorch/pytorch:2.2.0-cuda11.8-cudnn8-devel # 使用你下载的镜像
    container_name: graspnet-container
    network_mode: host
    runtime: nvidia # 启用 GPU 支持（需安装 NVIDIA Container Toolkit）
    environment:
      - NVIDIA_VISIBLE_DEVICES=all # 显示所有 GPU（可指定 GPU）
      - NVIDIA_DRIVER_CAPABILITIES=all
      - DISPLAY=${DISPLAY}         # 支持可视化
      - QT_X11_NO_MITSHM=1         # 防止 Qt 报错
      - HTTP_PROXY=http://127.0.0.1:7890  # Clash 代理端口
      - HTTPS_PROXY=http://127.0.0.1:7890
    volumes:
      - ~/graspnet:/workspace      # 挂载本地 ~/graspnet 到容器内 /workspace
      - /media/alexavier/8018420DD8B69548/dataset/graspnet:/workspace/dataset 
      - /tmp/.X11-unix:/tmp/.X11-unix # 共享 X11 的 Unix socket，支持 GUI
    privileged: true  
    working_dir: /workspace        # 容器内的默认工作目录
    stdin_open: true               # 支持交互式会话
    tty: true                      # 启用终端
```

#### **验证环境**：

在容器中运行以下命令：

```bash
nvidia-smi
```

由于nvcc是devel版本才有的工具，没法用`nvcc -V`，如果不需要开发cuda程序，只是运行程序时会用到可以只用base



---

## 其他问题

### 共享卷导致的git权限问题（可能）

类似这样的

```bash
❯ git pull
error: unable to create file RDKx5/hand/servo_limit.json: 权限不够
```

确保用户拥有整个 Git 仓库的文件和目录的所有权

```bash
sudo chown -R $USER:$USER ~/SumResearch_2024/Repo
```

### 容器配置主机代理

长期配置可在compose添加

```bash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
# test
curl -I https://www.google.com
```

### Vscode开发

#### VSCode Remote - Containers 插件

#### 修改共享目录权限

> 无法写入文件"/home/semitia/SumResearch_2024/Repo/Host/ROS1_ws/src/hand_control/src/hand_ctrl.py"(NoPermissions (FileSystemError): Error: EACCES: permission denied, open '/home/semitia/SumResearch_2024/Repo/Host/ROS1_ws/src/hand_control/src/hand_ctrl.py')

在宿主机上修改挂载目录的权限，使其对所有用户都可写：

```bash
chmod -R 777 ~/SumResearch_2024/Repo/Host/ROS1_ws
```
