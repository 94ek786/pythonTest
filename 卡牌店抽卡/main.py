import pyautogui
import time
import winsound

def clickkey(key:str,clicktime:int):
    start_time = time.perf_counter()
    target_time = start_time + clicktime
    t_time = start_time
    while(t_time < target_time):
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)
        t_time = t_time + 0.25
        while time.perf_counter() < t_time:
            pass
        t = time.perf_counter()
        #print(time.perf_counter()-t)
        #print(t_time)
        #print(target_time)




def countdown():
    print("5")
    time.sleep(1)
    print("4")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)

print("卡牌店自動抽卡小程式")
print("請先將遊戲的開卡包速度開至最快")
print("並將遊戲的案件設定互動改為V鍵拿走物品改為B鍵")
print("輸入數字前將遊戲中欲抽卡之箱子準備好並將準心對好")
print("再輸入數字後經過五秒將開始執行抽卡")
print("輸入1為小箱32包，輸入2為大箱64包，輸入其他東西則會關閉程式")
q = 0
loop = 0
while(q == 0):
    i = input("請輸入數字：")
    if(i == "1"):
        loop = 4
        countdown()
    elif(i == "2"):
        loop = 8
        countdown()
    elif(i == "0"):
        loop = 2
        countdown()
    else:
        q = 1
    while(loop>0):
        clickkey("b",2)
        #pyautogui.click(clicks=1, interval=0.5, button='left')
        pyautogui.keyDown('r')
        pyautogui.keyUp('r')
        clickkey("v",37)
        loop = loop - 1
    winsound.Beep(500,300)
    time.sleep(0.1)
    winsound.Beep(440,300)