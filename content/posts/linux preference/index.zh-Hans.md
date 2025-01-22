---
title: linux preference
date: 2025-01-21
description: Useful system configuration for linux.
summary: Useful system configuration for linux.
tags: ["linux"]
---

# 终端

### 自动补全

#### 1. **Bash Completion**

Bash Completion 是一个广泛使用的自动补全脚本，可以为许多常用命令提供自动补全功能。

#### 安装 Bash Completion：

在 Ubuntu 或 Debian 系统上，可以使用以下命令安装：

```bash
sudo apt update
sudo apt install bash-completion
```

安装完成后，确保在你的 `~/.bashrc` 文件中添加以下内容以启用 Bash Completion：

```bash
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
```

然后，重新加载 `~/.bashrc` 文件：

```bash
source ~/.bashrc
```

#### 2. **fzf**

`fzf` 是一个强大的命令行模糊查找工具，可以与 Bash 和 Zsh 结合使用，提供命令历史记录和文件名的模糊搜索。

#### 安装 fzf：

在 Ubuntu 或 Debian 系统上，可以使用以下命令安装：

```bash
sudo apt update
sudo apt install fzf
```

安装完成后，你可以将以下内容添加到 `~/.bashrc` 文件中以启用 fzf：

```bash
# Use fzf for command history search
bind -x '"\C-r": "fzf-history"'
fzf-history() {
  local selected=$(HISTTIMEFORMAT= history | fzf +s --tac --reverse --height 40% --border --ansi)
  READLINE_LINE="${selected[*]:7}"
  READLINE_POINT=${#READLINE_LINE}
}
```

然后，重新加载 `~/.bashrc` 文件：

```bash
source ~/.bashrc
```


### Zsh

[Zsh 安装与配置，使用 Oh-My-Zsh 美化终端 | Leehow的小站](https://www.haoyep.com/posts/zsh-config-oh-my-zsh/)

![IMG-20250122232358691.png](/img/posts/Linux/linux%20preference/IMG-20250122232358691.png)

1. 安装

```bash
sudo apt update
sudo apt install zsh
```

2. 切换默认终端到 Zsh

```bash
chsh -s $(which zsh)
```

3. **注销并重新登录**，使更改生效。

4. **验证默认终端是否为 Zsh**：
   重新打开终端，然后输入以下命令来验证当前 shell：
   
   ```bash
   echo $SHELL
   ```
   
   输出应该是 `/usr/bin/zsh` 或类似路径，表示当前默认 shell 已切换到 Zsh。

#### 配置ROS

将 ROS 2 的路径添加到 `PATH` 中。

1. `nano ~/.zshrc`

2. 在文件的末尾添加以下内容
   
   `source /opt/ros/foxy/setup.zsh`

3. 保存并关闭文件，然后重新加载 `
   
   `source ~/.zshrc`

验证 ROS 2 命令是否可用

`ros2 --help`



#### 配置 Zsh

1. **安装 Oh My Zsh**：
   
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

2. **安装 zsh-autosuggestions**：
   
```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
echo "source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh" >> ~/.zshrc
```

3. **安装 zsh-syntax-highlighting**：
   
```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.zsh/zsh-syntax-highlighting
echo "source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
```

4. **重新加载 `.zshrc` 文件**：
   
```bash
source ~/.zshrc
```

完成这些步骤后，Zsh 将成为你的默认 shell，并且你可以利用其强大的自动补全和提示功能来提高命令行效率。

在 Zsh 中使用 `Oh My Zsh` 可以很方便地更换和定制主题。以下是步骤：

#### 1. 安装 Oh My Zsh

如果你还没有安装 Oh My Zsh，可以使用以下命令进行安装：

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

#### 2. 选择和设置主题

Oh My Zsh 自带许多主题，你可以在 `~/.zshrc` 文件中设置想要使用的主题。以下是几个受欢迎的主题示例：

- **agnoster**: 一个简洁且信息丰富的主题，适合宽屏显示器。
- **robbyrussell**: Oh My Zsh 默认主题，简洁易用。
- **powerlevel10k**: 一个高度可定制且功能丰富的主题。

#### 修改主题：

1. **编辑 `.zshrc` 文件**：
   
   ```bash
   nano ~/.zshrc
   ```

2. **找到并修改 `ZSH_THEME` 行**：
   将 `ZSH_THEME` 设置为你想要的主题，例如：
   
   ```bash
   ZSH_THEME="agnoster"
   ```

3. **保存并重新加载 `.zshrc` 文件**：
   
   ```bash
   source ~/.zshrc
   ```

#### 3. 安装 Powerlevel10k 主题

如果你想使用 `powerlevel10k` 主题，以下是安装步骤：

1. **克隆 Powerlevel10k 仓库**：
   
```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

2. **设置 Powerlevel10k 主题**：
   在 `.zshrc` 文件中设置主题为 `powerlevel10k/powerlevel10k`：
   
   ```bash
   ZSH_THEME="powerlevel10k/powerlevel10k"
   ```

3. **保存并重新加载 `.zshrc` 文件**：
   
   ```bash
   source ~/.zshrc
   ```

4. **配置 Powerlevel10k**：
   重新打开终端，Powerlevel10k 会自动启动配置向导，帮助你定制主题外观。

#### 4. 安装字体

为了让一些高级主题（如 `powerlevel10k`）正常显示，你可能需要安装支持图标和特殊符号的字体，如 `MesloLGS NF`。

1. **下载 MesloLGS NF 字体**：
   从 [Nerd Fonts](https://github.com/romkatv/powerlevel10k#manual-font-installation) 下载 `MesloLGS NF` 字体。

2. **安装字体**：
   将下载的字体文件安装到系统中。对于 Ubuntu，可以将字体文件复制到 `~/.local/share/fonts` 目录，然后运行：
   
   ```bash
   fc-cache -fv
   ```

3. **在终端设置中选择字体**：
   打开你的终端设置，将字体设置为 `MesloLGS NF`。

### Tilix

#### 在文件夹右键打开终端

1. **创建脚本文件**：
   使用以下命令创建脚本文件：
   
   ```bash
   mkdir -p ~/.local/share/nautilus/scripts
   nano ~/.local/share/nautilus/scripts/Open\ in\ Tilix
   ```

2. **编辑脚本内容**：
   在打开的文件中输入以下内容：
   
   ```bash
   #!/bin/bash
   tilix -w $NAUTILUS_SCRIPT_CURRENT_URI
   ```

3. **保存并关闭文件**：
   在 nano 中，按 `Ctrl+O` 然后 `Enter` 保存文件，按 `Ctrl+X` 退出编辑器。

4. **设置脚本为可执行**：
   输入以下命令来设置脚本为可执行：
   
   ```bash
   chmod +x ~/.local/share/nautilus/scripts/Open\ in\ Tilix
   ```

完成以上步骤后，你应该能够在文件夹中右键点击，然后选择 “脚本” -> “Open in Tilix” 来在 Tilix 中打开该文件夹了，注意右键文件夹，而不是空白处。

### Kitty

[Kitty: 又一款基于 GPU 加速的终端工具-CSDN博客](https://blog.csdn.net/easylife206/article/details/124995683)

[GitHub - dexpota/kitty-themes: A collection of themes for kitty terminal 😻](https://github.com/dexpota/kitty-themes)

# Blog

你已经成功安装了nvm，但需要重新加载shell配置文件以使其生效。你可以按照安装脚本的提示，关闭并重新打开终端，或者手动运行以下命令：

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

### 1. 重新加载配置文件

你可以手动运行上面的命令或者在终端中输入以下命令来重新加载你的配置文件：

```bash
source ~/.zshrc
```

### 2. 安装Node.js 20版本

重新加载配置文件后，运行nvm命令来安装Node.js 20：

```bash
nvm install 20
```

### 3. 设置默认Node.js版本

安装完成后，可以设置Node.js 20为默认版本：

```bash
nvm use 20
nvm alias default 20
```

### 4. 验证安装

最后，验证Node.js和npm是否正确安装：

```bash
node -v
npm -v
```

### 5. 安装Hexo CLI

现在，你可以安装Hexo CLI：

```bash
npm install -g hexo-cli
```

通过这些步骤，你应该能够使用nvm安装并管理Node.js的版本，并成功安装Hexo CLI。如果仍有问题，请随时告知！


# 常用应用
## Zotero

以下是安装 `Zotero-7.0.11_linux-x86_64.tar.bz2` 的步骤：

似乎有个更简便的

>https://github.com/retorquere/zotero-deb

---

### 1. 解压压缩文件

首先，需要将下载的 `tar.bz2` 文件解压。

运行以下命令：

```bash
sudo apt update
sudo apt install bzip2
tar -xvjf Zotero-7.0.11_linux-x86_64.tar.bz2
```

这会将文件解压到当前目录，通常会生成一个名为 `Zotero_linux-x86_64` 的文件夹。

---

### 2. 移动解压后的文件到系统目录（可选）

为方便管理，可以将解压后的文件夹移动到 `/opt` 目录下（系统应用通常存放在这里）。

运行以下命令：

```bash
sudo mv Zotero_linux-x86_64 /opt/zotero
```

---

### 3. 创建桌面快捷方式

为了方便启动 Zotero，可以创建一个桌面快捷方式。

1. 编辑快捷方式文件：
    
    ```bash
    sudo nano /usr/share/applications/zotero.desktop
    ```
    
2. 在文件中添加以下内容：
    
    ```plaintext
    [Desktop Entry]
    Name=Zotero
    Exec=/opt/zotero/zotero
    Icon=/opt/zotero/chrome/icons/default/default256.png
    Type=Application
    Terminal=false
    Categories=Office;Education;
    ```
    
3. 保存并退出（按 `Ctrl+O` 保存，`Ctrl+X` 退出）。
    

---

### 4. 为可执行文件创建符号链接

创建符号链接，以便可以通过命令 `zotero` 在终端中运行。

运行以下命令：

```bash
sudo ln -s /opt/zotero/zotero /usr/local/bin/zotero
```

---

### 5. 安装必要的依赖项（如果需要）

Zotero 可能需要一些系统依赖项，确保它们已安装。运行以下命令：

```bash
sudo apt update
sudo apt install -y libxss1 libxtst6 libgconf-2-4 libnss3
```

---

### 6. 启动 Zotero

现在，你可以通过以下方式启动 Zotero：

- 在终端输入 `zotero` 并按下回车。
- 或者通过桌面快捷方式启动。

---

### 7. 可选：更新 Zotero

如果需要更新 Zotero，只需重复以上步骤。新的版本可以直接覆盖旧版本文件。

---

完成上述步骤后，Zotero 应该可以正常运行！如果你遇到任何问题，请告诉我！

# GNOME
## 分屏

### **1. 安装 GNOME Tweaks 工具**

GNOME Tweaks 用于管理扩展和系统自定义设置：

```bash
sudo apt install gnome-tweaks gnome-shell-extensions
```

### **2. 安装 GNOME 扩展浏览器插件**

- 打开 [GNOME Extensions 官方网站](https://extensions.gnome.org/)。
- 安装 GNOME Shell Integration 插件（支持 Firefox 和 Chrome）。
- 安装完成后，刷新浏览器页面，确保网站可以检测到 GNOME 环境。

### **推荐的分屏扩展**

1. **[Tiling Assistant](https://extensions.gnome.org/extension/3733/tiling-assistant/)**
    
    - **功能**：
        - 增强 GNOME 默认的分屏功能。
        - 支持 1/2 屏、1/4 屏、1/3 屏等多种分屏布局。
        - 允许通过拖拽调整窗口大小。
    - **安装**：
        - 访问扩展页面，点击 "Install" 按钮。
        - 安装完成后，可以在 GNOME Tweaks 中启用。
2. **[Pop Shell](https://extensions.gnome.org/extension/4186/pop-shell/)**
    
    - **功能**：
        - 类似平铺式窗口管理器的体验（Tiling Window Manager）。
        - 提供键盘快捷键操作窗口的分屏布局。
        - 支持鼠标拖拽、窗口栅格化等功能。
    - **安装**：
        - 同样通过 GNOME Extensions 网站安装。
    - **适合人群**：
        - 喜欢使用键盘快捷键的人。
        - 需要动态调整窗口分屏的人。
3. **[WinTile](https://extensions.gnome.org/extension/39/wintile/)**
    
    - **功能**：
        - 提供类似 Windows 的分屏功能。
        - 支持窗口左右、上下、四分屏。
    - **适合人群**：
        - 更喜欢 Windows 分屏操作逻辑的人。
4. **[Dash to Panel](https://extensions.gnome.org/extension/1160/dash-to-panel/)**
    
    - **功能**：
        - 并非直接用于分屏，但可以增强任务栏功能，方便窗口管理。
    - **搭配**：
        - 可以与其他分屏扩展配合使用。

直接搜索安装即可
