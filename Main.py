"""
Stuchkut language
By XiaohezAWA
Last updated: the 3rd week of Feb. 2026

5/19 更新：
完成准备执行初始部分编写，内核还没搞
能想出来让Python间接把我的脚本三次翻译得到机器码的我也是神了😋

5/20 更新：
Exception类和Chapter类框架编写完毕
"""

__version__ = "0.1.0"
__author__ = "XiaohezAWA"

import sys
import os
import os.path
import traceback

# Define exceptions
def abnrm_exit():
    sys.exit(-1)

class StuchException:
    def __init__(self, info: str, loc: str):
        self.info = info
        self.loc = loc
        self.name = self.__class__.__name__
    
    def getinfo(self):
        return self.info
    
    def throw(self):
        print(f"Exception at \"{self.name}\",loc {str(self.loc)}: \n" + 
              f"{self.info}")
        print("The program terminated abnormally.")
        abnrm_exit()
        
class CodeError(StuchException):
    def __init__(self, info: str, loc: str):
        super().__init__(info, loc)

class ChapterError(StuchException):
    def __init__(self, info: str, loc: str):
        super().__init__(info, loc)

class InpyStuchError(StuchException):
    def __init__(self, info: Exception, loc: str):
        super().__init__(info, loc)
    def throw(self):
        print("在Stuch的Python解释器中出现错误。\n" + 
            "一般这不是你的程序问题，而是在Python解释器中出现了异常或是某处编写不当")
        print("若有渠道，请提交此段文字至反馈：")
        try:
            print(traceback.format_exc())
            super().throw()
        except:
            super().throw()

# Chapters class
class Chapter:
    def __init__(self, name, ctype):
        self.name = name
        self.ctype = ctype
    
    def getname(self):
        return self.name
    
    def gettype(self):
        return self.ctype

class StrChapter(Chapter):
    def __init__(self, name):
        super().__init__(name, "str")
        self.value = ""
    
    def define(self, value: str):
        if type(value) != str:
            return (-1, "A \"str\" type Chapter cannot have values of other types")
        self.value = value
        return(0, "Success")

class IntChapter(Chapter):
    def __init__(self, name):
        super().__init__(name, "int")
        self.value = "" # 注意：这里初始化通常应为 0 或 None，但保持原意暂不修改逻辑
    
    def define(self, value: int): # 修正类型提示
        if type(value) != int:
            return (-1, "A \"int\" type Chapter cannot have values of other types")
        self.value = value
        return(0, "Success")

class ListChapter(Chapter):
    def __init__(self, name):
        super().__init__(name, "list")
        self.value = [] # 修正初始值
    
    def define(self, value: list):
        if type(value) != list:
            return (-1, "A \"list\" type Chapter cannot have values of other types")
        self.value = value
        return(0, "Success")

class MapChapter(Chapter):
    def __init__(self, name):
        super().__init__(name, "map")
        self.value = {} # 修正初始值
    
    def define(self, value: dict):
        if type(value) != dict:
            return (-1, "A \"map\" type Chapter cannot have values of other types")
        self.value = value
        return(0, "Success")

def definedCPT(cclass: type, name: str, value):
    if issubclass(cclass, Chapter):
        if cclass == Chapter:
            ChapterError("The parameter cclass cannot be the Chapter class itself", "definedCPT").throw()
        else:
            cpt = cclass(name)
            res = cpt.define(value)
            if res[0] == -1:
                ChapterError(res[1], "definedCPT_inPy").throw()
            else:
                return cpt
    else:
        ChapterError("Invalid class type for Chapter definition", "definedCPT").throw()

# Tasks class
class Task:
    def __init__(self, func: callable):
        if not callable(func):
            InpyStuchError(f"The parameter func is not a callable object", "definedTask").throw()
        self.func = func
        self.args = []
    
    def add(self, arg):
        self.args.append(arg)
    
    def run(self):
        self.func(self.args) # 内部函数必须接受一个列表形参

# MAIN

# Task types
def intro(args: list[Chapter]): # for test
    """打印"""
    """
    args[0]: Chapter object
    """
    if isinstance(args[0], Chapter) and type(args[0]) != Chapter: # 必须是Chapter的子类对象
        print(args[0].getvalue())
    else:
        ChapterError("Invalid Chapter object", "intro").throw()

# symbols

def create(args: list[str]):# for test
    """创建Task/Chapter"""
    """
    args[0]: "create"
    args[1]: "Task.xxx" or "Chapter.xxx"
    args[2]: "xxx/XXX"
    """

    tasks_func = {
        "intro": intro
    }

    chapters_func = {
        "str": StrChapter,
        "int": IntChapter,
        "list": ListChapter,
        "map": MapChapter
    }

    if not len(args) == 3:
        output = ""
        for i in args:
            output += i + " "
        CodeError(f"Invalid number of arguments:{output}", "Symbol.create").throw()
    else:
        types = args[1].split(".")
        if types[0] not in ["Task", "Chapter"]:
            CodeError("Invalid type of object", "Symbol.create").throw()
        else:
            if types[0] == "Task":
                tasks[args[2]] = Task(func = tasks_func[types[1]] if types[1] in tasks_func else intro)
            elif types[0] == "Chapter":
                chapters[types[1]][types[2]] = chapters_func[types[1]](name = types[2])
        

# 初始化全局字典，避免 run 函数中引用未定义全局变量报错
chapters = {
    "int": {},
    "str": {},
    "list": {},
    "map": {}
}
chapters["str"]["lang"] = definedCPT(StrChapter, "lang", "StuchkutV1")

def run(cmd: str):
    global numdict, strdict, listdict, mapdict
    """运行单行代码"""
    cmd = cmd.split(" ")
    syms = [
        "create",
    ]

    args = []
    func = print
    code = cmd[0]
    if code in syms:
        func = tasks[code]
        args = cmd[1:]
        func(args)
    else:
        output = ""
        for i in cmd:
            output += i + " "
            CodeError(f"Invalid symbol: {output}", "running").throw()

def runlines(code: str):
    """运行整个程序"""
    checkcode(code)
    # 执行逻辑
    for code in code.split("\n"):
        run(code)
    
def checkcode(code: str):
    """检查语法错误"""
    result = 0
    info = ["line 0", "No error on syntax"]
    # 进行逐行读取检查语法（目前仅查字符）
    for line in code.split("\n"):
        for char in line:
            if char not in "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789()_.-+=&|/:":
                CodeError(f"Invalid character: {char}", info[0]).throw()
            else:
                pass
    return {"result": result, "info": tuple(info)}

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("""
用法：
    stuchkut <filepath>
                """)
    else:
        # 修复缩进问题，确保所有章节在同一层级
        chapters = {
            "int": {},
            "str": {
                # 修复类名错误 SttChapter -> StrChapter
                "lang": definedCPT(StrChapter, "lang", "StuchkutV1")
            },
            "list": {},
            "map": {}
        }
        
        tasks = {}
        
        filepath = args[1]
        # 修复 path.exists -> os.path.exists
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as file:
                code_data = file.read()
            runlines(code_data)
        else:
            print(f"Error: File '{filepath}' not found.")