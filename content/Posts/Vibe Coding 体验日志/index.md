---
title: Vibe Coding Experience Log
date: 2026-02-17
description: Notes of trying vibe coding
summary: Notes of trying vibe coding
tags:
  - VsCode
  - RooCode
  - Cline
---

# Cline

> Third-party API Tutorial
> [Docs](https://hcn5nb52i36k.feishu.cn/wiki/FLymwjAYdiNPjJktRFycIUcInzd)
> API Website
> [New API](https://ccapi.aiclaude.club/console)

For this transit station,
claude-sonnet-4-6-thinking can be used under the default group, but it seems incompatible with cline's tool_use.


## Use API
### API Function Test

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

Output Example
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

### For `cline`

- **API Provider**: Select `OpenAI Compatible`
- **Base URL**: `https://ccapi.aiclaude.club/v1`
  _(⚠️ Note: Here you only need to fill in up to `/v1`, **do not** include `/chat/completions` at the end, Cline will auto-complete it)_
- **API Key**: `sk-xxx`
- **Model ID**: Manually enter `gemini-2.5-pro` or `gemini-3-pro-preview`

## Use miniforge
This is a very classic environment configuration pain point. PowerShell is indeed the default terminal under Windows, but it is not as friendly to "halfway" Python environments (such as Miniforge/Conda) as the traditional CMD, especially when you have not added a global path for system cleanliness.

To solve this problem and make Cline obediently use Conda, you have three main "tuning" schemes:

---

### Scheme 1: Modify VS Code's default terminal configuration (Most Recommended)

Cline usually inherits VS Code's terminal settings. You can put Miniforge's initialization script into VS Code's **"Terminal Profile"**.

1. Press `Ctrl + Shift + P` in VS Code.
    
2. Enter **"Terminal: Select Default Profile"** and confirm.
    
3. If Miniforge is not in it, click the **settings icon** next to it (or go to `settings.json`).
    
4. Add or modify the PowerShell configuration under `terminal.integrated.profiles.windows`, adding `args` to execute the initialization script:
    

JSON

```
"PowerShell (Conda)": {
    "source": "PowerShell",
    "icon": "terminal-powershell",
    "args": [
        "-ExecutionPolicy", "ByPass",
        "-NoExit",
        "-Command", "& 'C:\\YourMiniforgeInstallPath\\shell\\condabin\\conda-hook.ps1'; conda activate 'YourEnvName'"
    ]
}
```

---

### Scheme 2: Set custom instructions for Cline (Most Worry-free)

You can explicitly tell Cline how to start the environment through Cline's **Custom Instructions** (in Cline panel settings, or project's `.clinerules` file).

Add this paragraph to the instructions:

> "Every time you run a Python command, please use the full path to the conda executable or activate the environment first. My Miniforge path is `C:\path\to\miniforge`. Before running scripts, use: `& 'C:\path\to\miniforge\scripts\activate' your_env_name`."

In this way, when Cline generates execution code tasks, it will automatically add the environment activation operation before the command.

---

### Scheme 3: Implement "Silent Load" via PowerShell Profile

Even if you haven't added a global path, you can manually "hook" Miniforge in PowerShell's startup configuration file.

1. Enter `notepad $PROFILE` in the terminal (if the file does not exist, run `New-Item -Path $PROFILE -Type File -Force` first).
    
2. Add the following content in the opened Notepad:
    
    PowerShell
    
    ```
    # Point to your Miniforge's conda-hook
    (& "C:\YourPath\Miniforge3\scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
    ```
    
3. Save and restart VS Code.
    

**Result:** In the future, whether you open the terminal manually or Cline opens the terminal, the `conda` command will be directly available, even if it is not in the global environment variables.

---

### Why does Cline report an error?

Cline is essentially **an "advanced macro" that interacts with you through the command line**. If it reports an error when executing `python main.py`:

- **CommandNotFound**: It can't find Python (because it's in the Conda environment).
    
- **ModuleNotFoundError**: It found the system's built-in Python, but didn't find the package you installed.
    

### Next Step Suggestions

You can try **Scheme 3** first, because it is "configure once, benefit the whole family".

**If you are not sure about the specific installation path of Miniforge, you can enter `where conda` in the terminal (if you are in Conda's own command line) or directly look for the shortcut properties of Miniforge Prompt in the Start menu, send me that path, and I will help you write the specific configuration code?**
