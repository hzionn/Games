__author__ = "Shivam Shekhar"

import os

# import sys
import pygame
import random
from pygame import *

# -------------------------------------------------------------------------
# scr_size       :視窗大小
# FPS            :畫面刷新率
# gravity        :恐龍重力(影響跳躍高度與墜落時間)
# background_col :背景顏色
# high_score     :分數設定
# screen         :畫面顯示
# -------------------------------------------------------------------------
pygame.mixer.pre_init(44100, -16, 2, 2048)  # fix audio delay
pygame.init()  # pygame 初始

scr_size = (width, height) = (600, 300)  # 設定視窗大小
FPS = 60  # 幀數設定 低於30畫面卡頓
gravity = 0.6  # 影響恐龍的跳躍高度與墜落時間

black = (0, 0, 0)  # 設定黑色 rgb
white = (255, 255, 255)  # 設定白色 rgb
background_col = (235, 235, 235)  # 設定背景顏色 rgb

high_score = 0  # 分數初始化

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex Rush")

# 導入音效
jump_sound = pygame.mixer.Sound("sprites/jump.wav")
die_sound = pygame.mixer.Sound("sprites/die.wav")
checkPoint_sound = pygame.mixer.Sound("sprites/checkPoint.wav")


def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
):  # OK
    # -------------------------------------------------------------------------
    # 圖片調用(開始及結束畫面)
    #   fullname       :其他副程式使用檔案名稱調用sprites圖片
    #   image          :獲得調用完的結果並轉換成像素格式
    #   colorkey       :透明度設定
    # -------------------------------------------------------------------------

    fullname = os.path.join("sprites", name)  # 獲得圖片路徑
    image = pygame.image.load(fullname)  # 載入圖片
    image = image.convert()  # 將圖片轉換為像素格式

    # 去背
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))  # 獲得圖片在(0,0)位置的顏色值
        image.set_colorkey(colorkey, RLEACCEL)  # 與colorkey相同的顏色數值，將會被設定為透明

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))  # 縮小或放大圖片的大小

    return (image, image.get_rect())  # 回傳載入的圖片


def load_sprite_sheet(
    sheetname,
    nx,
    ny,
    scalex=-1,
    scaley=-1,
    colorkey=None,
):  # OK
    # -------------------------------------------------------------------------
    # 	目的：
    # 	將一張圖片，切成多個圖片，並且回傳圖片陣列
    #   fullname       :其他副程式使用檔案名稱調用sprites圖片
    #   sheet_rect     :獲取圖片的大小
    #   nx             :切成nx列
    #   ny             :切成ny行
    # -------------------------------------------------------------------------
    fullname = os.path.join("sprites", sheetname)  # 獲得圖片路徑
    sheet = pygame.image.load(fullname)  # 載入圖片
    sheet = sheet.convert()  # 將圖片轉換為像素格式

    sheet_rect = sheet.get_rect()  # 將圖片轉換為pygame.rect格式的物件
    sprites = []  # 用來存放切割完成的照片之list
    sizex = sheet_rect.width / nx  # 每一列的大小
    sizey = sheet_rect.height / ny  # 每一行的大小

    for i in range(0, ny):
        for j in range(0, nx):
            rect = pygame.Rect((j * sizex, i * sizey, sizex, sizey))  # 創建一個rect物件
            image = pygame.Surface(rect.size)  # 創建一個Surface物件
            image = image.convert()  # 將image轉為像素格式
            image.blit(
                sheet, (0, 0), rect
            )  # 若傳入一個Rect物件，則會使用Rect物件的左上方座標，將image物件繪製在sheet上，達到圖片切割的效果

            # 去背
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))  # 獲得圖片在(0,0)位置的顏色值
                image.set_colorkey(colorkey, RLEACCEL)  # 與colorkey相同的顏色數值，將會被設定為透明

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image, (scalex, scaley))  # 縮小或放大圖片的大小

            sprites.append(image)  # 將切割完成的圖片放進list

    sprite_rect = sprites[0].get_rect()  # 取出第一章圖片

    return sprites, sprite_rect  # 回傳切割完成的圖片，以及第一張圖片


def disp_gameOver_msg(retbutton_image, gameover_image):  # OK
    # -------------------------------------------------------------------------
    # 結束畫面顯示
    #   retbutton_rect :獲得"重新開始"的圖片大小
    #   gameover_rect  :獲得"GAME OVER"的圖片大小
    #   screen.blit    :把圖片重疊在rect後的圖片上
    # -------------------------------------------------------------------------
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = width / 2  # 設定"重新開始"位置
    retbutton_rect.top = height * 0.52  # 設定"重新開始"位置

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2  # 設定"GAME OVER"位置
    gameover_rect.centery = height * 0.35  # 設定"GAME OVER"位置

    screen.blit(retbutton_image, retbutton_rect)  # 將圖片繪製到螢幕上
    screen.blit(gameover_image, gameover_rect)  # 將圖片繪製到螢幕上


def extractDigits(number):  # OK
    # -------------------------------------------------------------------------
    # 	目的：
    # 	回傳每位數的係數
    # -------------------------------------------------------------------------

    if number > -1:
        digits = []
        # i = 0
        while number / 10 != 0:
            digits.append(number % 10)  # 獲得每位數之係數
            number = int(number / 10)

        digits.append(number % 10)  # 放入最後一位數之係數

        for _ in range(len(digits), 5):  # 若分數不到五位數字，則其他補零
            digits.append(0)

        digits.reverse()
        return digits  # 回傳切割好的分數陣列


class Dino:  # 小恐龍
    def __init__(self, sizex=-1, sizey=-1):  # OK
        # -------------------------------------------------------------------------
        # 	針對小恐龍的初始化
        # 	self.images 	：存放小恐龍奔跑、死亡的圖片(經過裁切後)
        # 	self.images1 	：存放小恐龍下蹲的圖片
        # -------------------------------------------------------------------------

        self.images, self.rect = load_sprite_sheet(
            "dino.png", 5, 1, sizex, sizey, -1
        )  # 獲得切割後的圖檔以及一個rect物件
        self.images1, self.rect1 = load_sprite_sheet(
            "dino_ducking.png", 2, 1, 59, sizey, -1
        )  # 獲得切割後的圖檔以及一個rect物件
        self.rect.bottom = int(0.98 * height)  # 設定小恐龍站的高度(上下)
        self.rect.left = width / 15  # 設定小恐龍站的位置(左右)
        self.image = self.images[0]  # 設定初始小恐龍之圖檔
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 12  # 跳的高度

        self.stand_pos_width = self.rect.width  # 設定站著的小恐龍寬度
        self.duck_pos_width = self.rect1.width  # 設定蹲下的小恐龍寬度

    def draw(self):  # OK
        screen.blit(self.image, self.rect)  # 將小恐龍畫至螢幕上

    def checkbounds(self):  # OK
        # 確保小龍的位置一直都站在0.98*height的位置上
        if self.rect.bottom > int(0.98 * height):
            self.rect.bottom = int(0.98 * height)
            self.isJumping = False

    def update(self):  # OK
        # -------------------------------------------------------------------------
        # 設定小恐龍樣式的切換
        # movement		: 設定rect物件移動的速度、方向
        # 	[0,0]	不移動
        # 	[0,1]	y軸正方向往上移動
        # 	[0,-1]  y軸負方向往下移動
        # counter		: 計時器，控制圖檔切換的時間差
        # -------------------------------------------------------------------------
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity  # movement[1]呼叫y軸做運算

        if self.isJumping:  # 跳起時，使用第一個樣式的小恐龍
            self.index = 0

        elif self.isBlinking:  # 在平地跑步時，第一與第二個樣式小恐龍交換出現
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        elif self.isDucking:  # 在蹲下時，切換蹲下的第一、第二樣式小恐龍
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.isDead:  # 死亡時，出現第五個樣式的小恐龍
            self.index = 4

        if not self.isDucking:  # 當小恐龍不是在蹲下的狀況時
            self.image = self.images[self.index]  # 設定image為，奔跑中的小恐龍
            self.rect.width = self.stand_pos_width  # 將rect物件之寬度，設定為奔跑中的寬度
        else:  # 當小恐龍在蹲下的狀況
            self.image = self.images1[(self.index) % 2]  # 設定image為，蹲下的小恐龍
            self.rect.width = self.duck_pos_width  # 將rect物件之寬度，設定為蹲下的寬度

        self.rect = self.rect.move(self.movement)  # 根據movement移動小恐龍
        self.checkbounds()  # 檢查移動完畢的物件是否有超出範圍

        if (
            not self.isDead and self.counter % 7 == 6 and self.isBlinking == False
        ):  # 計算分數
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:  # 每滿100分，放出音效
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = self.counter + 1  # 增加計時器


class Cactus(pygame.sprite.Sprite):  # 仙人掌
    def __init__(self, speed=5, sizex=-1, sizey=-1):  # OK
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet(
            "cacti-small.png", 3, 1, sizex, sizey, -1
        )  # 獲得切割後的圖檔以及一個rect物件
        self.rect.bottom = int(0.98 * height)  # 設定仙人掌站的高度
        self.rect.left = width + self.rect.width  # 初始仙人掌的位置在螢幕外
        self.image = self.images[random.randrange(0, 3)]  # 隨機選擇仙人掌圖片
        self.movement = [-1 * speed, 0]  # 設定仙人掌的移動方向、速度

    def draw(self):
        screen.blit(self.image, self.rect)  # 將仙人掌畫至螢幕上

    def update(self):  # OK
        self.rect = self.rect.move(self.movement)  # 根據movement移動仙人掌物件

        if self.rect.right < 0:  # 如果仙人掌超出螢幕左邊，刪除該物件
            self.kill()


class Ptera(pygame.sprite.Sprite):
    """飛鳥"""

    def __init__(self, speed=5, sizex=-1, sizey=-1):  # OK
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet(
            "ptera.png", 2, 1, sizex, sizey, -1
        )  # 獲得切割後的圖檔以及一個rect物件
        self.ptera_height = [height * 0.82, height * 0.75, height * 0.60]  # 設定飛鳥的三種高度
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]  # 隨機決定飛鳥的三個高度
        self.rect.left = width + self.rect.width  # 初始仙人掌的位置在螢幕外
        self.image = self.images[0]  # 初始飛鳥的樣式
        self.movement = [-1 * speed, 0]  # 設定仙人掌的移動方向、速度
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)  # 將飛鳥畫至螢幕上

    def update(self):
        if self.counter % 10 == 0:  # 切換飛鳥的兩個樣式
            self.index = (self.index + 1) % 2

        self.image = self.images[self.index]  # 設定image為，飛鳥的兩個樣式
        self.rect = self.rect.move(self.movement)  # 根據movement移動飛鳥
        self.counter = self.counter + 1  # 增加計時器

        if self.rect.right < 0:  #  如果飛鳥超出螢幕左邊，刪除該物件
            self.kill()


class Ground:
    def __init__(self, speed=-5):  # OK
        # -------------------------------------------------------------------------
        # 	載入兩張背景圖片，以輪播的方式顯示於是窗上
        # -------------------------------------------------------------------------
        self.image, self.rect = load_image("ground.png", -1, -1, -1)  # 載入背景圖片
        self.image1, self.rect1 = load_image("ground.png", -1, -1, -1)  # 載入背景圖片
        self.rect.bottom = height  # 設定圖片位置
        self.rect1.bottom = height  # 設定圖片位置
        self.rect1.left = self.rect.right  # 設定圖片位置
        self.speed = speed  # 設定移動速度

    def draw(self):
        screen.blit(self.image, self.rect)  # 將背景畫至螢幕上
        screen.blit(self.image1, self.rect1)  # 將背景畫至螢幕上

    def update(self):
        self.rect.left += self.speed  # 根據speed移動圖片
        self.rect1.left += self.speed  # 根據speed移動圖片

        if self.rect.right < 0:  # 當第一張背景圖片完全超出螢幕
            self.rect.left = self.rect1.right  # 第一張圖片接在第二張圖片後

        if self.rect1.right < 0:  # 當第二張背景圖片完全超出螢幕
            self.rect1.left = self.rect.right  # 第二張圖片接在第一張圖片後# 背景圖片# 背景


class Cloud(pygame.sprite.Sprite):  # 雲
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image(
            "cloud.png", int(90 * 30 / 42), 30, -1
        )  # 載入雲的圖片
        self.speed = 1  # 設定移動速度
        self.rect.left = x  # 設定左右位置
        self.rect.top = y  # 設定高度
        self.movement = [-1 * self.speed, 0]  # 設定移動方向、速度

    def draw(self):
        screen.blit(self.image, self.rect)  # 將雲畫至螢幕上

    def update(self):
        self.rect = self.rect.move(self.movement)  # 根據movement移動雲
        if self.rect.right < 0:  #  如果雲超出螢幕左邊，刪除該物件
            self.kill()


class Scoreboard:  # 記分板
    def __init__(self, x=-1, y=-1):  # OK
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet(
            "numbers.png", 12, 1, 11, int(11 * 6 / 5), -1
        )  # 載入數字
        self.image = pygame.Surface((55, int(11 * 6 / 5)))  # 建立一個surface擺放分數
        self.rect = self.image.get_rect()
        # 設定記分板的位置
        if x == -1:
            self.rect.left = width * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height * 0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)  # 劃出記分板

    def update(self, score):  # OK
        score_digits = extractDigits(score)  # 將數字拆解為一陣列
        self.image.fill(background_col)  # 填滿記分板的背景顏色

        for s in score_digits:  # 根據每個分數，完成記分板
            self.image.blit(self.tempimages[s], self.temprect)  # 在計分板上畫上數字
            self.temprect.left += self.temprect.width  # 更新下一個數字的位置

        self.temprect.left = 0  # 都更新完後，下一個位置歸零


def introscreen():  # 起始畫面
    # -------------------------------------------------------------------------
    # 起始畫面
    #   callout         :畫面版權宣告
    #   temp_ground     :預設地板
    #   logo            :標題顯示
    # -------------------------------------------------------------------------

    temp_dino = Dino(44, 47)  # 建立起始畫面上的小恐龍
    temp_dino.isBlinking = True
    gameStart = False

    # 繪製版權宣告
    callout, callout_rect = load_image("call_out.png", 196, 45, -1)
    callout_rect.left = width * 0.05
    callout_rect.top = height * 0.4

    # 繪製初始地板
    temp_ground, temp_ground_rect = load_sprite_sheet("ground.png", 15, 1, -1, -1, -1)
    temp_ground_rect.left = width / 20
    temp_ground_rect.bottom = height

    # 繪製標題
    logo, logo_rect = load_image("logo.png", 240, 40, -1)
    logo_rect.centerx = width * 0.6
    logo_rect.centery = height * 0.6

    # 如果遊戲尚未開始
    while not gameStart:
        # 檢查是否可以顯示遊戲
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True  # 回傳遊戲結束
        else:
            # -------------------------------------------------------------------------
            # 按鍵輸入偵測
            # -------------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 結束遊戲
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and temp_dino.rect.bottom == int(
                        0.98 * height
                    ):
                        temp_dino.isJumping = True  # 小恐龍跳躍
                        temp_dino.isBlinking = False  # 停止圖片切換
                        temp_dino.movement[1] = -1 * temp_dino.jumpSpeed  # 往上移動移動

        temp_dino.update()  # 更新小恐龍的狀態

        if pygame.display.get_surface() != None:
            screen.fill(background_col)  # 用顏色填滿初始畫面的背景
            screen.blit(temp_ground[0], temp_ground_rect)  # 畫上地板(小恐龍腳下的部分地板)
            if temp_dino.isBlinking:
                screen.blit(logo, logo_rect)  # 畫上logo
                screen.blit(callout, callout_rect)  # 畫上版權宣告
            temp_dino.draw()  # 畫出整個畫面

            pygame.display.update()

        clock.tick(FPS)

        # 當小恐龍完成一次的跳躍動作後，遊戲開始
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True


# -------------------------------------------------------------------------
# 遊戲內容設定
#   gamespeed      :遊戲畫面速度
#   startMenu      :開始畫面顯示
#   gameOver       :角色死亡
#   gameQuit       :角色退出
#   playerDino     :
#   new_ground     :畫面右邊出現的新地形跟gamespeed有關
#   scb            :右上分數顯示
#   highsc         :分數畫面大小
#   counter        :計算進行時間調整遊戲難度
#   cacti          :仙人掌角色群組
#   pteras         :烏鴉角色群組
#   clouds         :雲角色群組
# -------------------------------------------------------------------------
def gameplay():
    global high_score
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    playerDino = Dino(44, 47)
    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    counter = 0

    # 建立 pygame.sprite.group物件
    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbutton_image, retbutton_rect = load_image(
        "replay_button.png", 35, 31, -1
    )  # 載入圖片
    gameover_image, gameover_rect = load_image("game_over.png", 190, 11, -1)  # 載入圖片

    # 將數字圖片分離成單一
    temp_images, temp_rect = load_sprite_sheet(
        "numbers.png", 12, 1, 11, int(11 * 6 / 5), -1
    )  # 載入數字
    HI_image = pygame.Surface((22, int(11 * 6 / 5)))
    # 繪製最高分數
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.1
    HI_rect.left = width * 0.73

    def jump():
        playerDino.isJumping = True
        if pygame.mixer.get_init() != None:
            jump_sound.play()  # 撥放跳躍的音效
        playerDino.movement[1] = -1 * playerDino.jumpSpeed  # 小恐龍往上移動

    def duck():
        playerDino.isDucking = True

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            # print(playerDino.rect.bottom)
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 檢查是否關閉遊戲
                        gameQuit = True
                        gameOver = True
                    # -------------------------------------------------------------------------
                    # 任務一&任務二：按鍵輸入偵測
                    # -------------------------------------------------------------------------
                    if event.type == pygame.KEYDOWN:
                        # 判斷空白鍵按下跳躍
                        if event.key == pygame.K_SPACE:
                            if (
                                playerDino.rect.bottom
                                == int(0.98 * height)  # 保證小恐龍是站在地面
                                and playerDino.isDucking != True  # 保證小恐龍現在不是蹲下（正蹲下時不能跳）
                            ):
                                jump()

                        # 向下鍵按下蹲下
                        if event.key == pygame.K_DOWN:
                            if not (playerDino.isJumping and playerDino.isDead):
                                duck()

                    # 向下鍵放開取消蹲下
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False
            # -------------------------------------------------------------------------
            # 判斷角色狀態
            # -------------------------------------------------------------------------
            for c in cacti:
                c.movement[0] = -1 * gamespeed
                if pygame.sprite.collide_mask(
                    playerDino, c
                ):  # collide_mask用來檢測兩個物件是否碰撞
                    playerDino.isDead = True  # 有碰撞，小恐龍死亡
                    if pygame.mixer.get_init() != None:
                        die_sound.play()  # 播放死亡的音效

            for p in pteras:
                p.movement[0] = -1 * gamespeed
                if pygame.sprite.collide_mask(
                    playerDino, p
                ):  # collide_mask用來檢測兩個物件是否碰撞
                    playerDino.isDead = True  # 有碰撞，小恐龍死亡
                    if pygame.mixer.get_init() != None:
                        die_sound.play()  # 播放死亡的音效

            if len(cacti) < 2:  # 控制螢幕上仙人掌的數量，最多2個
                if len(cacti) == 0:  # 沒有仙人掌的情況下
                    last_obstacle.empty()  # 清空 last_obstacle 這個group物件
                    last_obstacle.add(Cactus(gamespeed, 40, 40))  # 並新增仙人掌

                else:
                    for l in last_obstacle:
                        if (
                            l.rect.right < width * 0.7 and random.randrange(0, 50) == 10
                        ):  # 還有其他障礙物，但快要消失 (用random控制生成，並不是每次都會生成仙人掌)
                            last_obstacle.empty()  # 清空 last_obstacle 這個group物件
                            last_obstacle.add(Cactus(gamespeed, 40, 40))  # 並新增仙人掌

            if (
                len(pteras) == 0 and random.randrange(0, 200) == 10 and counter > 500
            ):  # 沒有飛鳥且時間大於500才會生成飛鳥 (用random控制生成，並不是每次都會生成飛鳥)
                for l in last_obstacle:
                    if l.rect.right < width * 0.8:  # 還有其他障礙物，但快要消失
                        # 新增烏鴉
                        last_obstacle.empty()  # 清空 last_obstacle 這個group物件
                        last_obstacle.add(Ptera(gamespeed, 46, 40))  # 並新增飛鳥

            if (
                len(clouds) < 5 and random.randrange(0, 300) == 10
            ):  # 控制螢幕上雲朵的數量，最多5個  (用random控制生成，並不是每次都會生成飛鳥)
                Cloud(width, random.randrange(height / 5, height / 2))  # 隨機新增雲的出現位置

            # 更新畫面
            playerDino.update()
            cacti.update()
            pteras.update()
            clouds.update()
            new_ground.update()
            scb.update(playerDino.score)
            highsc.update(high_score)

            # 判斷Surface頁面是否不等於None
            if pygame.display.get_surface() != None:
                # 繪畫出物件(draw)
                screen.fill(background_col)
                new_ground.draw()
                clouds.draw(screen)
                scb.draw()
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                cacti.draw(screen)
                pteras.draw(screen)
                playerDino.draw()

                pygame.display.update()
            clock.tick(FPS)

            if playerDino.isDead:  # 如果小恐龍死亡
                gameOver = True
                if playerDino.score > high_score:  # 如果大於最高分數
                    high_score = playerDino.score  # 更新最高分數

            if counter % 700 == 699:  # 當時間超過700時
                new_ground.speed -= 1  # 減少背景圖片的速度
                gamespeed += 1  # 提升遊戲難度

            counter = counter + 1

        if gameQuit:
            break

        while gameOver:  # 當遊戲結束(小恐龍死亡)
            # 頁面顯示錯誤退出
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                # 在gameOver頁面時按鍵偵測
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        # esc按下Quit
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False
                        # Return或空白鍵按下繼續遊戲
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameplay()

            highsc.update(high_score)  # 更新最高分數

            if pygame.display.get_surface() != None:
                disp_gameOver_msg(retbutton_image, gameover_image)  # 顯示遊戲結束畫面

                if high_score != 0:  # 更新最高分數到遊戲結束畫面上
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)

                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


def main():
    isGameQuit = introscreen()  # 從初始畫面獲得是否開始遊戲

    if not isGameQuit:
        gameplay()  # 遊戲開始


main()
