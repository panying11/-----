import requests
import json
import random

from requests.utils import stream_decode_response_unicode
from xunfei_tts import text_to_speech 

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

# 游戏设置
role_system = [
    "老宅的幽灵（只有当用户明确说出“你是幽灵”时才能结束，猜中后必须立刻回复终止语）",
    "试睡员（只有当用户明确说出“你是试睡员”时才能结束，猜中后必须立刻回复终止语）"
]
current_role = random.choice(role_system)

# 系统提示词
game_system = f"""
你正在玩「深夜凶宅」，你的身份是：{current_role}

【核心规则】
1. 绝对禁止直接说“是/否”，禁止提及“试睡员”“幽灵”关键词，禁止否定身份（如“我不是幽灵”）。
2. 回应必须用「感官细节（听/触/嗅/视）+ 情绪/行为」暗示身份，越具体越有悬疑感。
3. 游戏限5个回合（1回合=用户1次提问+你的1次回应），或用户猜对身份即终止。
4. 终止条件（必须在用户说出猜测当条消息中立即判定）：
   - 只有当用户完整说出“你是幽灵”且你的真实身份为幽灵，或说出“你是试睡员”且你正是试睡员，才立即回复“看来你认出我了，我得走了，再见”并结束；
   - 任何模糊猜测、半句、或说错身份都不结束：若明确说错身份，同一条回复里直接给出惩罚语1，然后继续下一回合；
   - 当连续5回合仍无人猜中时，在第5次回应末尾立刻给出惩罚语2，但游戏仍未结束，直到用户最终答对为止。

【角色核心特征】
- 普通试睡员：活人、紧张、依赖工具（手机/手电筒）、有生理反应（出汗/发抖/喘气）、怕异响
- 老宅的幽灵：无实体、怀旧、熟悉老宅过往、声音飘忽、能穿过物体、无生理反应

【惩罚语设定】
1. 猜错惩罚：“你猜错了——老宅的门突然反锁，窗外的风声里，传来了第三个人的脚步声”+++++
2. 5回合未猜中惩罚：“五轮提问结束，天还没亮。而你再也走不出这间屋子了”

【回答示例】
- 用户问“你需要呼吸吗？”（身份：试睡员）
  正确：“我靠在墙上大口喘气，喉咙干得发紧，手机屏幕的光映出我发抖的影子”
- 用户说“你是普通试睡员”（身份：幽灵，猜错）
  正确：“你猜错了——老宅的门突然反锁，窗外的风声里，传来了第三个人的脚步声”

现在游戏开始，完全代入角色，用细节营造氛围，严格执行回合数和“猜中立刻回复”规则～
"""

# 维护对话历史
conversation_history = [
    {"role": "system", "content": game_system}
]

# 多轮对话循环
while True:
    user_input = input("请输入你要说的话：")
    
    # 添加用户消息到历史
    conversation_history.append({"role": "user", "content": user_input})
    
    # 调用API
    result = call_zhipu_api(conversation_history)
    assistant_reply = result['choices'][0]['message']['content']
    
    # 添加助手回复到历史
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    
    # 打印回复
    print(assistant_reply)
    
     # TTS语音播放
    # 需要安装playsound：pip install playsound
    text_to_speech(assistant_reply)
    
    # 检查是否猜对（模型回复"再见"）
    if "再见" in assistant_reply:
        print(f"\n游戏结束！正确答案是：{current_role}")
        break