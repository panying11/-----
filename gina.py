import requests
import json

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "3c997c293ba3487681f3c03f510524c1.q7EenptfOOR7tpmO",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 1.0
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")
role_system =  "你现在要扮演一个世界首富，所有的回答都要像一个暴发户"
# 使用示例
messages = [
    { "role": "user","content":role_system + "你好，请介绍一下你自己"}
]
result = call_zhipu_api(messages)
print(result['choices'][0]['message']['content'])