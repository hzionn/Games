import os

import pygame
from pygame import RLEACCEL


def load_sprite_sheet(
    sheetname: str,
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
    fullpath = os.path.join(
        os.path.dirname(__file__), "sprites", sheetname
    )  # 獲得圖片路徑
    sheet = pygame.image.load(fullpath).convert()  # load image and turn into pixel

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
                image.set_colorkey(
                    colorkey, RLEACCEL
                )  # 與colorkey相同的顏色數值，將會被設定為透明

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(
                    image, (scalex, scaley)
                )  # 縮小或放大圖片的大小

            sprites.append(image)  # 將切割完成的圖片放進list

    sprite_rect = sprites[0].get_rect()  # 取出第一章圖片
    return sprites, sprite_rect  # 回傳切割完成的圖片，以及第一張圖片


def load_image(
    image_name: str,
    sizex=-1,
    sizey=-1,
    colorkey=None,
) -> tuple:  # OK
    # -------------------------------------------------------------------------
    # 圖片調用(開始及結束畫面)
    #   fullname       :其他副程式使用檔案名稱調用sprites圖片
    #   image          :獲得調用完的結果並轉換成像素格式
    #   colorkey       :透明度設定
    # -------------------------------------------------------------------------

    fullpath = os.path.join(
        os.path.dirname(__file__), "sprites", image_name
    )  # 獲得圖片路徑
    image = pygame.image.load(fullpath).convert()  # load image and turn into pixel

    # 去背
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))  # 獲得圖片在(0,0)位置的顏色值
        image.set_colorkey(
            colorkey, RLEACCEL
        )  # 與colorkey相同的顏色數值，將會被設定為透明

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))  # 縮小或放大圖片的大小
    return (image, image.get_rect())  # 回傳載入的圖片
