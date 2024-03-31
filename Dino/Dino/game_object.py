import random

import pygame

from Dino.sprite import load_image, load_sprite_sheet
from Dino.sound import load_sound
from Dino.setting import BACKGROUND_COLOR, GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT


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
    def __init__(self, screen, sizex=-1, sizey=-1):  # OK
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
        self.rect.bottom = int(0.98 * SCREEN_HEIGHT)  # 設定小恐龍站的高度(上下)
        self.rect.left = SCREEN_WIDTH / 15  # 設定小恐龍站的位置(左右)
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
        self.screen = screen

        self.stand_pos_width = self.rect.width  # 設定站著的小恐龍寬度
        self.duck_pos_width = self.rect1.width  # 設定蹲下的小恐龍寬度

    def draw(self):  # OK
        self.screen.blit(self.image, self.rect)  # 將小恐龍畫至螢幕上

    def checkbounds(self):  # OK
        # 確保小龍的位置一直都站在0.98*height的位置上
        if self.rect.bottom > int(0.98 * SCREEN_HEIGHT):
            self.rect.bottom = int(0.98 * SCREEN_HEIGHT)
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
            self.movement[1] = self.movement[1] + GRAVITY  # movement[1]呼叫y軸做運算

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
                    load_sound("checkPoint.wav").play()
                    # checkPoint_sound.play()

        self.counter = self.counter + 1  # 增加計時器


class Cactus(pygame.sprite.Sprite):  # 仙人掌
    def __init__(self, screen, speed=5, sizex=-1, sizey=-1):  # OK
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet(
            "cacti-small.png", 3, 1, sizex, sizey, -1
        )  # 獲得切割後的圖檔以及一個rect物件
        self.rect.bottom = int(0.98 * SCREEN_HEIGHT)  # 設定仙人掌站的高度
        self.rect.left = SCREEN_WIDTH + self.rect.width  # 初始仙人掌的位置在螢幕外
        self.image = self.images[random.randrange(0, 3)]  # 隨機選擇仙人掌圖片
        self.movement = [-1 * speed, 0]  # 設定仙人掌的移動方向、速度
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)  # 將仙人掌畫至螢幕上

    def update(self):  # OK
        self.rect = self.rect.move(self.movement)  # 根據movement移動仙人掌物件

        if self.rect.right < 0:  # 如果仙人掌超出螢幕左邊，刪除該物件
            self.kill()


class Ptera(pygame.sprite.Sprite):
    """飛鳥"""

    def __init__(self, screen, speed=5, sizex=-1, sizey=-1):  # OK
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet(
            "ptera.png", 2, 1, sizex, sizey, -1
        )  # 獲得切割後的圖檔以及一個rect物件
        self.ptera_height = [SCREEN_HEIGHT * 0.82, SCREEN_HEIGHT * 0.75, SCREEN_HEIGHT * 0.60]  # 設定飛鳥的三種高度
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]  # 隨機決定飛鳥的三個高度
        self.rect.left = SCREEN_WIDTH + self.rect.width  # 初始仙人掌的位置在螢幕外
        self.image = self.images[0]  # 初始飛鳥的樣式
        self.movement = [-1 * speed, 0]  # 設定仙人掌的移動方向、速度
        self.index = 0
        self.counter = 0
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)  # 將飛鳥畫至螢幕上

    def update(self):
        if self.counter % 10 == 0:  # 切換飛鳥的兩個樣式
            self.index = (self.index + 1) % 2

        self.image = self.images[self.index]  # 設定image為，飛鳥的兩個樣式
        self.rect = self.rect.move(self.movement)  # 根據movement移動飛鳥
        self.counter = self.counter + 1  # 增加計時器

        if self.rect.right < 0:  #  如果飛鳥超出螢幕左邊，刪除該物件
            self.kill()


class Ground:
    def __init__(self, screen, speed=-5):  # OK
        # -------------------------------------------------------------------------
        # 	載入兩張背景圖片，以輪播的方式顯示於是窗上
        # -------------------------------------------------------------------------
        self.image, self.rect = load_image("ground.png", -1, -1, -1)  # 載入背景圖片
        self.image1, self.rect1 = load_image("ground.png", -1, -1, -1)  # 載入背景圖片
        self.rect.bottom = SCREEN_HEIGHT  # 設定圖片位置
        self.rect1.bottom = SCREEN_HEIGHT  # 設定圖片位置
        self.rect1.left = self.rect.right  # 設定圖片位置
        self.speed = speed  # 設定移動速度
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)  # 將背景畫至螢幕上
        self.screen.blit(self.image1, self.rect1)  # 將背景畫至螢幕上

    def update(self):
        self.rect.left += self.speed  # 根據speed移動圖片
        self.rect1.left += self.speed  # 根據speed移動圖片

        if self.rect.right < 0:  # 當第一張背景圖片完全超出螢幕
            self.rect.left = self.rect1.right  # 第一張圖片接在第二張圖片後

        if self.rect1.right < 0:  # 當第二張背景圖片完全超出螢幕
            self.rect1.left = self.rect.right  # 第二張圖片接在第一張圖片後# 背景圖片# 背景


class Cloud(pygame.sprite.Sprite):  # 雲
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image(
            "cloud.png", int(90 * 30 / 42), 30, -1
        )  # 載入雲的圖片
        self.speed = 1  # 設定移動速度
        self.rect.left = x  # 設定左右位置
        self.rect.top = y  # 設定高度
        self.movement = [-1 * self.speed, 0]  # 設定移動方向、速度
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)  # 將雲畫至螢幕上

    def update(self):
        self.rect = self.rect.move(self.movement)  # 根據movement移動雲
        if self.rect.right < 0:  #  如果雲超出螢幕左邊，刪除該物件
            self.kill()


class Scoreboard:  # 記分板
    def __init__(self, screen, x=-1, y=-1):  # OK
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet(
            "numbers.png", 12, 1, 11, int(11 * 6 / 5), -1
        )  # 載入數字
        self.image = pygame.Surface((55, int(11 * 6 / 5)))  # 建立一個surface擺放分數
        self.rect = self.image.get_rect()
        self.screen = screen
        # 設定記分板的位置
        if x == -1:
            self.rect.left = SCREEN_WIDTH * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = SCREEN_HEIGHT * 0.1
        else:
            self.rect.top = y

    def draw(self):
        self.screen.blit(self.image, self.rect)  # 劃出記分板

    def update(self, score):  # OK
        score_digits = extractDigits(score)  # 將數字拆解為一陣列
        self.image.fill(BACKGROUND_COLOR)  # 填滿記分板的背景顏色

        for s in score_digits:  # 根據每個分數，完成記分板
            self.image.blit(self.tempimages[s], self.temprect)  # 在計分板上畫上數字
            self.temprect.left += self.temprect.width  # 更新下一個數字的位置

        self.temprect.left = 0  # 都更新完後，下一個位置歸零
