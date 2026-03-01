---
title: WSL2
date: 2026-02-16
description: Simple usage of WSL2
summary: Simple usage of WSL2
tags: ["WSL2", "linux"]
---
![file-20260216214951136.webp](/img/Posts/Linux/WSL2/file-20260216214951136.webp)

# Installation
 
> Microsoft Official Tutorial
> [Windows Subsystem for Linux Documentation | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/)
> 
> [Manual Installation Steps for Older WSL Versions | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)
> 
> Zhihu
> [Windows Install and Configure Linux Subsystem (WSL2) - Zhihu](https://zhuanlan.zhihu.com/p/1903903315080774656)

After installing WSL, you can download Linux distributions through the Microsoft Store. However, it seems it doesn't use the proxy, and the network always has issues (or maybe other problems), and I couldn't open it after trying many methods.
Just download directly using the command line.

Adding the `--web-download` parameter will force downloading the kernel and distribution directly from GitHub/Microsoft servers, **bypassing the Microsoft Store**.

Open **Administrator** PowerShell and run:

```
wsl --install -d Ubuntu-24.04 --web-download
```

- This will automatically enable WSL components, download Ubuntu 24.04, and install it.
    
- After installation, restart your computer. It will automatically pop up a terminal for you to set your username and password.

# Network Configuration

Current versions seem to emphasize WSL sharing the local network with Windows. When opened for the first time, there will be such a warning:
```bash
wsl: Localhost proxy configuration detected but not mirrored to WSL. WSL in NAT mode does not support localhost proxy.
```

#### Method 1: Enable "Mirrored Network Mode" (Recommended, Windows 11 22H2 and above only)

This is currently the most perfect solution. It allows WSL and Windows to share the same network interface (including localhost).

1. In the Windows File Explorer address bar, enter `%UserProfile%` and press Enter.
    
2. Find or create a file named `.wslconfig` (note the dot at the beginning).
    
3. Open with Notepad, enter the following content and save:
    
    Ini, TOML
    
    ```
    [wsl2]
    networkingMode=mirrored
    autoProxy=true
    ```
    
4. Open PowerShell (CMD), enter `wsl --shutdown` to restart WSL.
    
5. Enter WSL again, this warning should disappear, and the network is completely interoperable with Windows.

If you want WSL to also go through the Clash proxy, the method I used before was:

1. Open **Allow LAN** in Clash.
2. Get Windows IP via `ipconfig` in PowerShell.
3. Add network configuration to WSL.

```jsx
echo 'export http_proxy="<http://192.168.xxx.xxx:7890>"' >> ~/.bashrc
echo 'export https_proxy="<http://192.168.xxx.xxx:7890>"' >> ~/.bashrc
echo 'export all_proxy="socks5://192.168.xxx.xxx:7891"' >> ~/.bashrc
source ~/.bashrc
```

# Graphical Configuration

## Using VcXsrv

[Win11 + WSL2 Build ros + gazebo environment and use graphical interface (xfce4) via VcXsrv on WSL2_windows11 wsl ros2-CSDN Blog](https://blog.csdn.net/qq_51908382/article/details/140607102)

### Step 1: Download and Install VcXsrv

1. **Download VcXsrv**: Currently, you cannot download and install VcXsrv directly via WSL command line, you need to download it manually. You can visit [VcXsrv Official Website](https://sourceforge.net/projects/vcxsrv/) to download the latest installer (`vcxsrv-64.X.XX.XX.exe`).
2. **Run Installer**: After downloading, double-click the installer and follow the prompts to complete the installation. Generally, the default settings are sufficient.

### Step 2: Configure VcXsrv

1. **Start VcXsrv**:
    - Find "XLaunch" in the Windows Start menu and launch it.
    - **Configuration Options**:
        - **Display settings**: Select "Multiple windows".
        - **Client startup**: Select "Start no client".
        - **Extra settings**: Check "Disable access control" (if you trust the LAN environment, this allows connections without restriction to specific hosts).
2. **Save Configuration File** (Optional):
    - In the last step of the startup configuration, you can choose to save the configuration for quick startup next time.

### Step 3: Set DISPLAY Variable in WSL

To allow Linux applications in WSL to connect to VcXsrv's graphical interface, you need to configure the environment variable `DISPLAY`.

1. Open WSL terminal and edit `~/.bashrc` file:
    
    ```bash
    nano ~/.bashrc
    ```
    
2. Add the following content to the end of the file:
    
    ```bash
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
    ```
    
    This command will automatically get your Windows host IP and set the `DISPLAY` environment variable so that the latest host IP is automatically used every time you connect to X Server.
    
3. **Apply Changes**:
    
    - Save and close the `~/.bashrc` file, then run the following command to apply the changes:
        
        ```bash
        source ~/.bashrc
        ```
        

### Step 4: Verify Settings

1. In WSL, install some simple graphical interface applications to test the settings, such as `xclock`:
    
    ```bash
    sudo apt update
    sudo apt install x11-apps
    ```
    
2. Run `xclock` to test:
    
    ```bash
    xclock
    ```
    
    If installed and configured correctly, a clock window should appear on the Windows desktop.
    

## WSLg

The latest version of WSL supports graphical display now.

### Step 1: Close All WSL Instances

Before updating, it is best to close all running WSL instances to ensure the update process goes smoothly.

```powershell
wsl --shutdown
```

### Step 2: Update WSL Kernel and WSLg

Run the following command in PowerShell or CMD to check and update the WSL kernel and WSLg:

```powershell
wsl --update
```

If `wsl --update` runs successfully, the system will automatically download and install the latest WSL components, including the kernel and WSLg.

### Step 3: Check WSL Version

After the update is complete, you can confirm whether the latest WSL, kernel, and WSLg versions have been successfully installed using the following command:

```powershell
wsl --version
# Old versions do not support the above command, use the following instead
wsl --status 
```

You should see information about the WSL version, kernel version, WSLg version, etc.

### Manual Update

If `wsl --update` fails to update normally (mine did), you can manually download and install the kernel update file:

1. Visit [WSL2 Kernel Update Page](https://aka.ms/wsl2kernel).
2. Download the `.msi` file and run it to update the kernel.

After installation, you can see similar output:

```bash
alexavier@DESKTOP-6SOFPUI:~$ echo $WAYLAND_DISPLAY
wayland-0
alexavier@DESKTOP-6SOFPUI:~$ echo $DISPLAY
:0
alexavier@DESKTOP-6SOFPUI:~$ echo $XDG_RUNTIME_DIR
/run/user/1000/
```

### **Method 2: Edit Configuration File**

If `gsettings` is not available, you can directly edit the GTK configuration file to modify the mouse pointer size.

1. Open or create configuration file:
    
    ```bash
    bash
    Copy code
    nano ~/.Xresources
    
    ```
    
2. Add the following content:
    
    ```bash
    bash
    Copy code
    Xcursor.size: 48
    
    ```
    
3. Save the file and refresh configuration:
    
    ```bash
    bash
    Copy code
    xrdb ~/.Xresources
    
    ```
    
4. After restarting WSL or X11 environment, the mouse pointer size will be updated.
    

# Development Tools

## Vscode

Run VSCode on Windows, install **Remote-WSL** plugin.

[Remote development in WSL](https://code.visualstudio.com/docs/remote/wsl-tutorial)

## Docker
**Install Docker:** Run the native Docker installation script in WSL 2 (`curl -fsSL https://get.docker.com | sh`).
After the script finishes and returns to the command prompt (`$`), to avoid typing `sudo docker` every time, please be sure to execute the following two lines of commands:

Bash

```
# 1. Add your user to the docker group
sudo usermod -aG docker $USER

# 2. Refresh the group (or simply restart the WSL window)
newgrp docker
```

After that, you can enter `docker run hello-world` to test if the installation was successful.
