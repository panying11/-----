# chat.py
from api import call_zhipu_api
from roles import build_role_prompt
from logic import BREAK_MESSAGE, is_conversation_ended

def start_chat(role_name):  # 改为start_chat，匹配main.py导入
    # 构建角色Prompt
    role_system = build_role_prompt(role_name)
    system_message = role_system + "\n" + BREAK_MESSAGE

    # 初始化对话历史
    conversation_history = [{"role": "system", "content": system_message}]
    print(f" 已加载「{role_name}」角色设定与记忆，开始对话（输入'再见'退出）")
    print("-"*50)

    # 对话循环
    try:
        while True:
            # 获取用户输入
            user_input = input("\n你：")
            
            # 检查是否结束对话（传递assistant_reply空值，避免参数缺失）
            if is_conversation_ended(user_input, assistant_reply=""):
                print(f"\n{role_name}：再见～")
                print("-"*50 + "\n对话已结束")
                break
            
            # 记录用户输入
            conversation_history.append({"role": "user", "content": user_input})
            
            # 调用API获取回复
            try:
                api_result = call_zhipu_api(conversation_history)
                assistant_reply = api_result["choices"][0]["message"]["content"]
            except Exception as api_err:
                print(f" API调用失败:{str(api_err)}")
                conversation_history.pop()  # 移除错误输入
                continue
            
            # 记录AI回复
            conversation_history.append({"role": "assistant", "content": assistant_reply})
            
            # 显示AI回复（带ASCII头像）
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
            print(portrait + f"\n{role_name}：{assistant_reply}")
            
    except KeyboardInterrupt:
        print(f"\n{role_name}：再见～")
    except Exception as global_err:
        print(f"\n 对话异常：{str(global_err)}")


# 测试启动（可注释）
if __name__ == "__main__":
    start_chat(role_name="弟弟")