import tkinter
import random

# 縮放倍率
scale = 0.8

index = 0
timer = 0
score = 0
hisc = 1000
difficulty = 0
tsugi = 0

cursor_x = 0
cursor_y = 0
mouse_x = 0
mouse_y = 0
mouse_c = 0

def mouse_move(e):
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y

def mouse_press(e):
    global mouse_c
    mouse_c = 1

neko = []
check = []
for i in range(10):
    neko.append([0, 0, 0, 0, 0, 0, 0, 0])        #append()命令初始化列表
    check.append([0, 0, 0, 0, 0, 0, 0, 0])       

def draw_neko():
    cvs.delete("NEKO")                           #顯示貓咪的函數
    for y in range(10):                          
        for x in range(8):                       
            if neko[y][x] > 0:                   
                cvs.create_image(int((x*72+60)*scale), int((y*72+60)*scale), image=img_neko[neko[y][x]], tag="NEKO")

def check_neko():                   
    for y in range(10):             #迴圈 y 從0遞增至9
        for x in range(8):          #迴圈 x 從0遞增至7
            check[y][x] = neko[y][x]         #將貓咪的值放入判斷專用列表

    for y in range(1, 9):           
        for x in range(8):
            if check[y][x] > 0:                                                    
                if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:  
                    
                
                

    for y in range(10):
        for x in range(   ):
            if check[y][x] > 0:                                                    
                if check         == check[y][x] and check       == check[y][x]: 
                 
                
                

    for y in            :
        for x in           :
            if check[y][x] > 0:                                                      
                if                       and                    :  
                    
                    neko[y][x] = 7
                    
                if                       and                    :  
                  
                    neko[y][x] = 7
                    

def sweep_neko():                   #將剛剛檢查完變成肉球的值消除，計算並回傳消除數量
    num = 0
    for y in range(10):
        for x in range(8):
            if neko[y][x] == 7:
                neko[y][x] = 0
                num = num + 1
    return num

def drop_neko():                    #由下往上檢查，若有值且下方為空，則將值往下放置
    flg = False                     
    for y in range         :      
        for x in range  :          
            if neko[y][x] != 0 and neko[y+1][x] == 0:       
                neko[y+1][x] = neko[y][x]                    
                neko[y][x] = 0                                
                flg = True                                   
    return flg                    

def over_neko():                  #判斷是否堆到頂端，若有則回傳Ture結束遊戲
    for x in range(8):
        if neko[0][x] > 0:
            return True
    return False

def set_neko():
    for x in range(8):
        neko[0][x] = random.randint(0, difficulty)

def draw_txt(txt, x, y, siz, col, tg):
    fnt = ("Times New Roman", siz, "bold")
    cvs.create_text(x+2, y+2, text=txt, fill="black", font=fnt, tag=tg)
    cvs.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)

def game_main():
    global index, timer, score, hisc, difficulty, tsugi
    global cursor_x, cursor_y, mouse_c
    if index == 0: 
        draw_txt("貓咪貓咪", int(312*scale), int(240*scale), int(100*scale), "violet", "TITLE")
        cvs.create_rectangle(int(168*scale), int(384*scale), int(456*scale), int(456*scale), fill="skyblue", width=0, tag="TITLE")
        draw_txt("Easy", int(312*scale), int(420*scale), int(40*scale), "white", "TITLE")
        cvs.create_rectangle(int(168*scale), int(528*scale), int(456*scale), int(600*scale), fill="lightgreen", width=0, tag="TITLE")
        draw_txt("Normal", int(312*scale), int(564*scale), int(40*scale), "white", "TITLE")
        cvs.create_rectangle(int(168*scale), int(672*scale), int(456*scale), int(744*scale), fill="orange", width=0, tag="TITLE")
        draw_txt("Hard", int(312*scale), int(708*scale), int(40*scale), "white", "TITLE")
        index = 1
        mouse_c = 0
    elif index == 1: # 標題畫面 等待遊戲開始
        difficulty = 0
        if mouse_c == 1:                 #判斷滑鼠點擊，以點擊當下位置設定難度
            if int(168*scale) < mouse_x and mouse_x < int(456*scale) and int(384*scale) < mouse_y and mouse_y < int(456*scale):
                difficulty = 4
            if int(168*scale) < mouse_x and mouse_x < int(456*scale) and int(528*scale) < mouse_y and mouse_y < int(600*scale):
                difficulty = 5
            if int(168*scale) < mouse_x and mouse_x < int(456*scale) and int(672*scale) < mouse_y and mouse_y < int(744*scale):
                difficulty = 6

        if difficulty > 0: # 當difficulty大於0，代表遊戲開始，數值初始
            for y in range(10):
                for x in range(8):
                    neko[y][x] = 0
            mouse_c = 0
            score = 0
            tsugi = 0
            cursor_x = 0
            cursor_y = 0
            set_neko()
            draw_neko()
            cvs.delete("TITLE")
            index = 2
    elif index == 2: # 貓咪落下
        if drop_neko() == False:
            index = 3
        draw_neko()
    elif index == 3: # 是否連成一線
        check_neko()
        draw_neko()
        index = 4
    elif index == 4: # 消除連成一線的貓咪
        sc = sweep_neko()                   #這邊會得到消除數量的回傳值
        score = score + sc*difficulty*2     #以消除數量及難度計算加分
        if score > hisc:                    #若分數大於最高分則記錄至最高分
            hisc = score
        if sc > 0:
            index = 2
        else:
            if over_neko() == False:
                tsugi = random.randint(1, difficulty)  #出下一隻貓的值讓玩家放置
                index = 5
            else:
                index = 6
                timer = 0
        draw_neko()
    elif index == 5: # 等待玩家滑鼠輸入
        if int(24*scale) <= mouse_x and mouse_x < int((24+72*8)*scale) and int(24*scale) <= mouse_y and mouse_y < int((24+72*10)*scale):
            cursor_x = int((mouse_x-(24*scale))/(72*scale))
            cursor_y = int((mouse_y-(24*scale))/(72*scale))
            if mouse_c == 1:                #判斷滑鼠點擊，將點擊位置替換值為放置的值
                mouse_c = 0
                set_neko()
                neko[cursor_y][cursor_x] = tsugi
                tsugi = 0
                index = 2
        cvs.delete("CURSOR")
        cvs.create_image(int((cursor_x*72+60)*scale), int((cursor_y*72+60)*scale), image=cursor, tag="CURSOR")
        draw_neko()


    elif index == 6: # 遊戲結束
        timer = timer + 1
        if timer == 1:
            draw_txt("GAME OVER", int(312*scale), int(348*scale), int(60*scale), "red", "OVER")
        if timer == 50:
            cvs.delete("OVER")
            index = 0
    cvs.delete("INFO")
    draw_txt("SCORE "+str(score), int(160*scale), int(60*scale), int(32*scale), "blue", "INFO")
    draw_txt("HISC "+str(hisc), int(450*scale), int(60*scale), int(32*scale), "yellow", "INFO")
    if tsugi > 0:
        cvs.create_image(int(752*scale), int(128*scale), image=img_neko[tsugi], tag="INFO")
    root.after(100, game_main)

# 視窗大小
width = int(912 * scale)
height = int(768 * scale)

root = tkinter.Tk()
root.title("掉落物拼圖「貓咪貓咪」")
root.resizable(False, False)
root.bind("<Motion>", mouse_move)
root.bind("<ButtonPress>", mouse_press)
cvs = tkinter.Canvas(root, width=width, height=height)
cvs.pack()

bg = tkinter.PhotoImage(file="neko_bg.png")
cursor = tkinter.PhotoImage(file="neko_cursor.png")
img_neko = [                                          
    None,
    tkinter.PhotoImage(file="neko1.png"),
    tkinter.PhotoImage(file="neko2.png"),
    tkinter.PhotoImage(file="neko3.png"),
    tkinter.PhotoImage(file="neko4.png"),
    tkinter.PhotoImage(file="neko5.png"),
    tkinter.PhotoImage(file="neko6.png"),
    tkinter.PhotoImage(file="neko_niku.png")          
]

cvs.create_image(width/2, height/2, image=bg)
game_main()
root.mainloop()
