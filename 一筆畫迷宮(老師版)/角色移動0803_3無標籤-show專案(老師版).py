import tkinter

key = ""
def key_down(e):
    global key
    key = e.keysym
def key_up(e):
    global key
    key = ""

cx = 400   #管理角色X座標的變數
cy = 300   #管理角色Y座標的變數
def main_proc():
    global cx, cy   #將CX、CY宣告為全域變數
    if key == "Up":     #任務一：按下方向鍵「上」的話，Y座標減少20點
        cy = cy - 20
    if key == "Down":   #任務一：按下方向鍵「下」的話，Y座標增加20點
        cy = cy + 20
    if key == "Left":   #任務一：按下方向鍵「左」的話，X座標減少20點
        cx = cx - 20
    if key == "Right":  #任務一：按下方向鍵「右」的話，X座標增加20點
        cx = cx + 20
    canvas.coords("MYCHR", cx, cy)
    root.after(100, main_proc)

root = tkinter.Tk()
root.title("移動角色")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=800, height=600, bg="lightgreen")
canvas.pack()
img = tkinter.PhotoImage(file="mimi.png")
canvas.create_image(cx, cy, image=img, tag="MYCHR")
main_proc()
root.mainloop()
