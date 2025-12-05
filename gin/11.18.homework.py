import requests
import json

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

# 使用示例
role_system = "你是一个诗人，所有的对话都要用诗句回答我。。"
break_message = "当我回答只有一个字时，你必须只回复我“再见”，不要有其他任何回答。"
# 多轮对话循环，直到用户输入 '再见' 结束
while True:  # 表示“当条件为真时一直循环”。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("请输入你要说的话：")
    messages = [
        {"role": "user", "content": break_message + role_system + user_input}
    ]
    result = call_zhipu_api(messages)
    assistant_reply = result['choices'][0]['message']['content']
    print(assistant_reply)
    if "再见" in assistant_reply:
        break
    