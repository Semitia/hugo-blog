---
title: WSL2
date: 2026-02-16
description: Simple usage of WSL2
summary: Simple usage of WSL2
tags: ["WSL2", "linux"]
---
![file-20260216214951136.webp](/img/Posts/Linux/WSL2/file-20260216214951136.webp)

# 安装
 
> 微软官方教程
> [Windows Subsystem for Linux 文档 | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/wsl/)
> 
> [旧版 WSL 的手动安装步骤 | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)
> 
> 知乎
> [Windows安装和配置Linux子系统（WSL2） - 知乎](https://zhuanlan.zhihu.com/p/1903903315080774656)

安装完wsl后可以通过 Microsoft Store 下载 linux 发行版，但其似乎不走代理，网络总是有问题（也可能是其他问题），试了很多方法还是打不开。
干脆直接使用命令行下载。

加上 `--web-download` 参数，会强制从 GitHub/微软服务器直接下载内核和发行版，而**不走微软商店**。

打开**管理员** PowerShell，运行：

```
wsl --install -d Ubuntu-24.04 --web-download
```

- 这会自动开启 WSL 组件、下载 Ubuntu 24.04 并安装。
    
- 安装完后重启电脑，它会自动弹出终端让你设置用户名密码。

# 网络配置

现在的版本似乎强调wsl与windows共享本地网络。初次打开时会有这样的警告
```bash
wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。
```

#### 方法一：开启“镜像网络模式” (推荐，仅限 Windows 11 22H2 及以上)

这是目前最完美的解决方案。它会让 WSL 和 Windows 共享同一个网络接口（包括 localhost）。

1. 在 Windows 文件资源管理器地址栏输入 `%UserProfile%` 并回车。
    
2. 找到或新建一个名为 `.wslconfig` 的文件（注意前面有点）。
    
3. 用记事本打开，输入以下内容并保存：
    
    Ini, TOML
    
    ```
    [wsl2]
    networkingMode=mirrored
    autoProxy=true
    ```
    
4. 打开 PowerShell (CMD)，输入 `wsl --shutdown` 重启 WSL。
    
5. 再次进入 WSL，这个警告应该消失了，且网络与 Windows 完全互通。

如果想要wsl也能走clash代理，在之前我使用的方法是：

1. clash打开 **Allow LAN**
2. 在powershell通过 `ipconfig` 获取windows IP
3. 给wsl添加网络配置

```jsx
echo 'export http_proxy="<http://192.168.xxx.xxx:7890>"' >> ~/.bashrc
echo 'export https_proxy="<http://192.168.xxx.xxx:7890>"' >> ~/.bashrc
echo 'export all_proxy="socks5://192.168.xxx.xxx:7891"' >> ~/.bashrc
source ~/.bashrc
```

# 图形化配置

## 使用VcXsrv

[Win11 + WSL2 搭建 ros + gazebo 环境以及通过 VcXsrv 在 WSL2 上使用图形化界面（xfce4）_windows11 wsl ros2-CSDN博客](https://blog.csdn.net/qq_51908382/article/details/140607102)

### 步骤 1：下载安装 VcXsrv

1. **下载 VcXsrv**：目前无法直接通过WSL命令行下载并安装VcXsrv，需手动下载。可以访问 [VcXsrv的官方网站](https://sourceforge.net/projects/vcxsrv/) 下载最新的安装程序（`vcxsrv-64.X.XX.XX.exe`）。
2. **运行安装程序**：下载后，双击安装程序并按提示完成安装。一般来说，默认设置已经足够。

### 步骤 2：配置 VcXsrv

1. **启动 VcXsrv**：
    - 在Windows开始菜单中找到 "XLaunch" 并启动它。
    - **配置选项**：
        - **Display settings**: 选择 "Multiple windows"。
        - **Client startup**: 选择 "Start no client"。
        - **Extra settings**: 勾选 "Disable access control"（如果你信任局域网环境，这样可以允许连接，不受限于特定主机）。
2. **保存配置文件**（可选）：
    - 在启动配置最后一步，可以选择保存配置，以便下次快速启动。

### 步骤 3：在 WSL 中设置 DISPLAY 变量

为了让WSL中的Linux应用程序能够连接到VcXsrv的图形界面，需要配置环境变量 `DISPLAY`。

1. 打开 WSL 终端，并编辑 `~/.bashrc` 文件：
    
    ```bash
    nano ~/.bashrc
    ```
    
2. 在文件末尾添加以下内容：
    
    ```bash
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
    ```
    
    这条命令会自动获取你的Windows主机IP，并设置 `DISPLAY` 环境变量，以便于每次连接X Server时自动使用最新的主机IP。
    
3. **应用更改**：
    
    - 保存并关闭 `~/.bashrc` 文件，然后运行以下命令应用更改：
        
        ```bash
        source ~/.bashrc
        ```
        

### 步骤 4：验证设置

1. 在WSL中，安装一些简单的图形界面应用来测试设置，例如 `xclock`：
    
    ```bash
    sudo apt update
    sudo apt install x11-apps
    ```
    
2. 运行 `xclock` 以测试：
    
    ```bash
    xclock
    ```
    
    如果安装和配置正确，应该会在Windows桌面上显示一个时钟窗口。
    

## WSLg

最新版的wsl支持图形化显示了

### 步骤 1：关闭所有 WSL 实例

在更新前，最好关闭所有正在运行的 WSL 实例，以确保更新过程顺利进行。

```powershell
wsl --shutdown
```

### 步骤 2：更新 WSL 核心和 WSLg

在 PowerShell 或 CMD 中运行以下命令来检查和更新 WSL 核心和 WSLg：

```powershell
wsl --update
```

如果 `wsl --update` 成功运行，系统会自动下载并安装最新的 WSL 组件，包括内核和 WSLg。

### 步骤 3：检查 WSL 版本

完成更新后，可以通过以下命令确认是否已成功安装最新的 WSL、内核和 WSLg 版本：

```powershell
wsl --version
# 老版本不支持上面的命令，可以用下面的
wsl --status 
```

应该可以看到 WSL 版本、内核版本、WSLg 版本等信息：

### 手动更新

如果 `wsl --update` 无法正常更新（我的就是），可以手动下载并安装内核更新文件：

1. 访问 [WSL2 内核更新页面](https://aka.ms/wsl2kernel)。
2. 下载 `.msi` 文件并运行它来更新内核。

安装完毕后可以看到类似输出

```bash
alexavier@DESKTOP-6SOFPUI:~$ echo $WAYLAND_DISPLAY
wayland-0
alexavier@DESKTOP-6SOFPUI:~$ echo $DISPLAY
:0
alexavier@DESKTOP-6SOFPUI:~$ echo $XDG_RUNTIME_DIR
/run/user/1000/
```

### **方法 2：编辑配置文件**

如果 `gsettings` 不可用，你可以直接编辑 GTK 配置文件来修改鼠标指针大小。

1. 打开或创建配置文件：
    
    ```bash
    bash
    复制代码
    nano ~/.Xresources
    
    ```
    
2. 添加以下内容：
    
    ```bash
    bash
    复制代码
    Xcursor.size: 48
    
    ```
    
3. 保存文件并刷新配置：
    
    ```bash
    bash
    复制代码
    xrdb ~/.Xresources
    
    ```
    
4. 重新启动 WSL 或 X11 环境后，鼠标指针大小会更新。
    

# 开发工具

## Vscode

运行windows上的vscode，安装**Remote-WSL**插件。

[Remote development in WSL](https://code.visualstudio.com/docs/remote/wsl-tutorial)

## Docker
**安装 Docker：** 在 WSL 2 里运行原生 Docker 安装脚本（`curl -fsSL https://get.docker.com | sh`）。
等脚本跑完回到命令行提示符（`$`）后，为了以后不用每次输 `sudo docker`，请务必执行下面这两行命令：

Bash

```
# 1. 把你的用户加入 docker 用户组
sudo usermod -aG docker $USER

# 2. 刷新用户组（或者直接重启 WSL 窗口）
newgrp docker
```

之后你可以输入 `docker run hello-world` 测试是否安装成功。