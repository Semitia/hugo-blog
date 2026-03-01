---
title: Blogs
date: 2025-01-21
description: Blog configuration with common frameworks.
summary: Blog configuration with common frameworks.
tags: ["Blog", "Hugo", "Obsidian"]
---

![IMG-20250121234134792.webp](/img/Posts/Tools/Blogs/IMG-20250121234134792.webp)

# Hugo

## Environment Configuration

Develop using docker

```bash
docker pull hugomods/hugo:ci
```

### Create Hugo Web Project

Skip if you already have a Hugo project

```bash
mkdir Hugo
cd Hugo
docker run --rm -it \
    -v $(pwd):/src \
    hugomods/hugo:ci new site .
```

Pull theme

```bash
sudo git -c http.proxy=http://127.0.0.1:7890 submodule add -b stable https://github.com/jpanther/congo.git themes/congo
```

Change web project content according to theme configuration documentation

> https://jpanther.github.io/congo/docs/installation/#create-a-new-site

You can also continue to refer to the documentation for personalization

> https://jpanther.github.io/congo/zh-hans/docs/getting-started/

#### congo theme

This theme wants the article title to display a picture on the side. The picture must be added in the same directory as the note with the name **cover/thumb/feature**; at the same time, there must be an index.md, not just an index.zh-Hans.md.

### Clone Existing Repository
In addition to cloning the existing blog repository, you also need to clone the **theme**
Here is to update submodules:

```bash
git submodule update --init --recursive
```

## Container Development

`docker-compose.yml` file (located in the blog project root directory)
**Image Selection:**
- Specify an old version because the code is a bit old;
- Choose the extended version, the `exts` tag means there are extra tools; for this author, choose one that is not `reg` and `std`.

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
      - .:/src  # Mount the current directory of yml to the /src directory of the container
    privileged: true  
    working_dir: /src
    stdin_open: true              
    tty: true              
    command: server -D -p 1313 --bind 0.0.0.0
```

Run in the root directory to start the container

```bash
docker compose up -d
```

At this point, if there are no errors, you can view the effect by visiting `http://localhost:1313/` via a browser

## Common Operations

If mysterious problems occur, such as thumbnails not updating, articles not appearing, etc., you can try deleting the **public directory** (cache) and regenerating.

Your intuition is very sharp! That "invisible connection" is actually very simple and crude - **filename matching**.

In the Congo theme, the logic is like this: When you write `{ github = "..." }`, the theme will look for a file named `github.svg` in the `assets/icons/` folder. If it exists, it renders it; if not, it displays a blank or a box.

So, to implement icons for Bilibili, Tools (Toolbox), Games (Gamepad), you only need to do two steps: **Find Icon** -> **Change Configuration**.

### Step 1: Prepare Icon File (SVG)

You need to put the corresponding SVG file into the `assets/icons/` folder under your blog root directory (create an `icons` folder if it doesn't exist).

**Operation Process:**

1. **Find `assets` folder**: In your `semitia-blog` root directory (Note: **Do not** go to `themes/congo/assets`, find it in your own root directory, so that upgrading the theme will not lose files).
    
2. **Create `icons` folder**: The path should be `Your Blog Root Directory/assets/icons/`.
    
3. **Download and Put in SVG**:
    
    - **Bilibili**: Go to download Bilibili's SVG, rename it to **`bilibili.svg`**, and put it into the above folder.
        
    - **Tools**: Find a toolbox icon (recommended), download SVG, rename it to **`tools.svg`**, and put it into the folder.
        
    - **Games**: Find a gamepad icon, rename it to **`gamepad.svg`**, and put it into the folder.
        

_(Tip: To make the icon color change with the theme, you can open the SVG file with Notepad, delete the `fill="..."` attribute inside, or change it to `fill="currentColor"`. Congo will automatically color them.)_

### Step 2: Modify `languages.zh-Hans.toml`

Now that the file is there, you only need to use the **filename (without suffix)** as the key in the configuration file.

Modify your configuration as follows:

### Why could GitHub display before?

Because the Congo theme folder (`themes/congo/assets/icons/`) already has built-in `github.svg`, `youtube.svg` and other common icons. Hugo's lookup logic is: **First look for `assets` in your own root directory, if not found, then look in the theme directory.**

So, as long as you put in an SVG with the same name, you can even overwrite the default GitHub icon!

### Summary

1. **File is the Key**: Whatever the filename is, write that as the key in the configuration file.
    
2. **Location**: Put into `assets/icons/`.
    

Go try lighting up Bilibili's little TV! 📺



## vercel

### Create vercel project

Add vercel configuration file in Hugo repository

Upload Hugo repository to github, then bind github account on Vercel

Create a new project (new project) in vercel, select Hugo repository

Framework Preset can directly choose Hugo

Root Directory does not need modification


### Bind Domain

Click Domain in Hugo project management to add domain.

Follow the configuration given by vercel, modify the domain DNS configuration at the domain provider.

## Auto Deploy Script

Currently use auto script to synchronize note modifications under specific folders in obsidian to hugo directory, but if you want to add `_index.md` page to directory like `post`, you need to tile notes in its sibling level, like
```
|-content
| |-post
| |-_index.md
| |-note_dir
| | |-index.md
| | |-thumb.jpg
```

Also found that only in this way can the article summary be displayed normally
