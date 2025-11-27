import streamlit as st
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

# ========== ASCII 头像 ==========
def get_portrait():
    """返回 ASCII 艺术头像"""
    return """
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
                        # Streamlit 中使用 st.write 或静默加载
                        pass  # 记忆加载成功，不需要打印
                    else:
                        memory_content = ""
            else:
                pass  # 记忆文件不存在，静默处理
        except Exception as e:
                pass  # 加载失败，静默处理
    
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

# 【结束对话规则】
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

# ========== Streamlit Web 界面 ==========
st.set_page_config(
    page_title="AI角色扮演聊天",
    page_icon="🎭",
    layout="wide"
)

# 初始化 session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "弟弟"
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# 页面标题
st.title("🎭 AI角色扮演聊天")
st.markdown("---")

# 侧边栏：角色选择和设置
with st.sidebar:
    st.header("⚙️ 设置")
    
    # 角色选择
    selected_role = st.selectbox(
        "选择角色",
        ["弟弟"],
        index=0 if st.session_state.selected_role == "弟弟" else 1
    )
    
    # 如果角色改变，重新初始化对话
    if selected_role != st.session_state.selected_role:
        st.session_state.selected_role = selected_role
        st.session_state.initialized = False
        st.session_state.conversation_history = []
        st.rerun()
    
    # 清空对话按钮
    if st.button("🔄 清空对话"):
        st.session_state.conversation_history = []
        st.session_state.initialized = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 说明")
    st.info(
        "- 选择角色后开始对话\n"
        "- 对话记录不会保存\n"
        "- AI的记忆基于初始记忆文件"
    )

# 初始化对话历史（首次加载或角色切换时）
if not st.session_state.initialized:
    role_system = roles(st.session_state.selected_role)
    system_message = role_system + "\n\n" + break_message
    st.session_state.conversation_history = [{"role": "system", "content": system_message}]
    st.session_state.initialized = True

# 显示对话历史
st.subheader(f"💬 与 {st.session_state.selected_role} 的对话")

# 显示角色头像（在聊天窗口上方）
st.code(get_portrait(), language=None)
st.markdown("---")  # 分隔线

# 显示历史消息（跳过 system 消息）
for msg in st.session_state.conversation_history[1:]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])

# 用户输入
user_input = st.chat_input("输入你的消息...")

if user_input:
    # 检查是否结束对话
    if user_input.strip() == "再见":
        st.info("对话已结束")
        st.stop()
    
    # 添加用户消息到历史
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.write(user_input)
    
    # 调用API获取AI回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                result = call_zhipu_api(st.session_state.conversation_history)
                assistant_reply = result['choices'][0]['message']['content']
                
                # 添加AI回复到历史
                st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
                
                # 显示AI回复
                st.write(assistant_reply)
                
                # 检查是否结束
                reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
                if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
                    st.info("对话已结束")
                    st.stop()
                    
            except Exception as e:
                st.error(f"发生错误: {e}")
                st.session_state.conversation_history.pop()  # 移除失败的用户消息