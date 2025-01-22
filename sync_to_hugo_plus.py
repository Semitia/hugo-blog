import os
import shutil
from datetime import datetime, timedelta
import urllib.parse

# 定义 Obsidian 和 Hugo 的主目录路径
obsidian_root = os.path.expanduser("~/文档/ObsidianRepo")
hugo_root = os.path.expanduser("~/Blogs/Hugo")

# 定义 Obsidian 的 posts 目录和附件目录
obsidian_posts = os.path.join(obsidian_root, "posts")
obsidian_attachments = os.path.join(obsidian_root, "Attachment")

# 定义 Hugo 的 content 和 static 目录
hugo_content = os.path.join(hugo_root, "content")
hugo_static = os.path.join(hugo_root, "static")

# 定义同步的时间间隔（例如，30天）
time_interval = timedelta(days=30)

def sync_obsidian_to_hugo():
    """
    同步 Obsidian 的笔记和附件到 Hugo 的内容目录
    """
    for root, dirs, files in os.walk(obsidian_posts):
        for file in files:
            if file.endswith(".md"):  # 找到 Markdown 文件
                # 获取笔记的相对路径
                relative_path = os.path.relpath(root, obsidian_posts)  # 相对posts目录的路径
                note_name, _ = os.path.splitext(file)

                # 获取文件的修改时间
                obsidian_note_path = os.path.join(root, file)
                last_modified_time = datetime.fromtimestamp(os.path.getmtime(obsidian_note_path))
                time_since_modified = datetime.now() - last_modified_time

                if time_since_modified > time_interval:
                    print(f"Skipping note (not modified within interval): {file}")
                    continue

                # 笔记在 Hugo 的目标路径
                hugo_note_dir = os.path.join(hugo_content, "posts", note_name)
                os.makedirs(hugo_note_dir, exist_ok=True)

                # 复制 Markdown 文件到目标路径，并改名
                hugo_note_path_zh = os.path.join(hugo_note_dir, "index.zh-Hans.md")
                hugo_note_path_en = os.path.join(hugo_note_dir, "index.md")
                shutil.copy2(obsidian_note_path, hugo_note_path_zh)
                shutil.copy2(obsidian_note_path, hugo_note_path_en)

                print(f"Copied note: {obsidian_note_path} -> {hugo_note_path_zh}")
                print(f"Copied note: {obsidian_note_path} -> {hugo_note_path_en}")

                # 查找并复制图片
                obsidian_image_dir = os.path.join(obsidian_attachments, "posts", relative_path, note_name)
                if os.path.exists(obsidian_image_dir):
                    images = os.listdir(obsidian_image_dir)
                    if images:
                        # 复制第一张图片并重命名为thumb
                        first_image = images[0] 
                        first_image_ext = os.path.splitext(first_image)[1] # 获取扩展名 
                        thumb_name = f"thumb{first_image_ext}" 
                        obsidian_image_path = os.path.join(obsidian_image_dir, first_image) 
                        hugo_image_path = os.path.join(hugo_note_dir, thumb_name) 
                        shutil.copy2(obsidian_image_path, hugo_image_path) 
                        print(f"Copied first image as thumb: {obsidian_image_path} -> {hugo_image_path}")

                    # 复制所有图片到 static 目录
                    hugo_image_static_dir = os.path.join(hugo_static, "img", "posts", relative_path, note_name)
                    os.makedirs(hugo_image_static_dir, exist_ok=True)
                    for image_file in images:
                        obsidian_image_path = os.path.join(obsidian_image_dir, image_file)
                        hugo_image_static_path = os.path.join(hugo_image_static_dir, image_file)
                        shutil.copy2(obsidian_image_path, hugo_image_static_path)
                        print(f"Copied image: {obsidian_image_path} -> {hugo_image_static_path}")

                        # 修改 Markdown 文件中的图片引用，使用 URL 编码处理空格 
                        image_url = urllib.parse.quote(f"/img/posts/{relative_path}/{note_name}/{image_file}") 
                        with open(hugo_note_path_zh, 'r') as file: 
                            content = file.read() 
                            new_content = content.replace(f"![[{image_file}]]", f"![{image_file}]({image_url})") 
                        with open(hugo_note_path_zh, 'w') as file: 
                            file.write(new_content) 
                        with open(hugo_note_path_en, 'r') as file: 
                            content = file.read() 
                            new_content = content.replace(f"![[{image_file}]]", f"![{image_file}]({image_url})") 
                        with open(hugo_note_path_en, 'w') as file: 
                            file.write(new_content)
                else:
                    print(f"No images found for note: {file}")

if __name__ == "__main__":
    sync_obsidian_to_hugo()
