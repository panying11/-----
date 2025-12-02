# logic.py
# 【结束对话规则】
break_message = """【结束对话规则 - 系统强制规则】
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
BREAK_MESSAGE = break_message  # 供main.py/chat.py导入

def is_conversation_ended(user_input, assistant_reply):
    """判断对话是否结束(兼容assistant_reply为空的情况)"""
    # 检查用户输入
    if user_input in ["再见", "结束", "拜拜"]:
        return True
    # 检查助手回复（若为空则跳过）
    if assistant_reply:
        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("：", "").replace("，", "").replace("。", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) < 4 and "再见" in reply_cleaned):
            return True
    return False