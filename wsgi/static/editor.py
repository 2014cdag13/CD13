import sys
import time
import dis
import traceback

from browser import doc
from javascript import JSObject

# set height of container to 66% of screen
_height = doc.documentElement.clientHeight
_s = doc['container']
_s.style.height = '%spx' % int(_height*0.66)

has_ace = True
try:
    editor=JSObject(ace).edit("editor")
    editor.getSession().setMode("ace/mode/python")
    editor.setTheme("ace/theme/monokai")
except:
    from browser import html
    editor = html.TEXTAREA(rows=20,cols=70)
    doc["editor"] <= editor
    def get_value(): return editor.value
    def set_value(x):editor.value=x
    editor.getValue = get_value
    editor.setValue = set_value
    has_ace = False

if sys.has_local_storage:
    from browser.local_storage import storage
else:
    storage = False

def reset_src():
    if storage and "py_src" in storage:
       editor.setValue(storage["py_src"])
    else:
       editor.setValue('''#coding: utf-8
# 猜數字遊戲
import random
 
標準答案 = random.randint(1, 100)
你猜的數字 = int(input("請輸入您所猜的整數:"))
猜測次數 = 1
while 標準答案 != 你猜的數字:
    if 標準答案 < 你猜的數字:
        print("太大了，再猜一次 :)加油")
    else:
        print("太小了，再猜一次 :)加油")
    你猜的數字 = int(input("請輸入您所猜的整數:"))
    猜測次數 += 1
 
print("猜對了！總共猜了", 猜測次數, "次")
''')

    editor.scrollToRow(0)
    editor.gotoLine(0)

def reset_src_area():
    if storage and "py_src" in storage:
       editor.value = storage["py_src"]
    else:
        editor.value = '''#coding: utf-8
# 猜數字遊戲
import random
 
標準答案 = random.randint(1, 100)
你猜的數字 = int(input("請輸入您所猜的整數:"))
猜測次數 = 1
while 標準答案 != 你猜的數字:
    if 標準答案 < 你猜的數字:
        print("太大了，再猜一次 :)加油")
    else:
        print("太小了，再猜一次 :)加油")
    你猜的數字 = int(input("請輸入您所猜的整數:"))
    猜測次數 += 1
 
print("猜對了！總共猜了", 猜測次數, "次")
'''

def write(data):
    doc["console"].value += str(data)

#sys.stdout = object()    #not needed when importing sys via src/Lib/sys.py
sys.stdout.write = write

#sys.stderr = object()    # ditto
sys.stderr.write = write

def to_str(xx):
    return str(xx)

#info = sys.implementation.version
#doc['version'].text = '%s.%s.%s' %(info.major,info.minor,info.micro)

output = ''

def show_console(ev):
    doc["console"].value = output
    doc["console"].cols = 60

def clear_text(ev):
    editor.setValue('')
    if sys.has_local_storage:
        storage["py_src"]=''

    doc["console"].value=''

def clear_src(ev):
    editor.setValue('')
    if sys.has_local_storage:
        storage["py_src"]=''
        
def clear_canvas(ev):
    canvas = doc["plotarea"]
    ctx = canvas.getContext("2d")
    # Store the current transformation matrix
    ctx.save();
    # Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    # Restore the transform
    ctx.restore();
    #ctx.clearRect(0, 0, canvas.width, canvas.height)

def clear_console(ev):
    doc["console"].value=''

def run(*args):
    global output
    doc["console"].value=''
    src = editor.getValue()
    if storage:
       storage["py_src"]=src

    t0 = time.perf_counter()
    try:
        exec(src,globals())
        state = 1
    except Exception as exc:
        traceback.print_exc()
        state = 0
    output = doc["console"].value

    print('<completed in %6.2f ms>' % ((time.perf_counter()-t0)*1000.0))
    return state

# load a Python script
def load(evt):
    _name=evt.target.value+'?foo=%s' %time.time()
    editor.setValue(open(_name).read())

def show_js(ev):
    src = editor.getValue()
    doc["console"].value = dis.dis(src)

def change_theme(evt):
    _theme=evt.target.value
    editor.setTheme(_theme)

    if storage:
       storage["ace_theme"]=_theme
doc["ace_theme"].bind("change",change_theme)

def reset_theme():
    if storage:
       if "ace_theme" in storage:
          editor.setTheme(storage["ace_theme"])
          doc["ace_theme"].value=storage["ace_theme"]

def reset_the_src(ev):
    if has_ace:
        reset_src()
        reset_theme()
    else:
        reset_src_area()

if has_ace:
    reset_src()
    reset_theme()
else:
    reset_src_area()
