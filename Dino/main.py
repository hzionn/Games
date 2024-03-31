import random

import pygame

from Dino.sound import load_sound
from Dino.sprite import load_sprite_sheet, load_image
from Dino.setting import TITLE, BACKGROUND_COLOR, FPS
from Dino.game_object import Dino, Cactus, Ptera, Cloud, Ground, Scoreboard

# -------------------------------------------------------------------------
# SCREEN_SIZE       :視窗大小
# FPS            :畫面刷新率
# GRAVITY        :恐龍重力(影響跳躍高度與墜落時間)
# BACKGROUND_COLOR :背景顏色
# high_score     :分數設定
# screen         :畫面顯示
# -------------------------------------------------------------------------
pygame.mixer.pre_init(44100, -16, 2, 2048)  # fix audio delay
pygame.init()  # pygame 初始

SCREEN_SIZE = (width, height) = (600, 300)  # 設定視窗大小
high_score = 0  # 分數初始化

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)


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


def introscreen():  # 起始畫面
    # -------------------------------------------------------------------------
    # 起始畫面
    #   callout         :畫面版權宣告
    #   temp_ground     :預設地板
    #   logo            :標題顯示
    # -------------------------------------------------------------------------

    temp_dino = Dino(screen, 44, 47)  # 建立起始畫面上的小恐龍
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
            screen.fill(BACKGROUND_COLOR)  # 用顏色填滿初始畫面的背景
            screen.blit(
                temp_ground[0], temp_ground_rect
            )  # 畫上地板(小恐龍腳下的部分地板)
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
    playerDino = Dino(screen, 44, 47)
    new_ground = Ground(screen, -1 * gamespeed)
    scb = Scoreboard(screen)
    highsc = Scoreboard(screen, width * 0.78)
    counter = 0

    # 建立 pygame.sprite.group物件
    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbutton_image, _ = load_image("replay_button.png", 35, 31, -1)  # 載入圖片
    gameover_image, _ = load_image("game_over.png", 190, 11, -1)  # 載入圖片

    # 將數字圖片分離成單一
    temp_images, temp_rect = load_sprite_sheet(
        "numbers.png", 12, 1, 11, int(11 * 6 / 5), -1
    )  # 載入數字
    HI_image = pygame.Surface((22, int(11 * 6 / 5)))
    # 繪製最高分數
    HI_rect = HI_image.get_rect()
    HI_image.fill(BACKGROUND_COLOR)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.1
    HI_rect.left = width * 0.73

    def jump():
        playerDino.isJumping = True
        if pygame.mixer.get_init() != None:
            load_sound("jump.wav").play()
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
                                and playerDino.isDucking
                                != True  # 保證小恐龍現在不是蹲下（正蹲下時不能跳）
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
                        load_sound("die.wav").play()

            for p in pteras:
                p.movement[0] = -1 * gamespeed
                if pygame.sprite.collide_mask(
                    playerDino, p
                ):  # collide_mask用來檢測兩個物件是否碰撞
                    playerDino.isDead = True  # 有碰撞，小恐龍死亡
                    if pygame.mixer.get_init() != None:
                        load_sound("die.wav").play()

            if len(cacti) < 2:  # 控制螢幕上仙人掌的數量，最多2個
                if len(cacti) == 0:  # 沒有仙人掌的情況下
                    last_obstacle.empty()  # 清空 last_obstacle 這個group物件
                    last_obstacle.add(Cactus(screen, gamespeed, 40, 40))  # 並新增仙人掌

                else:
                    for l in last_obstacle:
                        if (
                            l.rect.right < width * 0.7 and random.randrange(0, 50) == 10
                        ):  # 還有其他障礙物，但快要消失 (用random控制生成，並不是每次都會生成仙人掌)
                            last_obstacle.empty()  # 清空 last_obstacle 這個group物件
                            last_obstacle.add(
                                Cactus(screen, gamespeed, 40, 40)
                            )  # 並新增仙人掌

            if (
                len(pteras) == 0 and random.randrange(0, 200) == 10 and counter > 500
            ):  # 沒有飛鳥且時間大於500才會生成飛鳥 (用random控制生成，並不是每次都會生成飛鳥)
                for l in last_obstacle:
                    if l.rect.right < width * 0.8:  # 還有其他障礙物，但快要消失
                        # 新增烏鴉
                        last_obstacle.empty()  # 清空 last_obstacle 這個group物件
                        last_obstacle.add(
                            Ptera(screen, gamespeed, 46, 40)
                        )  # 並新增飛鳥

            if (
                len(clouds) < 5 and random.randrange(0, 300) == 10
            ):  # 控制螢幕上雲朵的數量，最多5個  (用random控制生成，並不是每次都會生成飛鳥)
                Cloud(
                    screen, width, random.randrange(height / 5, height / 2)
                )  # 隨機新增雲的出現位置

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
                screen.fill(BACKGROUND_COLOR)
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
        gameplay()


if __name__ == "__main__":
    main()
