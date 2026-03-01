---
title: Linux Preference
date: 2025-01-21
description: Useful system configuration for linux.
summary: Useful system configuration for linux.
tags:
  - linux
---

# Terminal

### Auto Completion

#### 1. **Bash Completion**

Bash Completion is a widely used auto-completion script that provides auto-completion functionality for many common commands.

#### Install Bash Completion:

On Ubuntu or Debian systems, you can install it using the following commands:

```bash
sudo apt update
sudo apt install bash-completion
```

After installation, ensure you add the following content to your `~/.bashrc` file to enable Bash Completion:

```bash
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
```

Then, reload the `~/.bashrc` file:

```bash
source ~/.bashrc
```

#### 2. **fzf**

`fzf` is a powerful command-line fuzzy finder that can be combined with Bash and Zsh to provide fuzzy search for command history and filenames.

#### Install fzf:

On Ubuntu or Debian systems, you can install it using the following commands:

```bash
sudo apt update
sudo apt install fzf
```

After installation, you can add the following content to your `~/.bashrc` file to enable fzf:

```bash
# Use fzf for command history search
bind -x '"\C-r": "fzf-history"'
fzf-history() {
  local selected=$(HISTTIMEFORMAT= history | fzf +s --tac --reverse --height 40% --border --ansi)
  READLINE_LINE="${selected[*]:7}"
  READLINE_POINT=${#READLINE_LINE}
}
```

Then, reload the `~/.bashrc` file:

```bash
source ~/.bashrc
```


### Zsh

[Zsh Installation and Configuration, Beautify Terminal with Oh-My-Zsh | Leehow's Station](https://www.haoyep.com/posts/zsh-config-oh-my-zsh/)

![IMG-20250122232358691.webp](/img/Posts/Linux/Linux%20Preference/IMG-20250122232358691.webp)

1. Installation

```bash
sudo apt update
sudo apt install zsh
```

2. Switch default terminal to Zsh

```bash
chsh -s $(which zsh)
```

3. **Logout and log back in** to make the changes effective.

4. **Verify if the default terminal is Zsh**:
   Reopen the terminal and enter the following command to verify the current shell:
   
   ```bash
   echo $SHELL
   ```
   
   The output should be `/usr/bin/zsh` or a similar path, indicating that the current default shell has been switched to Zsh.

#### Configure ROS

Add the path of ROS 2 to `PATH`.

1. `nano ~/.zshrc`

2. Add the following content to the end of the file
   
   `source /opt/ros/foxy/setup.zsh`

3. Save and close the file, then reload `~/.zshrc`
   
   `source ~/.zshrc`

Verify if ROS 2 commands are available

`ros2 --help`



#### Configure Zsh

1. **Install Oh My Zsh**:
   
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

2. **Install zsh-autosuggestions**:
   
```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
echo "source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh" >> ~/.zshrc
```

3. **Install zsh-syntax-highlighting**:
   
```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.zsh/zsh-syntax-highlighting
echo "source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ~/.zshrc
```

4. **Reload `.zshrc` file**:
   
```bash
source ~/.zshrc
```

After completing these steps, Zsh will become your default shell, and you can leverage its powerful auto-completion and suggestion features to improve command-line efficiency.

Using `Oh My Zsh` in Zsh makes it very convenient to change and customize themes. Here are the steps:

#### 1. Install Oh My Zsh

If you haven't installed Oh My Zsh yet, you can use the following command to install it:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

#### 2. Select and Set Theme

Oh My Zsh comes with many themes. You can set the theme you want to use in the `~/.zshrc` file. Here are a few popular theme examples:

- **agnoster**: A clean and informative theme, suitable for wide screens.
- **robbyrussell**: The default theme of Oh My Zsh, simple and easy to use.
- **powerlevel10k**: A highly customizable and feature-rich theme.

#### Modify Theme:

1. **Edit `.zshrc` file**:
   
   ```bash
   nano ~/.zshrc
   ```

2. **Find and modify the `ZSH_THEME` line**:
   Set `ZSH_THEME` to the theme you want, for example:
   
   ```bash
   ZSH_THEME="agnoster"
   ```

3. **Save and reload `.zshrc` file**:
   
   ```bash
   source ~/.zshrc
   ```

#### 3. Install Powerlevel10k Theme

If you want to use the `powerlevel10k` theme, here are the installation steps:

1. **Clone Powerlevel10k Repository**:
   
```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

2. **Set Powerlevel10k Theme**:
   Set the theme to `powerlevel10k/powerlevel10k` in the `.zshrc` file:
   
   ```bash
   ZSH_THEME="powerlevel10k/powerlevel10k"
   ```

3. **Save and reload `.zshrc` file**:
   
   ```bash
   source ~/.zshrc
   ```

4. **Configure Powerlevel10k**:
   Reopen the terminal, and Powerlevel10k will automatically start the configuration wizard to help you customize the theme appearance.

#### 4. Install Fonts

To make some advanced themes (like `powerlevel10k`) display correctly, you may need to install fonts that support icons and special symbols, such as `MesloLGS NF`.

1. **Download MesloLGS NF Font**:
   Download `MesloLGS NF` font from [Nerd Fonts](https://github.com/romkatv/powerlevel10k#manual-font-installation).

2. **Install Font**:
   Install the downloaded font file to the system. For Ubuntu, you can copy the font file to the `~/.local/share/fonts` directory, then run:
   
   ```bash
   fc-cache -fv
   ```

3. **Select Font in Terminal Settings**:
   Open your terminal settings and set the font to `MesloLGS NF`.

### Tilix

#### Open Terminal in Folder Context Menu

1. **Create Script File**:
   Use the following command to create a script file:
   
   ```bash
   mkdir -p ~/.local/share/nautilus/scripts
   nano ~/.local/share/nautilus/scripts/Open\ in\ Tilix
   ```

2. **Edit Script Content**:
   Enter the following content in the opened file:
   
   ```bash
   #!/bin/bash
   tilix -w $NAUTILUS_SCRIPT_CURRENT_URI
   ```

3. **Save and Close File**:
   In nano, press `Ctrl+O` then `Enter` to save the file, and press `Ctrl+X` to exit the editor.

4. **Make Script Executable**:
   Enter the following command to make the script executable:
   
   ```bash
   chmod +x ~/.local/share/nautilus/scripts/Open\ in\ Tilix
   ```

After completing the above steps, you should be able to right-click inside a folder, then select "Scripts" -> "Open in Tilix" to open that folder in Tilix. Note that you should right-click on a folder or inside the folder, not on empty space if specifically targeting a folder selection (though usually context menu inside folder works for current dir).

### Kitty

[Kitty: Another GPU-accelerated terminal tool - CSDN Blog](https://blog.csdn.net/easylife206/article/details/124995683)

[GitHub - dexpota/kitty-themes: A collection of themes for kitty terminal 😻](https://github.com/dexpota/kitty-themes)

# Blog

You have successfully installed nvm, but need to reload the shell configuration file for it to take effect. You can follow the prompts of the installation script, close and reopen the terminal, or manually run the following commands:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

### 1. Reload Configuration File

You can manually run the above commands or enter the following command in the terminal to reload your configuration file:

```bash
source ~/.zshrc
```

### 2. Install Node.js Version 20

After reloading the configuration file, run the nvm command to install Node.js 20:

```bash
nvm install 20
```

### 3. Set Default Node.js Version

After installation is complete, you can set Node.js 20 as the default version:

```bash
nvm use 20
nvm alias default 20
```

### 4. Verify Installation

Finally, verify if Node.js and npm are installed correctly:

```bash
node -v
npm -v
```

### 5. Install Hexo CLI

Now, you can install Hexo CLI:

```bash
npm install -g hexo-cli
```

Through these steps, you should be able to use nvm to install and manage Node.js versions and successfully install Hexo CLI. If there are still problems, please feel free to let me know!


# Common Applications
## Zotero

Here are the steps to install `Zotero-7.0.11_linux-x86_64.tar.bz2`:

It seems there is a simpler way:

>https://github.com/retorquere/zotero-deb

---

### 1. Extract Compressed File

First, you need to extract the downloaded `tar.bz2` file.

Run the following command:

```bash
sudo apt update
sudo apt install bzip2
tar -xvjf Zotero-7.0.11_linux-x86_64.tar.bz2
```

This will extract the file to the current directory, usually generating a folder named `Zotero_linux-x86_64`.

---

### 2. Move Extracted Files to System Directory (Optional)

For easier management, you can move the extracted folder to the `/opt` directory (system applications are usually stored here).

Run the following command:

```bash
sudo mv Zotero_linux-x86_64 /opt/zotero
```

---

### 3. Create Desktop Shortcut

To start Zotero conveniently, you can create a desktop shortcut.

1. Edit shortcut file:
    
    ```bash
    sudo nano /usr/share/applications/zotero.desktop
    ```
    
2. Add the following content to the file:
    
    ```plaintext
    [Desktop Entry]
    Name=Zotero
    Exec=/opt/zotero/zotero
    Icon=/opt/zotero/chrome/icons/default/default256.png
    Type=Application
    Terminal=false
    Categories=Office;Education;
    ```
    
3. Save and exit (Press `Ctrl+O` to save, `Ctrl+X` to exit).
    

---

### 4. Create Symbolic Link for Executable

Create a symbolic link so that you can run Zotero by typing `zotero` in the terminal.

Run the following command:

```bash
sudo ln -s /opt/zotero/zotero /usr/local/bin/zotero
```

---

### 5. Install Necessary Dependencies (If Needed)

Zotero might need some system dependencies, ensure they are installed. Run the following command:

```bash
sudo apt update
sudo apt install -y libxss1 libxtst6 libgconf-2-4 libnss3
```

---

### 6. Start Zotero

Now, you can start Zotero in the following ways:

- Type `zotero` in the terminal and press Enter.
- Or start via the desktop shortcut.

---

### 7. Optional: Update Zotero

If you need to update Zotero, simply repeat the above steps. The new version can directly overwrite the old version files.

---

After completing the above steps, Zotero should run normally! If you encounter any problems, please let me know!

# GNOME
## Split Screen

### **1. Install GNOME Tweaks Tool**

GNOME Tweaks is used to manage extensions and system customization settings:

```bash
sudo apt install gnome-tweaks gnome-shell-extensions
```

### **2. Install GNOME Extensions Browser Plugin**

- Open [GNOME Extensions Official Website](https://extensions.gnome.org/).
- Install GNOME Shell Integration plugin (supports Firefox and Chrome).
- After installation, refresh the browser page to ensure the website can detect the GNOME environment.

### **Recommended Split Screen Extensions**

1. **[Tiling Assistant](https://extensions.gnome.org/extension/3733/tiling-assistant/)**
    
    - **Features**:
        - Enhances GNOME's default split-screen functionality.
        - Supports 1/2 screen, 1/4 screen, 1/3 screen and other split-screen layouts.
        - Allows resizing windows by dragging.
    - **Installation**:
        - Visit the extension page, click the "Install" button.
        - After installation, enable it in GNOME Tweaks.
2. **[Pop Shell](https://extensions.gnome.org/extension/4186/pop-shell/)**
    
    - **Features**:
        - Similar to Tiling Window Manager experience.
        - Provides keyboard shortcuts for window split-screen layouts.
        - Supports mouse dragging, window grid, etc.
    - **Installation**:
        - Also install via GNOME Extensions website.
    - **Suitable for**:
        - People who prefer using keyboard shortcuts.
        - People who need to dynamically adjust window split screens.
3. **[WinTile](https://extensions.gnome.org/extension/39/wintile/)**
    
    - **Features**:
        - Provides split-screen functionality similar to Windows.
        - Supports window left/right, up/down, quarter screen.
    - **Suitable for**:
        - People who prefer Windows split-screen operation logic.
4. **[Dash to Panel](https://extensions.gnome.org/extension/1160/dash-to-panel/)**
    
    - **Features**:
        - Not directly used for split screen, but can enhance taskbar functionality for convenient window management.
    - **Combination**:
        - Can be used in combination with other split-screen extensions.

Simply search and install.
