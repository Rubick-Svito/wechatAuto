import pyautogui
import time
import pyperclip
import myapi

def mouseClick(lOrR,img):
  while True:
    location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
    if location is not None:
        pyautogui.click(location.x,location.y,clicks=1,interval=0.2,duration=0.2,button=lOrR)
        break
    print("未找到匹配图片,0.5秒后重试")
    time.sleep(0.5)

def doSomething(funcName, args):
  # 取和
  if funcName == 'sum':
    try:
      arr = list(map(int,args))
    except ValueError:
      return '无法读取sum函数参数'
    else:
      return sum(arr)
  # 历史上的今天
  elif funcName == '历史上的今天':
    return myapi.api(funcName, args)
  # 天气
  elif funcName == '天气':
    if(len(args) == 0):
      return '未输入城市'
    return myapi.api(funcName, args)
  # 没有方法就自动回复
  else:
    return myapi.api(funcName, args)

def mainwork():
  # 初始位置
  origin = "origin.png"
  mouseClick("left",origin)
  # 点击新消息
  red = "red.png"
  mouseClick("left",red)
  # 复制新消息
  cut = "cut.png"
  msgLocation = pyautogui.locateCenterOnScreen(cut,confidence=0.9)
  if(msgLocation is not None):
    pyautogui.doubleClick(msgLocation.x + 10,msgLocation.y - 50,button='left')
    pyautogui.hotkey('ctrl','c')
    pyautogui.click()
  msg = pyperclip.paste()
  # 处理消息
  todo = msg.split(' ')
  res = doSomething(todo[0],todo[1:])
  pyperclip.copy(res)
  # 粘贴结果
  textLocation = pyautogui.locateCenterOnScreen(cut,confidence=0.9)
  if(textLocation is not None):
    pyautogui.click(textLocation.x,textLocation.y + 80,clicks=1,interval=0.2,duration=0.2,button='left')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl','v')
  # 点击发送
  send = 'send.png'
  mouseClick("left",send)
  # 返回原点
  mouseClick("left",origin)
    
if __name__ == '__main__':
  while True:
    mainwork()
    time.sleep(0.1)
    print("等待0.1秒")   