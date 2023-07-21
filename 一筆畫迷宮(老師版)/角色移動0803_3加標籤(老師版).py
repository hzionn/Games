import tkinter

key = ""          #宣告存放鍵值的變數
def key_down(e):  #定義於按下按鍵之際執行的函數
    global key      #將Key宣告為全域變數
    key = e.keysym  #將按鍵名稱帶入key
def key_up(e):    #定義於放開按鍵之際執行的函數
    global key      #將key宣告為全域變數
    key = ""        #將空白字串帶入key

cx = 400   #管理角色X座標的變數
cy = 300   #管理角色Y座標的變數
def main_proc():
    global cx, cy   #將CX、CY宣告為全域變數
    if key == "Up":    #任務一：按下方向鍵「上」的話，Y座標減少20點
        cy = cy - 20
    if key == "Down":  #任務一：按下方向鍵「下」的話，Y座標增加20點
        cy = cy + 20
    if key == "Left":  #任務一：按下方向鍵「左」的話，X座標減少20點
        cx = cx - 20
    if key == "Right": #任務一：按下方向鍵「右」的話，X座標增加20點
        cx = cx + 20
    canvas.coords("MYCHR", cx, cy)   #將圖片移至新位置
    show_label["text"] = ("X=", cx,"Y=", cy)    #任務二：加入標籤 顯示 X Y 座標
    root.after(100, main_proc)       #利用after()命令指定0.1秒之後執行的函數

root = tkinter.Tk()    #建立視窗物件
root.title("移動角色")  #指定標題
root.bind("<KeyPress>", key_down)  #利用bind()命令指定於按下按鍵時執行之函數
root.bind("<KeyRelease>", key_up)  #利用bind()命令指定於按開按鍵時執行之函數
show_label = tkinter.Label(font=("微軟正黑體",20), bg="lightgreen",fg="red") #任務二：設定字體大小顏色、背景
show_label.pack()  #任務二：配置標籤
canvas = tkinter.Canvas(width=800, height=600, bg="lightgreen")  #建立畫布零件
canvas.pack()   #配置畫布
img = tkinter.PhotoImage(file="mimi.png")   #將角色圖片載入變數img
canvas.create_image(cx, cy, image=img, tag="MYCHR")   #於畫布顯示圖片
main_proc()     #執行main_proc函數
root["bg"] = "lightgreen"   #顯示背景
root.mainloop() #顯示視窗
