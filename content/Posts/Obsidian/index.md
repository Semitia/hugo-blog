---
title: Obsidian
date: 2026-02-16
description: Simple usage of Obsidian
summary: Simple usage of Obsidian
tags: ["Obsidian"]
---
![file-20260216220629548.webp](/img/Posts/Tools/Obsidian/file-20260216220629548.webp)

# Links

[Want to get started with Obsidian in one hour? This article is enough. [Obsidian Nanny-level Tutorial] - Zhihu (zhihu.com)](https://zhuanlan.zhihu.com/p/428519519)


# Basic Functions
[Method to display outline in Obsidian_obsidian outline-CSDN Blog](https://blog.csdn.net/csdn2683/article/details/138413414)


## Basic Syntax
### Tags
In Obsidian, content immediately following `#` represents a **Tag**, with the syntax format:  
`#TagName`  

#### Main Features:
1. **Role of Tags**  
   - Used for classifying and associating notes (similar to keyword tagging).  
   - Click on a tag to quickly filter related notes.  
   - Supports hierarchical tags (e.g., `#Programming/Python`).  

2. **Reason for Popup Candidate Box**  
   - When you type `#`, Obsidian will **automatically search for existing tags** and display a matching candidate list (tags used in other notes).  
   - This helps to quickly input existing tags and avoid creating different tags with the same semantics (e.g., `#python` and `#Python`).  

3. **Supplementary Usage**  
   - **Sub-tags**: Use `/` to separate levels (e.g., `#Study/Math`).  
   - **No spaces allowed in tags**: Use hyphens or CamelCase (e.g., `#TimeManagement` or `#TimeManagement`).  
   - **Tag Search**: Enter `tag:#TagName` in the search bar to locate all notes with that tag.  

#### Examples:
- Type `#Fitness` → Popup candidate tags like `#Fitness/Running`, `#Fitness/StrengthTraining`.  
- Type `#Project/` → Show all sub-tags starting with `#Project/`.  

If you need to turn off auto-completion, you can adjust it in settings:  
`Settings → Editor → Smart Completion → Turn off tag completion`.


# Plugins
Download and use directly in the built-in plugin store
## Attachment Management

Created a new folder named "Attachment" to unify attachment management, other configurations are default. The specific effect is:
*The path of a note relative to the vault directory* and *the path of its attachment relative to Attachment* are the same.

However, this plugin seems to have a **mysterious BUG**, switched to **‘Custom Attachment Location’**.

## Custom Attachment Location
