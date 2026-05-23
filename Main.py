"""
Stuchkut language
By XiaohezAWA

"""

__version__ = "0.2.0"
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
    def __init__(self, info: str, loc: str):
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
        self.value = 0
    
    def define(self, value: int):
        if type(value) != int:
            return (-1, "A \"int\" type Chapter cannot have values of other types")
        self.value = value
        return(0, "Success")

class ListChapter(Chapter):
    def __init__(self, name):
        super().__init__(name, "list")
        self.value = []
    
    def define(self, value: list):
        if type(value) != list:
            return (-1, "A \"list\" type Chapter cannot have values of other types")
        self.value = value
        return(0, "Success")

class MapChapter(Chapter):
    def __init__(self, name):
        super().__init__(name, "map")
        self.value = {}
    
    def define(self, value: dict):
        if type(value) != dict:
            return (-1, "A \"map\" type Chapter cannot have values of other types")
        self.value = value
        return(0, "Success")

def definedCPT(cclass: type, name: str, value):
    """返回定义后的Chapter对象(不添加索引)"""
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

def define_newCPT(cclass: type, name: str, value, return_value = False):
    """定义新Chapter的标准方法"""
    if issubclass(cclass, Chapter):
        if cclass == Chapter:
            ChapterError("The parameter cclass cannot be the Chapter class itself", "definedCPT").throw()
        else:
            cpt = cclass(name)
            res = cpt.define(value)
            if res[0] == -1:
                ChapterError(res[1], "definedCPT_inPy").throw()
            else:
                chapters[cpt.gettype()][name] = cpt
                chapters_index[name] = cpt.gettype()
            if return_value:
                return cpt
            else:
                return 0
    else:
        ChapterError("Invalid class type for Chapter definition", "defineCPT").throw()

def getCPT(name: str):
    """直接由Chapter名获取Chapter"""
    if name in chapters_index:
        return chapters[chapters_index[name]][name]
    else:
        ChapterError(f"Chapter \"{name}\" does not exist", "getCPT").throw()    

def check_vars():
    """消除重复名称Chapter"""
    vaild_vars = []
    for var in chapters_index.keys():
        if var in vaild_vars:
            for type in chapters.keys():
                if type == chapters_index[var]:
                    pass
                else:
                    if var in chapters[type].keys():
                        del chapters[type][var]

# manage when define
def mg_str(value: str):
    """处理字符串"""
    if value.startswith("\"") and value.endswith("\""):
        return value[1:-1]
    else:
        return value

def mg_int(value: str):
    """处理整数"""
    try:
        value = int(value)
    except:
        ChapterError("Invalid integer format", "mg_int").throw()
        return int(value)

def mg_list(value: str):
    """处理列表"""
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
        if value == "":
            return []
        else:
            value = value.split(",")
            for i in range(len(value)):
                value[i] = mg_str(value[i])
            return value
    else:
        ChapterError("Invalid list format", "mg_list").throw()

def mg_map(value: str):
    """处理字典"""
    if value.startswith("{") and value.endswith("}"):
        value = value[1:-1]
        if value == "":
            return {}
        else:
            value = value.split(",")
            temp_dict = {}
            for i in range(len(value)):
                if ":" in value[i]:
                    key, val = value[i].split(":")
                    temp_dict[mg_str(key)] = mg_str(val)
                else:
                    ChapterError("Invalid map format", "mg_map").throw()
    else:
        ChapterError("Invalid map format", "mg_map").throw()

mgs = {
    "str": mg_str,
    "int": mg_int,
    "list": mg_list,
    "map": mg_map
}

# Tasks class
class Task:
    """Task基础类"""
    def __init__(self, func: callable):
        if not callable(func):
            InpyStuchError(f"The parameter func is not a callable object", "definedTask").throw()
        self.func = func
        self.args = []
    
    def add(self, arg):
        self.args.append(arg)
    
    def run(self):
        resolved_args = []
        for arg in self.args:
            if isinstance(arg, str):
                resolved_args.append(getCPT(arg) if arg in chapters_index else arg)
            else:
                resolved_args.append(arg)
        self.func(resolved_args)

# MAIN

# Task types
def intro(args: list[Chapter]):
    """打印"""
    """
    args[0]: Chapter object
    """
    if isinstance(args[0], Chapter) and type(args[0]) != Chapter:
        print(args[0].value)
    else:
        ChapterError("Invalid Chapter object", "intro").throw()

def cset(args: list):
    """设置current_chapter的值"""
    """
    args[0]: new value
    """
    global current_chapter
    ctype = current_chapter.gettype()
    current_chapter.define(cpt_types[ctype](args[0]))


# symbols

def sym_create(args: list[str]):
    """创建Task/Chapter"""
    """
    args[0]: "create"
    args[1]: "Task.xxx" or "Chapter.xxx"
    args[2]: "xxx/XXX"
    """

    global tasks, chapters
    if len(args) != 2:
        output = ""
        for i in args:
            output += i + " "
        CodeError(f"Invalid number of arguments:{output}", "Symbol.create").throw()
    else:
        types = args[0].split(".")
        if types[0] not in ["Task", "Chapter"]:
            CodeError("Invalid type of object", "Symbol.create").throw()
        else:
            if types[0] == "Task":
                tasks[args[1]] = Task(func = tasks_func[types[1]] if types[1] in tasks_func else intro)
            elif types[0] == "Chapter":
                chapters[types[1]][args[1]] = chapters_func[types[1]](name = args[1])
                chapters_index[args[1]] = types[1]

def sym_run(args: list[Chapter]):
    """运行Task"""
    """
    args[0]: Task Chapter
    """
    task_name = args[0]
    if task_name in tasks:
        tasks[task_name].run()
    else:
        ChapterError(f"Task \"{task_name}\" does not exist", "Symbol.run").throw()


def sym_ready(args: list):
    """将current_chapter放入某Task的形参列表"""
    """
    args[0]: Task name
    """
    task_name = args[0]
    if task_name in tasks:
        tasks[task_name].add(current_chapter)
    else:
        ChapterError(f"Task \"{task_name}\" does not exist", "Symbol.ready").throw()

def sym_switch(args: list[Chapter]):
    """切换current_chapter"""
    """
    args[0]: Chapter name
    """
    global current_chapter
    chapter_name = args[0]
    if chapter_name in chapters_index:
        current_chapter = getCPT(chapter_name)
    else:
        ChapterError(f"Chapter \"{chapter_name}\" does not exist", "Symbol.switch").throw()

def sym_go(args: list):
    """将常量放入某Task的形参列表"""
    """
    args[0]: Task name
    args[1]: constant type
    args[2]: constant
    """
    task_name = args[0]
    if not args[1] in cpt_types:
        CodeError("Invalid constant type", "Symbol.go").throw()
    if task_name in tasks:
        tasks[task_name].add(mgs[args[1]](args[2]))
    else:
        ChapterError(f"Task \"{task_name}\" does not exist", "Symbol.go").throw()



chapters = {
    "int": {},
    "str": {},
    "list": {},
    "map": {}
}
chapters_index = {

}

cpt_types = {
    "str": str,
    "int": int,
    "list": list,
    "map": dict
}

tasks = {}


tasks_func = {
    "intro": intro,
    "set": cset
}

chapters_func = {
    "str": StrChapter,
    "int": IntChapter,
    "list": ListChapter,
    "map": MapChapter
}

syms = {
    "create": sym_create,
    "run": sym_run,
    "ready": sym_ready,
    "switch": sym_switch,
    "go": sym_go,
}

define_newCPT(StrChapter, "lang", "StuchkutV0.2.0")
current_chapter = getCPT("lang")

def run(cmd: str):
    """运行单行代码"""
    cmd = cmd.split(" ")

    args = []
    func = print
    code = cmd[0]
    if code in syms.keys():
        func = syms[code]
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
    for code in code.split("\n"):
        run(code)
    
def checkcode(code: str):
    """检查语法错误"""
    
    result = 0
    line_num = 1
    for line in code.split("\n"):
        for char in line:
            if char not in "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789()_.-+=&|/:\" \n":
                CodeError(f"Invalid character: {char}", f"line {line_num}").throw()
        line_num += 1
    return {"result": result, "info": ("line -1", "No CodeError")}



if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("""
用法：
    stuchkut <filepath>
                """)
    else:
        filepath = args[1]
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as file:
                code_data = file.read()
            runlines(code_data)
        else:
            print(f"Error: File '{filepath}' not found.")