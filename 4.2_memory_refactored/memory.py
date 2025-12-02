import os
import json

# 修正记忆文件夹路径
MEMORY_FOLDER = "4.2_memory_refactored" 
ROLE_MEMORY_MAP = {
    "弟弟": "brother_memory.json"
}

def load_role_memory(role_name):
    """加载角色的外部记忆文件"""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    if not memory_file:
        return ""
    
    memory_path = os.path.join(MEMORY_FOLDER, memory_file)
    try:
        if os.path.exists(memory_path):
            with open(memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 处理记忆内容
            if isinstance(data, list):
                contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                memory_content = '\n'.join(contents)
            elif isinstance(data, dict):
                memory_content = data.get('content', str(data))
            else:
                memory_content = str(data)
            
            if memory_content.strip():
                print(f" 已加载角色「{role_name}」的记忆：{memory_file}({len(data) if isinstance(data, list) else 1}条记录）")
                return memory_content
        else:
            print(f" 记忆文件不存在：{memory_path}")
    except Exception as e:
        print(f" 加载记忆失败：{e}")
    return ""