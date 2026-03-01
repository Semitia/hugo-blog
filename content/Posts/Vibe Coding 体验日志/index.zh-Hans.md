---
title: Vibe Coding 体验日志
date: 2026-02-17
description: Notes of trying vibe coding
summary: Notes of trying vibe coding
tags:
  - VsCode
  - RooCode
  - Cline
---

# Cline

> 第三方API教程
> [Docs](https://hcn5nb52i36k.feishu.cn/wiki/FLymwjAYdiNPjJktRFycIUcInzd)
> API网站
> [New API](https://ccapi.aiclaude.club/console)

对于这个中转站，
claude-sonnet-4-6-thinking在默认分组下可以用，但是与cline的tool_use似乎不兼容。


## 使用API
### API功能测试

`windows powershell`
```powershell
Invoke-RestMethod -Uri "https://ccapi.aiclaude.club/v1/chat/completions" `
  -Method Post `
  -Headers @{
    "Authorization" = "Bearer sk-xxx"
    "Content-Type" = "application/json"
  } `
  -Body '{"model": "gemini-2.5-pro", "messages": [{"role": "user", "content": "hello"}]}'
  
```

输出示例
```powershell
id      : chatcmpl-20260221104424823667108QNzSowg3
model   : gemini-2.5-pro
object  : chat.completion
created : 1771670671
choices : {@{index=0; message=; finish_reason=stop}}
usage   : @{prompt_tokens=2; completion_tokens=501; total_tokens=503; prompt_tokens_details=; c
          ompletion_tokens_details=; input_tokens=0; output_tokens=0; input_tokens_details=; cl
          aude_cache_creation_5_m_tokens=0; claude_cache_creation_1_h_tokens=0}
```

### 用于`cline`

- **API Provider (服务商)**: 选择 `OpenAI Compatible`
- **Base URL (基础 URL)**: `https://ccapi.aiclaude.club/v1`
  _(⚠️ 注意：这里只需要填到 `/v1`，**不要**带后面的 `/chat/completions`，Cline 会自动补全)_
- **API Key (密钥)**: `sk-xxx`
- **Model ID (模型 ID)**: 手动填入 `gemini-2.5-pro` 或 `gemini-3-pro-preview`

## 使用miniforge
这是一个非常经典的环境配置痛点。PowerShell 确实是 Windows 下的默认终端，但它对“半路出家”的 Python 环境（如 Miniforge/Conda）并不像传统的 CMD 那么友好，尤其是当你为了系统整洁没有添加全局路径时。

要解决这个问题，让 Cline 乖乖用上 Conda，你有三种主要的“调教”方案：

---

### 方案一：修改 VS Code 的默认终端配置（最推荐）

Cline 通常会继承 VS Code 的终端设置。你可以通过 VS Code 的 **“终端配置文件”**，把 Miniforge 的初始化脚本塞进去。

1. 在 VS Code 中按下 `Ctrl + Shift + P`。
    
2. 输入 **"Terminal: Select Default Profile"** 并确认。
    
3. 如果里面没有 Miniforge，点击旁边的**设置图标**（或者去 `settings.json`）。
    
4. 在 `terminal.integrated.profiles.windows` 下添加或修改 PowerShell 配置，加上 `args` 来执行初始化脚本：
    

JSON

```
"PowerShell (Conda)": {
    "source": "PowerShell",
    "icon": "terminal-powershell",
    "args": [
        "-ExecutionPolicy", "ByPass",
        "-NoExit",
        "-Command", "& 'C:\\你的Miniforge安装路径\\shell\\condabin\\conda-hook.ps1'; conda activate '你的环境名'"
    ]
}
```

---

### 方案二：为 Cline 设置自定义指令（最省心）

你可以通过 Cline 的 **Custom Instructions**（在 Cline 面板的设置里，或者项目的 `.clinerules` 文件中）明确告诉它怎么启动环境。

在指令中加入这段话：

> "Every time you run a Python command, please use the full path to the conda executable or activate the environment first. My Miniforge path is `C:\path\to\miniforge`. Before running scripts, use: `& 'C:\path\to\miniforge\scripts\activate' your_env_name`."

这样 Cline 在生成执行代码的任务时，会自动在命令前加上激活环境的操作。

---

### 方案三：通过 PowerShell Profile 实现“静默加载”

即使你没加全局路径，你也可以在 PowerShell 的启动配置文件中手动“钩入” Miniforge。

1. 在终端输入 `notepad $PROFILE`（如果文件不存在，先运行 `New-Item -Path $PROFILE -Type File -Force`）。
    
2. 在打开的记事本中加入以下内容：
    
    PowerShell
    
    ```
    # 指向你 Miniforge 的 conda-hook
    (& "C:\你的路径\Miniforge3\scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
    ```
    
3. 保存并重启 VS Code。
    

**结果：** 以后不管是你手动开终端，还是 Cline 开终端，`conda` 命令都会直接可用，哪怕它不在全局环境变量里。

---

### 为什么 Cline 会报错？

Cline 本质上是**通过命令行和你交互的“高级宏”**。如果它执行 `python main.py` 时报错：

- **CommandNotFound**: 它找不到 Python（因为它在 Conda 环境里）。
    
- **ModuleNotFoundError**: 它找到了系统自带的 Python，但没找到你装的包。
    

### 下一步建议

你可以先尝试**方案三**，因为它是“一次配置，全家受益”。

**如果不确定 Miniforge 的具体安装路径，可以在终端输入 `where conda`（如果你在 Conda 自己的命令行里）或者直接去开始菜单里找 Miniforge Prompt 的快捷键属性，把那个路径发给我，我帮你写出具体的配置代码？**