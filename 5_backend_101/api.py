import requests
import json

try:
    import streamlit as st
    ZHIPU_API_KEY = st.secrets.get("ZHIPU_API_KEY", "3c997c293ba3487681f3c03f510524c1.q7EenptfOOR7tpmO")
except:
    ZHIPU_API_KEY = "3c997c293ba3487681f3c03f510524c1.q7EenptfOOR7tpmO"

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5   
    }

    response = requests.post(
        url, 
        headers=headers, 
        json=data,
        timeout=30
    )
    response.encoding = 'utf-8'

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")