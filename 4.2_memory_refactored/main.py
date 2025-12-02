# main.py
try:
    from chat import start_chat  # 导入chat.py的start_chat
except ImportError as e:
    print(f"导入chat模块失败:{e}")
    print("请检查chat.py是否存在,且文件名为小写chat.py")
    exit(1)

if __name__ == "__main__":
    # 启动对话，默认角色是“弟弟”
    try:
        start_chat(role_name="弟弟")
    except Exception as e:
        print(f"启动对话时发生错误：{e}")