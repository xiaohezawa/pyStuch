"""
Stuchkut language
By XiaohezAWA
"""

__version__ = "0.2.0"
__author__ = "XiaohezAWA"

import sys
import os
import traceback


# Define exceptions
def abnrm_exit():
    sys.exit(-1)

def expect_type(ch, ctype):
    """
    ctype: "int" / "str" / "list" / "map"
    """

    py_map = {
        "int": int,
        "str": str,
        "list": list,
        "map": dict,
    }

    # Chapter
    if isinstance(ch, Chapter):
        if ch.gettype() != ctype:
            ChapterError(
                f"Expected Chapter.{ctype}, got Chapter.{ch.gettype()}",
                "typed_task"
            ).throw()
        return

    # Raw value
    if not isinstance(ch, py_map[ctype]):
        ChapterError(
            f"Expected {ctype}, got {type(ch).__name__}",
            "typed_task"
        ).throw()


class StuchException:
    def __init__(self, info: str, loc: str):
        self.info = info
        self.loc = loc
        self.name = self.__class__.__name__

    def getinfo(self):
        return self.info

    def throw(self):
        print(f'Exception at "{self.name}", loc {str(self.loc)} :\n{self.info}\n (excepted at line{current_line})')
        print("The program terminated abnormally.")
        abnrm_exit()


class CodeError(StuchException):
    def __init__(self, info: str, loc: str):
        super().__init__(info, loc)


class ChapterError(StuchException):
    def __init__(self, info: str, loc: str):
        super().__init__(info, loc)

class StampError(StuchException):
    def __init__(self, info: str, loc: str):
        super().__init__(info, loc)

class InpyStuchError(StuchException):
    def __init__(self, info: str, loc: str):
        super().__init__(info, loc)

    def throw(self):
        print("在Stuch的Python解释器中出错。")
        print("一般这不是你的程序问题，而是解释器内部异常。")
        print("若有渠道，请提交以下信息：")
        try:
            print(traceback.format_exc())
            super().throw()
        except Exception:
            super().throw()


# Chapters
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
        if issubclass(type(value), Chapter):
            value = value.value()
        if not isinstance(value, str):
            return (-1, 'A "str" type Chapter cannot have values of other types')
        self.value = value
        return (0, "Success")


class IntChapter(Chapter):
    def __init__(self, name):
        super().__init__(name, "int")
        self.value = 0

    def define(self, value: int):
        if issubclass(type(value), Chapter):
            value = value.value()
        if not isinstance(value, int):
            return (-1, 'A "int" type Chapter cannot have values of other types')
        self.value = value
        return (0, "Success")


class ListChapter(Chapter):
    def __init__(self, name):
        super().__init__(name, "list")
        self.value = []

    def define(self, value: list):
        if issubclass(type(value), Chapter):
            value = value.value()
        if not isinstance(value, list):
            return (-1, 'A "list" type Chapter cannot have values of other types')
        self.value = value
        return (0, "Success")


class MapChapter(Chapter):
    def __init__(self, name):
        super().__init__(name, "map")
        self.value = {}

    def define(self, value: dict):
        if issubclass(type(value), Chapter):
            value = value.value()
        if not isinstance(value, dict):
            return (-1, 'A "map" type Chapter cannot have values of other types')
        self.value = value
        return (0, "Success")


def definedCPT(cclass: type, name: str, value):
    """返回定义后的 Chapter 对象（不加入索引）"""
    if issubclass(cclass, Chapter):
        if cclass == Chapter:
            ChapterError(
                "The parameter cclass cannot be the Chapter class itself",
                "definedCPT"
            ).throw()
        cpt = cclass(name)
        res = cpt.define(value)
        if res[0] == -1:
            ChapterError(res[1], "definedCPT_inPy").throw()
        return cpt
    else:
        ChapterError(
            "Invalid class type for Chapter definition",
            "definedCPT"
        ).throw()


def define_newCPT(cclass: type, name: str, value, return_value=False):
    """标准方式定义新 Chapter"""
    if issubclass(cclass, Chapter):
        if cclass == Chapter:
            ChapterError(
                "The parameter cclass cannot be the Chapter class itself",
                "definedCPT"
            ).throw()
        cpt = cclass(name)
        res = cpt.define(value)
        if res[0] == -1:
            ChapterError(res[1], "definedCPT_inPy").throw()
        chapters[cpt.gettype()][name] = cpt
        chapters_index[name] = cpt.gettype()
        return cpt if return_value else 0
    else:
        ChapterError(
            "Invalid class type for Chapter definition",
            "defineCPT"
        ).throw()


def getCPT(name: str):
    """通过名称获取 Chapter"""
    if name in chapters_index:
        return chapters[chapters_index[name]][name]
    ChapterError(f'Chapter "{name}" does not exist', "getCPT").throw()


def check_vars():
    """清理重复变量名"""
    valid_vars = []
    for var in chapters_index.keys():
        if var in valid_vars:
            for ctype in chapters.keys():
                if ctype == chapters_index[var]:
                    pass
                elif var in chapters[ctype]:
                    del chapters[ctype][var]


# 字面量解析
def mg_str(value: str):
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def mg_int(value: str):
    try:
        return int(value)
    except ValueError:
        ChapterError("Invalid integer format", "mg_int").throw()


def mg_list(value: str):
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
        if value == "":
            return []
        parts = value.split(",")
        return [mg_str(p.strip()) for p in parts]
    ChapterError("Invalid list format", "mg_list").throw()


def mg_map(value: str):
    if value.startswith("{") and value.endswith("}"):
        value = value[1:-1]
        if value == "":
            return {}
        out = {}
        for pair in value.split(","):
            if ":" in pair:
                k, v = pair.split(":", 1)
                out[mg_str(k.strip())] = mg_str(v.strip())
            else:
                ChapterError("Invalid map format", "mg_map").throw()
        return out
    ChapterError("Invalid map format", "mg_map").throw()


mgs = {
    "str": mg_str,
    "int": mg_int,
    "list": mg_list,
    "map": mg_map,
}


# Task
class Task:
    def __init__(self, func: callable):
        if not callable(func):
            InpyStuchError(
                "The parameter func is not a callable object",
                "definedTask"
            ).throw()
        self.func = func
        self.args = []

    def add(self, arg):
        self.args.append(arg)

    def run(self):
        resolved = []
        for arg in self.args:
            if isinstance(arg, str) and arg in chapters_index:
                resolved.append(getCPT(arg))
            else:
                resolved.append(arg)
        self.func(resolved)


# Built-in tasks
def intro(args):
    if isinstance(args[0], Chapter):
        print(args[0].value)
    else:
        ChapterError("Invalid Chapter object", "intro").throw()

def cset(args):
    global current_chapter
    if len(args) != 1:
        ChapterError("set requires exactly 1 argument", "set").throw()
    val = args[0]
    if isinstance(val, Chapter):
        val = val.value
    ctype = current_chapter.gettype()
    if ctype == "int" and not isinstance(val, int):
        ChapterError("set expects int value", "set").throw()
    if ctype == "str" and not isinstance(val, str):
        ChapterError("set expects str value", "set").throw()
    if ctype == "list" and not isinstance(val, list):
        ChapterError("set expects list value", "set").throw()
    if ctype == "map" and not isinstance(val, dict):
        ChapterError("set expects map value", "set").throw()
    current_chapter.define(val)

def add(args):
    a, b = args
    expect_type(a, "int")
    expect_type(b, "int")
    a = int(a.value) if type(a) == IntChapter else a
    b = int(b.value) if type(b) == IntChapter else b
    current_chapter.define(a + b)

def drop(args):
    a, b = args
    expect_type(a, "int")
    expect_type(b, "int")
    a = int(a.value) if type(a) == IntChapter else a
    b = int(b.value) if type(b) == IntChapter else b
    current_chapter.define(a - b)

def mtpy(args):
    a, b = args
    expect_type(a, "int")
    expect_type(b, "int")
    a = int(a.value) if type(a) == IntChapter else a
    b = int(b.value) if type(b) == IntChapter else b
    current_chapter.define(a * b)

def dvsn(args):
    a, b = args
    expect_type(a, "int")
    expect_type(b, "int")
    a = int(a.value) if type(a) == IntChapter else a
    b = int(b.value) if type(b) == IntChapter else b
    if b.value == 0:
        ChapterError("Division by zero", "dvsn").throw()
    current_chapter.define(a // b)

def apnd(args):
    lst, val = args
    expect_type(lst, "list")
    lst.value.append(val.value)

def dlnd(args):
    lst = args[0]
    expect_type(lst, "list")
    if lst.value:
        lst.value.pop()

def istl(args):
    lst, idx, val = args
    expect_type(lst, "list")
    expect_type(idx, "int")
    lst.value.insert(idx.value, val.value)

def get(args):
    container, key = args
    if container.gettype() == "list":
        expect_type(key, "int")
        current_chapter.define(container.value[key.value])
    elif container.gettype() == "map":
        expect_type(key, "str")
        current_chapter.define(container.value[key.value])
    else:
        ChapterError("get only supports list or map", "get").throw()

def setmap(args):
    mp, key, val = args
    expect_type(mp, "map")
    expect_type(key, "str")
    mp.value[key.value] = val.value

def dlmp(args):
    container, key = args
    if container.gettype() == "list":
        expect_type(key, "int")
        del container.value[key.value]
    elif container.gettype() == "map":
        expect_type(key, "str")
        del container.value[key.value]

def bigr(args):
    a, b = args
    expect_type(a, "int")
    expect_type(b, "int")
    current_chapter.define(int(a.value > b.value))

def smlr(args):
    a, b = args
    expect_type(a, "int")
    expect_type(b, "int")
    current_chapter.define(int(a.value < b.value))

def eqal(args):
    a, b = args
    expect_type(a, "int")
    expect_type(b, "int")
    current_chapter.define(int(a.value == b.value))


# Symbols
def sym_create(args):
    global tasks, chapters

    if len(args) != 2:
        CodeError(
            f"Invalid number of arguments: {' '.join(args)}",
            "Symbol.create"
        ).throw()

    full_type, name = args[0], args[1]

    # Task.xxx
    if full_type.startswith("Task."):
        task_name = full_type.split(".", 1)[1]
        tasks[name] = Task(tasks_func.get(task_name, intro))
        return

    # Chapter.int / Chapter.str ...
    if full_type.startswith("Chapter."):
        parts = full_type.split(".", 2)
        if len(parts) != 2:
            ChapterError(
                f"Invalid Chapter type: {full_type}",
                "Symbol.create"
            ).throw()

        ctype = parts[1]
        if ctype not in chapters_func:
            ChapterError(
                f"Unknown Chapter type: {ctype}",
                "Symbol.create"
            ).throw()

        chapters[ctype][name] = chapters_func[ctype](name)
        chapters_index[name] = ctype
        return

    CodeError(
        f"Invalid object type: {full_type}",
        "Symbol.create"
    ).throw()


def sym_run(args):
    task_name = args[0]
    if task_name in tasks:
        tasks[task_name].run()
    else:
        ChapterError(f'Task "{task_name}" does not exist', "Symbol.run").throw()


def sym_ready(args):
    task_name = args[0]
    if task_name in tasks:
        tasks[task_name].add(current_chapter)
    else:
        ChapterError(f'Task "{task_name}" does not exist', "Symbol.ready").throw()


def sym_switch(args):
    global current_chapter
    chapter_name = args[0]
    if chapter_name in chapters_index:
        current_chapter = getCPT(chapter_name)
    else:
        ChapterError(f'Chapter "{chapter_name}" does not exist', "Symbol.switch").throw()


def sym_go(args):
    task_name = args[0]
    const_type = args[1]
    raw_value = args[2]

    if task_name not in tasks:
        ChapterError(f'Task "{task_name}" does not exist', "Symbol.go").throw()
        
    if raw_value in chapters_index:
        tasks[task_name].add(getCPT(raw_value))
        return
        
    if const_type not in mgs:
        CodeError("Invalid constant type", "Symbol.go").throw()

    tasks[task_name].add(mgs[const_type](raw_value))


def sym_startstamp(args):
    global recording
    name = args[0]
    recording = name
    stamps[name] = []

def sym_onlystamp(args):
    global recording
    recording = args[0]
    stamps.setdefault(recording, [])

def sym_endstamp(args):
    global recording
    recording = None

def sym_backstamp(args):
    name = args[0]
    if name not in stamps:
        StampError(f"Stamp '{name}' does not exist", "backstamp").throw()

    lines = stamps[name]
    pc = 0
    while pc < len(lines):
        run(lines[pc])
        pc += 1

def sym_ifstamp(args):
    cond_task, stamp_name = args
    tasks[cond_task].run()
    result = current_chapter.value
    if result == 1:
        sym_backstamp([stamp_name])

# Runtime tables
chapters = {
    "int": {},
    "str": {},
    "list": {},
    "map": {},
}

chapters_index = {}

cpt_types = {
    "str": str,
    "int": int,
    "list": list,
    "map": dict,
}

tasks = {}

tasks_func = {
    "intro": intro,
    "set": cset,
}
#0.3.0 update
tasks_func.update({
    "add": add,
    "drop": drop,
    "mtpy": mtpy,
    "dvsn": dvsn,
    "apnd": apnd,
    "dlnd": dlnd,
    "istl": istl,
    "get": get,
    "setm": setmap,
    "dlmp": dlmp,
    "bigr": bigr,
    "smlr": smlr,
    "eqal": eqal,
})



chapters_func = {
    "str": StrChapter,
    "int": IntChapter,
    "list": ListChapter,
    "map": MapChapter,
}

syms = {
    "create": sym_create,
    "run": sym_run,
    "ready": sym_ready,
    "switch": sym_switch,
    "go": sym_go,
}
#0.3.0 update
syms.update({
    "startstamp": sym_startstamp,
    "onlystamp": sym_onlystamp,
    "backstamp": sym_backstamp,
    "onlystamp": sym_onlystamp,
    "endstamp": sym_endstamp,
    "ifstamp": sym_ifstamp,
})

stamps = {}  # name -> list[str]
recording = None
stamp_pc = {}  # stamp_name -> index

define_newCPT(StrChapter, "lang", "StuchkutV0.2.0")
current_chapter = getCPT("lang")


def run(cmd: str):
    cmd = cmd.strip()
    if not cmd:
        return

    comment_pos = cmd.find("^")
    if comment_pos != -1:
        cmd = cmd[:comment_pos].strip()
    if not cmd:
        return

    if recording is not None:
        stamps[recording].append(cmd)
        return

    cmd = cmd.split()
    code = cmd[0]

    if code in syms:
        syms[code](cmd[1:])
    else:
        CodeError(f"Invalid symbol: {' '.join(cmd)}", "running").throw()


def runlines(code: str):
    global current_line
    
    checkcode(code)
    for line in code.split("\n"):
        current_line += 1
        line = line.strip()
        if line:
            run(line)

def checkcode(code: str):
    for ch in code:
        # 禁止 ASCII 控制字符
        if ord(ch) < 32 and ch not in "\n\t":
            CodeError(f"Invalid control character: {repr(ch)}", "checkcode").throw()



if __name__ == "__main__":
    current_line = 0
    if len(sys.argv) < 2:
        print("用法：\n    stuchkut <filepath>")
    else:
        path = sys.argv[1]
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                runlines(f.read())
        else:
            print(f"Error: File '{path}' not found.")
