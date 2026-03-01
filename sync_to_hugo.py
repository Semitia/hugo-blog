import os
import shutil
from datetime import datetime, timedelta
import urllib.parse
import glob

# ================= 配置区域 =================

# Obsidian 和 Hugo 的主目录
# obsidian_root = os.path.expanduser("~/文档/ObsidianRepo")
obsidian_root = os.path.expanduser("/mnt/d/WORK/ObsidianRepo")
hugo_root = os.path.expanduser("~/Blogs/hugo-blog")

obsidian_attachments_root = os.path.join(obsidian_root, "Attachment")
hugo_content_root = os.path.join(hugo_root, "content")
hugo_static_root = os.path.join(hugo_root, "static")

# 同步的文件夹
SYNC_FOLDERS = ["Posts", "Notes", "Projects", "Essays"]

# 时间限制
time_interval = timedelta(days=30)

# 图片格式优先级 (排在前面的会被优先保留)
# 如果文件夹里同时有 image.png 和 image.webp，脚本只复制 .webp，并让 Markdown 指向它
EXT_PRIORITY = ['.webp', '.png', '.jpg', '.jpeg', '.gif', '.svg']

# ===========================================

def get_priority_index(filename):
    """获取文件扩展名的优先级索引，未定义的排在最后"""
    ext = os.path.splitext(filename)[1].lower()
    if ext in EXT_PRIORITY:
        return EXT_PRIORITY.index(ext)
    return 999

def smart_copy_image(src_path, dest_dir, dest_filename=None):
    """
    智能复制：
    1. 复制文件到目标位置。
    2. 删除目标位置同名但后缀不同的所有旧文件。
    """
    if not os.path.exists(src_path):
        return

    if dest_filename:
        final_filename = dest_filename
    else:
        final_filename = os.path.basename(src_path)
    
    file_name_no_ext = os.path.splitext(final_filename)[0]
    dest_path = os.path.join(dest_dir, final_filename)

    # === 强力清理逻辑 ===
    # 查找目标目录下所有同名文件 (image.*)
    # 使用 glob.escape 防止文件名中有 [ ] 等特殊字符导致匹配失败
    safe_search_path = os.path.join(glob.escape(dest_dir), f"{glob.escape(file_name_no_ext)}.*")
    existing_files = glob.glob(safe_search_path)
    
    for existing_file in existing_files:
        existing_name = os.path.basename(existing_file)
        # 如果文件名不同（即后缀不同），删除它
        if existing_name != final_filename:
            try:
                os.remove(existing_file)
                print(f"   [Clean] Deleted redundant file: {existing_name}")
            except OSError as e:
                print(f"   [Error] Could not delete {existing_name}: {e}")

    # === 复制逻辑 ===
    # 只有当源文件修改时间比目标新，或者目标不存在时才复制（节省IO）
    should_copy = True
    if os.path.exists(dest_path):
        src_mtime = os.path.getmtime(src_path)
        dest_mtime = os.path.getmtime(dest_path)
        if src_mtime <= dest_mtime:
            should_copy = False
    
    if should_copy:
        shutil.copy2(src_path, dest_path)
        print(f"   [Copy] {src_path} -> {final_filename}")

def process_markdown_images(file_path, image_map):
    """替换 Markdown 图片链接"""
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    # image_map: { '原文件名.png': '新路径.webp', '原文件名.webp': '新路径.webp' }
    for original_name, new_url in image_map.items():
        # 替换 ![[image.png]] 格式
        obsidian_link = f"![[{original_name}]]"
        hugo_link = f"![{original_name}]({new_url})"
        new_content = new_content.replace(obsidian_link, hugo_link)
        
        # 兼容处理：如果 Markdown 里已经写的是标准链接 ![xxx](yyy)，这里暂不处理，以免复杂化

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"   [Update] Updated links in {os.path.basename(file_path)}")

def sync_folder(folder_name):
    source_dir = os.path.join(obsidian_root, folder_name)
    if not os.path.exists(source_dir):
        return

    print(f"\n=== Processing Folder: {folder_name} ===")

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".md"):
                relative_path = os.path.relpath(root, source_dir)
                note_name, _ = os.path.splitext(file)
                obsidian_note_path = os.path.join(root, file)

                # 检查笔记是否过期
                last_modified = datetime.fromtimestamp(os.path.getmtime(obsidian_note_path))
                if datetime.now() - last_modified > time_interval:
                    continue
                
                print(f"> Checking Note: {file}")

                # 准备目录
                hugo_note_dir = os.path.join(hugo_content_root, folder_name, note_name)
                os.makedirs(hugo_note_dir, exist_ok=True)

                # 复制 Markdown 
                hugo_zh = os.path.join(hugo_note_dir, "index.zh-Hans.md")
                hugo_en = os.path.join(hugo_note_dir, "index.md")
                shutil.copy2(obsidian_note_path, hugo_zh)
                # shutil.copy2(obsidian_note_path, hugo_en)

                # === 处理图片 (新增分组逻辑) ===
                # [删除] 原来的逻辑：寻找 Attachment/posts/分类/笔记名
                # obsidian_img_dir = os.path.join(obsidian_attachments_root, folder_name, relative_path, note_name)
                # [新增] 现在的逻辑：直接寻找 Attachment/笔记名
                obsidian_img_dir = os.path.join(obsidian_attachments_root, note_name)
                
                image_url_map = {}

                if os.path.exists(obsidian_img_dir):
                    # 获取该目录下所有文件
                    raw_images = [img for img in os.listdir(obsidian_img_dir) if not img.startswith('.')]
                    
                    # 1. 按文件主名分组： {'img1': ['img1.png', 'img1.webp'], 'img2': ['img2.jpg']}
                    image_groups = {}
                    for img in raw_images:
                        stem = os.path.splitext(img)[0]
                        if stem not in image_groups:
                            image_groups[stem] = []
                        image_groups[stem].append(img)

                    # 2. 处理每一组
                    # 目标：从一组里选出一个 Best，复制过去，然后让组里所有名字都指向这个 Best 的 URL
                    
                    # 排序 key：是否是第一张图（封面），以及文件名排序
                    # 这里为了找出 Thumb，我们先按文件名排序，默认第一张为封面
                    sorted_stems = sorted(image_groups.keys())

                    for idx, stem in enumerate(sorted_stems):
                        group_files = image_groups[stem]
                        
                        # 在这一组里，根据优先级选出最好的文件 (webp > png ...)
                        best_image = sorted(group_files, key=lambda x: get_priority_index(x))[0]
                        best_image_path = os.path.join(obsidian_img_dir, best_image)
                        
                        # --- 处理封面逻辑 (Thumb) ---
                        if idx == 0: 
                            # 如果是这一组是本篇笔记的第一张图，做成封面
                            _, ext = os.path.splitext(best_image)
                            thumb_name = f"thumb{ext}"
                            smart_copy_image(best_image_path, hugo_note_dir, dest_filename=thumb_name)

                        # --- 处理正文图片逻辑 ---
                        # 确定目标路径
                        hugo_static_target_dir = os.path.join(hugo_static_root, "img", folder_name, relative_path, note_name)
                        os.makedirs(hugo_static_target_dir, exist_ok=True)
                        
                        # 复制 Best Image 到 static
                        smart_copy_image(best_image_path, hugo_static_target_dir)

                        # 生成 URL
                        # URL 指向的是那个 Best Image
                        raw_url_path = f"/img/{folder_name}/{relative_path}/{note_name}/{best_image}"
                        raw_url_path = raw_url_path.replace("\\", "/") # Win路径修正
                        encoded_url = urllib.parse.quote(raw_url_path)

                        # --- 关键：建立映射 ---
                        # 无论 Markdown 里引用的是 .png 还是 .webp，都映射到这个 Best Image 的 URL
                        for variant in group_files:
                            image_url_map[variant] = encoded_url

                # === 替换链接 ===
                if image_url_map:
                    process_markdown_images(hugo_zh, image_url_map)
                    process_markdown_images(hugo_en, image_url_map)

def sync_obsidian_to_hugo():
    print("Starting Sync...")
    for folder in SYNC_FOLDERS:
        sync_folder(folder)
    print("\nSync Complete.")

if __name__ == "__main__":
    sync_obsidian_to_hugo()