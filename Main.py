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
        # 修复原代码截断问题，假设func是一个可调用对象
        if not callable(func):
            raise TypeError("func must be callable")
        self.func = func

# 主程序部分

# 初始化全局字典，避免 run 函数中引用未定义全局变量报错
numdict = {}
strdict = {}
listdict = {}
mapdict = {}
strdict["lang"] = definedCPT(StrChapter, "lang", "StuchkutV1")

def run(cmd: str):
    global numdict, strdict, listdict, mapdict
    """运行单行代码"""
    pass # 占位符，实际逻辑待实现
   
def runlines(code: str):
    """运行整个程序"""
    checkcode(code)
    # 这里应该添加实际执行逻辑，目前仅检查
    
def checkcode(code: str):
    """检查语法错误"""
    result = 0
    info = ["line 0", "No error on syntax"]
    # 进行逐行读取检查语法
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