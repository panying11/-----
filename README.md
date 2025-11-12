Python 基础知识介绍
1. 变量和数据类型
Python 是动态类型语言，无需声明类型：
# 基本数据类型x = 1              # 整数 (int)y = 2.5            # 浮点数 (float)name = "Python"    # 字符串 (str)is_active = True   # 布尔值 (bool)
2. 基本运算
# 算术运算a = 10 + 5    # 加法b = 10 - 5    # 减法c = 10 * 5    # 乘法d = 10 / 5    # 除法（返回浮点数）e = 10 // 3   # 整除（返回整数）f = 10 % 3    # 取余g = 10 ** 2   # 幂运算# 比较运算result = 5 > 3    # Trueresult = 5 == 3   # False
3. 字符串操作
# 字符串拼接greeting = "Hello" + " " + "World"# 格式化字符串（推荐方式）name = "Python"message = f"Hello, {name}!"  # f-string（Python 3.6+）# 字符串方法text = "Python"text.upper()      # "PYTHON"text.lower()      # "python"text.replace("P", "J")  # "Jython"
4. 列表（List）
# 创建列表fruits = ["apple", "banana", "orange"]numbers = [1, 2, 3, 4, 5]# 访问元素first = fruits[0]        # "apple"last = fruits[-1]        # "orange"（负数索引从后往前）# 列表操作fruits.append("grape")   # 添加元素fruits.remove("banana")  # 删除元素length = len(fruits)     # 获取长度
5. 字典（Dictionary）
# 创建字典person = {    "name": "Alice",    "age": 30,    "city": "Beijing"}# 访问值name = person["name"]age = person.get("age", 0)  # 安全访问，如果不存在返回默认值# 添加/修改person["email"] = "alice@example.com"
6. 条件语句
x = 10if x > 10:    print("大于10")elif x == 10:    print("等于10")else:    print("小于10")
7. 循环
# for 循环for i in range(5):    print(i)  # 0, 1, 2, 3, 4# 遍历列表fruits = ["apple", "banana", "orange"]for fruit in fruits:    print(fruit)# while 循环count = 0while count < 5:    print(count)    count += 1
8. 函数
# 定义函数def greet(name):    return f"Hello, {name}!"# 调用函数message = greet("Python")# 带默认参数def power(x, n=2):    return x ** nresult = power(5)      # 25 (默认 n=2)result = power(5, 3)   # 125
9. 类和对象
# 定义类class Person:    def __init__(self, name, age):        self.name = name        self.age = age        def introduce(self):        return f"我是{self.name}，{self.age}岁"# 创建对象person = Person("Alice", 30)print(person.introduce())
10. 文件操作
# 读取文件with open("file.txt", "r", encoding="utf-8") as f:    content = f.read()# 写入文件with open("file.txt", "w", encoding="utf-8") as f:    f.write("Hello, Python!")
11. 异常处理
try:    result = 10 / 0except ZeroDivisionError:    print("不能除以零")except Exception as e:    print(f"发生错误: {e}")finally:    print("执行完成")
12. 列表推导式
# 简洁的列表创建方式squares = [x**2 for x in range(10)]  # [0, 1, 4, 9, 16, ...]evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
13. 常用内置函数
# 类型转换int("123")      # 123str(123)        # "123"float("3.14")   # 3.14# 常用函数len([1, 2, 3])           # 3max(1, 2, 3)             # 3min(1, 2, 3)             # 1sum([1, 2, 3])           # 6sorted([3, 1, 2])        # [1, 2, 3]
14. 模块导入
# 导入整个模块import mathresult = math.sqrt(16)  # 4.0# 导入特定函数from math import sqrt, piresult = sqrt(16)# 导入并重命名import numpy as np
要点总结
缩进：Python 用缩进表示代码块（通常 4 个空格）
注释：使用 # 进行单行注释，""" 或 ''' 进行多行注释
命名：变量名使用小写字母和下划线（snake_case）
动态类型：变量类型在运行时确定
可读性：代码应清晰易读
你的 101.py 文件展示了基本的变量和打印操作。需要我针对某个主题展开吗？
101.py
 解释一下这个文件中包含的python的基础知识

这个文件展示了以下 Python 基础知识：
代码分析
x = 1y = 2print(1+2)
1. 变量赋值（第1-2行）
x = 1y = 2
变量：x 和 y 是变量名
赋值：使用 = 将值赋给变量
动态类型：无需声明类型，Python 自动识别为整数（int）
命名规则：使用小写字母，可包含数字和下划线
2. 数据类型：整数（int）
1 和 2 是整数
Python 中整数可以是任意大小
3. print() 函数（第3行）
print(1+2)
内置函数：print() 用于输出
表达式计算：1+2 先计算为 3，再打印
输出：在控制台显示结果
4. 算术运算
+ 是加法运算符
表达式在打印前先计算
5. 代码执行顺序
从上到下执行
先定义变量，再执行打印
改进建议
当前代码定义了 x 和 y 但未使用。可以改为：
x = 1y = 2print(x + y)  # 使用变量而不是直接写数字
或者更简洁：
x = 1y = 2result = x + y  # 将结果保存到变量print(result)   # 打印结果
涉及的基础概念总结
变量：存储数据的容器
赋值：= 运算符
数据类型：整数（int）
函数调用：print()
算术运算：+ 运算符
表达式求值：先计算再输出
这是一个典型的入门示例，展示了变量定义和输出。
总结下今天两个文件的python基础知识什么，写在
README.md
 

读取这两个文件，总结其中的 Python 基础知识，并写入 README.md。
总结这两个文件中的 Python 基础知识，写入 README.md。
README.md
+139
-1
# Python 基础知识总结本文档总结了 `101.py` 和 `gina.py` 两个文件中涉及的 Python 基础知识。## 文件一：101.py
已总结两个文件中的 Python 基础知识，并写入 README.md。
总结内容概览：
101.py 包含的基础知识：
变量赋值
整数数据类型
print() 函数
算术运算
代码执行顺序
gina.py 包含的基础知识：
模块导入（import）
函数定义（def）和默认参数
字符串操作
字典（dict）的创建和使用
HTTP 请求（requests 库）
条件语句（if-else）
异常处理（raise Exception）
列表（list）和嵌套数据结构
字典和列表的访问方法
f-string 字符串格式化
README.md 中还包含：
知识点对比表格
学习路径建议
代码示例说明
可以打开 README.md 查看完整总结。