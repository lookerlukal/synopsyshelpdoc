import os
import json

def scan_directory(root_dir, base_path="", level=0):
    """
    扫描目录结构并生成树形数据
    :param root_dir: 要扫描的根目录
    :param base_path: 当前相对路径
    :param level: 当前层级
    :return: 目录结构列表
    """
    result = []
    try:
        items = sorted(os.listdir(os.path.join(root_dir, base_path)), key=lambda x: (not os.path.isdir(os.path.join(root_dir, base_path, x)), x))
    except PermissionError:
        return result

    for name in items:
        if name.startswith('.'):  # 跳过隐藏文件
            continue
            
        full_path = os.path.join(root_dir, base_path, name)
        rel_path = os.path.join(base_path, name)
        
        if os.path.isdir(full_path):
            # 处理目录
            children = scan_directory(root_dir, rel_path, level+1)
            index_file = os.path.join(full_path, "index.html")
            
            node = {
                "name": " ".join([part.capitalize() for part in name.split('_')]),
                "level": level,
                "children": children
            }
            
            # 如果目录中有index.html则作为入口文件
            if os.path.isfile(index_file):
                node["url"] = rel_path.replace("\\", "/") + "/index.html"
                
            if children or node.get("url"):
                result.append(node)
        else:
            # 只处理HTML文件
            if name.lower().endswith(('.html', '.htm')):
                # 跳过自动生成的索引文件
                if name.lower() in ["index.html", "default.html"]:
                    continue
                    
                result.append({
                    "name": " ".join([part.capitalize() for part in os.path.splitext(name)[0].split('_')]),
                    "url": rel_path.replace("\\", "/"),
                    "level": level
                })
    
    return result

def generate_toc(root_dir, output_file="toc.json"):
    """
    生成目录结构文件
    :param root_dir: 要扫描的根目录路径
    :param output_file: 输出文件名
    """
    toc_data = scan_directory(root_dir)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(toc_data, f, indent=2, ensure_ascii=False)
    
    print(f"成功生成目录文件 {output_file}，共 {len(toc_data)} 个顶级条目")

if __name__ == "__main__":
    # 使用示例
    content_dir = input("请输入要扫描的目录路径（留空则使用当前目录）: ") or "."
    generate_toc(content_dir) 