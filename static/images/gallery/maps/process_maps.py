#!/usr/bin/env python3
"""
自动处理地图图片：切片、生成缩略图、更新 gallery.yml
使用方法：
    cd static/images/gallery/maps
    python process_maps.py
"""

import os
import subprocess
import yaml
from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET

# 解除 PIL 图片大小限制
Image.MAX_IMAGE_PIXELS = None

# CDN
CDN_BASE_URL = "https://maps.andrepimpo.wang"

SCRIPT_DIR = Path(__file__).parent
MAPS_DIR = SCRIPT_DIR
DATA_DIR = SCRIPT_DIR.parent.parent.parent.parent / "data"
GALLERY_YML = DATA_DIR / "gallery.yml"

def get_png_files():
    """获取所有未切片的 PNG 文件"""
    png_files = []
    for file in MAPS_DIR.glob("*.png"):
        folder_name = file.stem
        if not (MAPS_DIR / folder_name).exists():
            png_files.append(file)
    return png_files

def tile_image(png_file):
    """使用 gdal2tiles 切片"""
    map_name = png_file.stem
    output_dir = MAPS_DIR / map_name
    
    print(f"正在切片: {png_file.name} -> {map_name}/")
    
    cmd = [
        "python", "gdal2tiles.py",
        "-l", "-p", "raster",
        "-z", "0-5",
        str(png_file),
        str(map_name)
    ]
    
    subprocess.run(cmd, cwd=MAPS_DIR, check=True)
    print(f"✓ 切片完成: {map_name}")
    
    return output_dir

def generate_thumbnail(png_file, max_size_mb=1):
    """生成缩略图（不超过指定大小）"""
    thumb_name = f"{png_file.stem}_thumb.jpg"
    thumb_path = MAPS_DIR / thumb_name
    
    print(f"正在生成缩略图: {thumb_name}")
    
    img = Image.open(png_file)
    
    # 逐步降低质量直到文件小于 max_size_mb
    quality = 85
    width, height = img.size
    
    # 先缩放到合适尺寸（长边不超过1200px）
    max_dimension = 1200
    if max(width, height) > max_dimension:
        ratio = max_dimension / max(width, height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Convert RGBA to RGB if needed
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    
    # 调整质量直到满足大小要求
    while quality > 20:
        img.save(thumb_path, 'JPEG', quality=quality, optimize=True)
        size_mb = thumb_path.stat().st_size / (1024 * 1024)
        if size_mb <= max_size_mb:
            break
        quality -= 5
    
    print(f"✓ 缩略图生成: {thumb_name} ({size_mb:.2f}MB, quality={quality})")
    return thumb_name

def parse_tilemapresource(tile_dir):
    """解析 tilemapresource.xml 获取地图信息"""
    xml_path = tile_dir / "tilemapresource.xml"
    
    if not xml_path.exists():
        return None
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # 获取 BoundingBox
    bbox = root.find('.//BoundingBox')
    if bbox is not None:
        width = abs(float(bbox.get('maxx')) - float(bbox.get('minx')))
        height = abs(float(bbox.get('maxy')) - float(bbox.get('miny')))
    else:
        width, height = 10000, 10000  # 默认值
    
    # 获取最大 zoom level
    tilesets = root.findall('.//TileSet')
    max_zoom = len(tilesets) - 1 if tilesets else 5
    
    return {
        'width': int(width),
        'height': int(height),
        'maxZoom': max_zoom
    }

def update_gallery_yml(processed_maps):
    """更新 gallery.yml"""
    
    # 读取现有的 gallery.yml（如果存在）
    if GALLERY_YML.exists():
        with open(GALLERY_YML, 'r', encoding='utf-8') as f:
            gallery_data = yaml.safe_load(f) or []
    else:
        gallery_data = []
    
    # 获取已存在的地图名称
    existing_maps = {item.get('title') for item in gallery_data if item.get('type') == 'map'}
    
    # 添加新处理的地图
    for map_info in processed_maps:
        title = map_info['name']
        if title not in existing_maps:
            gallery_data.append({
                'title': title,
                'image': f"{CDN_BASE_URL}/{map_info['name']}.png",
                'thumbnail': f"{CDN_BASE_URL}/{map_info['thumbnail']}",
                'type': 'map',
                'tiles': f"{CDN_BASE_URL}/{map_info['name']}/{{z}}/{{x}}/{{y}}.png",
                'width': map_info['width'],
                'height': map_info['height'],
                'maxZoom': map_info['maxZoom']
            })
            print(f"✓ 添加到 gallery.yml: {title}")
    
    # 写入 gallery.yml
    GALLERY_YML.parent.mkdir(parents=True, exist_ok=True)
    with open(GALLERY_YML, 'w', encoding='utf-8') as f:
        yaml.dump(gallery_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"✓ gallery.yml 已更新")

def main():
    print("=" * 50)
    print("地图自动处理脚本")
    print("=" * 50)
    
    # 获取待处理的 PNG 文件
    png_files = get_png_files()
    
    if not png_files:
        print("没有需要处理的地图文件")
        return
    
    print(f"\n找到 {len(png_files)} 个待处理文件:")
    for f in png_files:
        print(f"  - {f.name}")
    
    processed_maps = []
    
    for png_file in png_files:
        print(f"\n处理: {png_file.name}")
        print("-" * 50)
        
        try:
            # 1. 切片
            tile_dir = tile_image(png_file)
            
            # 2. 生成缩略图
            thumbnail = generate_thumbnail(png_file)
            
            # 3. 解析 XML 获取信息
            map_info = parse_tilemapresource(tile_dir)
            
            if map_info:
                processed_maps.append({
                    'name': png_file.stem,
                    'thumbnail': thumbnail,
                    **map_info
                })
            
        except Exception as e:
            print(f"✗ 处理失败: {e}")
            continue
    
    # 4. 更新 gallery.yml
    if processed_maps:
        print("\n" + "=" * 50)
        update_gallery_yml(processed_maps)
    
    print("\n完成！")

if __name__ == "__main__":
    main()