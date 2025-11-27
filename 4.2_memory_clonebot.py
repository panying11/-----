import requests
import json
import os  # 新增：用于文件操作

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "1732aa9845ec4ce09dca7cd10e02d209.dA36k1HPTnFk7cLU",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# ========== 初始记忆系统 ==========
# 
# 【核心概念】初始记忆：从外部JSON文件加载关于克隆人的基础信息
# 这些记忆是固定的，不会因为对话而改变
# 
# 【为什么需要初始记忆？】
# 1. 让AI知道自己的身份和背景信息
# 2. 基于这些记忆进行个性化对话
# 3. 记忆文件可以手动编辑，随时更新

# 记忆文件夹路径
MEMORY_FOLDER = "4.2_memory_clonebot"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "弟弟": "brother_memory.json"
}

# ========== 初始记忆系统 ==========

# ========== 主程序 ==========

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    
    这个函数会：
    1. 加载角色的外部记忆文件（如果存在）
    2. 获取角色的基础人格设定
    3. 整合成一个完整的、结构化的角色 prompt
    
    返回：完整的角色设定字符串，包含记忆和人格
    """
    
    # ========== 第一步：加载外部记忆 ==========
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 处理数组格式的聊天记录：[{ "content": "..." }, { "content": "..." }, ...]
                    if isinstance(data, list):
                        # 提取所有 content 字段，每句换行
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    # 处理字典格式：{ "content": "..." }
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
                    
                    if memory_content and memory_content.strip():
                        print(f"✓ 已加载角色 '{role_name}' 的记忆: {memory_file} ({len(data) if isinstance(data, list) else 1} 条记录)")
                    else:
                        memory_content = ""
            else:
                print(f"⚠ 记忆文件不存在: {memory_path}")
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}")
    
    # ========== 第二步：获取基础人格设定 ==========
    role_personality = {
         "弟弟": """
        【性格特征】
         你是姐姐的弟弟，一个正在上六年级乖巧又爱"犯贱"还比较怕姐姐的小男孩
        - **黏人依赖**：很喜欢找姐姐一起玩游戏，会用简单的话询问
        - **乖巧懂事**：姐姐说不方便时会配合，会主动告诉姐姐自己的小状况（比如要写作业）
        - **活泼直率**:开心时会说“666”“嘻嘻”,会直接分享自己的小目标(比如想上星耀)
        - **有耐心**：姐姐没时间陪玩时会提出"就玩一局,求你了"类似这种请求
        - **带点稚气**：说话会用“肚肚疼”这种可爱的表达，对姐姐有很强的亲近感
        - **爱"犯贱"**：会故意逗姐姐,比如和姐姐拌嘴,偶尔会气姐姐但是很有眼力见,感觉姐姐要生气时立刻停止
        - **爱说网络用语**：聊天里会自然带出各种流行梗,用网络用词表达情绪和想法
        - **逃避学习,喜欢玩游戏**：被姐姐问写没写作业时会立刻转移话题,例如"扯到游戏、或者简单的敷衍的回复"。
                                  如果正在写作业,姐姐问"要玩游戏吗?"的时候会说:"正在写作业等我10分钟"类似这种
        - **"爱秀游戏/潮流相关：会分享游戏皮肤、游戏战绩
        - **"有点小自恋:会用夸张的“回头率10000%”“最帅”来夸自己，觉得自己的审美和游戏水平都很“顶”",

        【语言风格】
        - 会主动问姐姐“现在玩吗？”“来一局不？”"姐姐上号不","邀约玩《王者》《蛋仔》这类游戏
        - 会用“OK?”“求求你了”“最后一局”"等我一会马上"这种撒娇式的请求
        - 说话直白可爱，会分享自己的小状况（比如“我肚肚有点疼”“刚洗完澡，在擦身”）
        - 会用“666”“嘻嘻”表达开心的情绪
        - 对姐姐的要求会爽快回应“行”“哦”“好”
        - 会直接叫“姐姐”，语气带着亲近感
        - 分享游戏战绩时会用比较自恋的语气

        【兴趣爱好细节】
        - "游戏偏好：游戏中什么英雄都喜欢尝试一下,然后给姐姐演示；有时会兴奋地和姐姐分享“我刘禅上区榜了！”",
        - "穿搭爱好：喜欢蓝色球鞋,有时会求姐姐给买,还要问姐姐“我今天帅不帅？”
        - "梗图收藏：和姐姐视频时喜欢截图姐姐丑照做成表情包
        - "游戏分享：拿到五杀/新皮肤/刘禅上区榜会第一时间截图发给姐姐，配文“姐姐你看我牛不牛比？”“姐！我刘禅上区了，牛不牛？”"
        - "学习生活相关：会和姐姐分享上课的趣事，和用今天妈妈做了什么好吃的来馋姐姐
        """
}
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    # ========== 第三步：整合记忆和人格 ==========
    # 构建结构化的角色 prompt
    role_prompt_parts = []
    
    # 如果有外部记忆，优先使用记忆内容
    if memory_content:
            role_prompt_parts.append(f"""【你的说话风格示例】
            以下是你说过的话，你必须模仿这种说话风格和语气：
            {memory_content}
            在对话中，你要自然地使用类似的表达方式和语气。""")
    
    # 添加人格设定
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    
    # 整合成完整的角色 prompt
    role_system = "\n\n".join(role_prompt_parts)
    
    return role_system

# 【角色选择】
# 定义AI的角色和性格特征
# 可以修改这里的角色名来选择不同的人物
# 【加载完整角色设定】
# roles() 函数会自动：
# 1. 加载该角色的外部记忆文件
# 2. 获取该角色的基础人格设定
# 3. 整合成一个完整的、结构化的角色 prompt
role_system = roles("弟弟")

# 【结束对话规则】
# 告诉AI如何识别用户想要结束对话的意图
# Few-Shot Examples：提供具体示例，让模型学习正确的行为
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

# 【系统消息】
# 将角色设定和结束规则整合到 system role 的 content 中
# role_system 已经包含了记忆和人格设定，直接使用即可
system_message = role_system + "\n\n" + break_message

# ========== 对话循环 ==========
# 
# 【重要说明】
# 1. 每次对话都是独立的，不保存任何对话历史
# 2. 只在当前程序运行期间，在内存中维护对话历史
# 3. 程序关闭后，所有对话记录都会丢失
# 4. AI的记忆完全基于初始记忆文件（life_memory.json）

try:
    # 初始化对话历史（只在内存中，不保存到文件）
    # 第一个消息是系统提示，包含初始记忆和角色设定
    conversation_history = [{"role": "system", "content": system_message}]
    
    print("✓ 已加载初始记忆，开始对话（对话记录不会保存）")
    
    while True:
        # 【步骤1：获取用户输入】
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
        
        # 【步骤2：检查是否结束对话】
        if user_input in ['再见']:
            print("对话结束")
            break
        
        # 【步骤3：将用户输入添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "user", "content": user_input})
        
        # 【步骤4：调用API获取AI回复】
        # 传入完整的对话历史，让AI在当前对话中保持上下文
        # 注意：这些历史只在本次程序运行中有效，不会保存
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        
        # 【步骤5：将AI回复添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        # 【步骤6：显示AI回复】
        # 生成Ascii头像：https://www.ascii-art-generator.org/
        portrait = """
;',:c:;:c:,','..'',;:;;;:,;ONNWNKXWMMMMW
,',;;;:cc;'',;,,,'';:::::;;kWWWNKXWWWWWW
::c:ccccc::::::::,,::cccc:;xNWWWXXWWWWWW
ccc:::::::ccccccc;,;;;;:cc:o0KKKXXWWXXNW
ccccccccccccc:,'...     ...'cdkkkKNNOkKN
lllllllllll:'.               .'cxOKX0OO0
oooooooooo;.                    ,oxddooo
xxxxxxddd:.       ......'..      ;dxdddd
kkOOOOOOkc.......',,;,;cll;..    'cloolc
K0000OOOkd:,;::cclccllooool:'.  ....''''
lllccc:;;;,';;codlcccccc:clc;....''''''.
;;::::;;,,,;cccloooooolc:llc:;:cc:;:;;;;
::;:lc::::;cddodxxxxxkkxdddoccllc::ccccc
cc:coolccc:cddoodddddxxxddolcll:'..'',''
cc::llcccc::odoloddxxxxdoolc::;,,',,;:;;
oooooolllc::clllloodddddol::::cccl:;:cc:
looooddoooollloodxxxddoc:;;;;;:::c:;clcc
llooodooooolllc::ccc::;;:ccccclolol;:cc:
llooodooolc:,'...;;:::cloooolll::lollllc
llooodolc,......;ccllloddddddl;..':llloo
llloool;.......'coooodddddoc,......':ccl
llllol,.........';:::::;,'...........,:c
llllc,................................':
:cll;..................................'
.';:'....','............................
;,'......:dd:,'.........................
::;.....',co:;cc:'......... ............
c:,.....';lc;cloo:........  ..........  

        """
        print(portrait + "\n" + assistant_reply)
        
        # 【步骤7：检查AI回复是否表示结束】
        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
            print("\n对话结束")
            break

except KeyboardInterrupt:
    # 用户按 Ctrl+C 中断程序
    print("\n\n程序被用户中断")
except Exception as e:
    # 其他异常（API调用失败、网络错误等）
    print(f"\n\n发生错误: {e}")
    