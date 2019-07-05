import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image,ImageEnhance,ImageFilter

def denoise(img_name = '/tmp/test2.png', output_path):
    #去除干扰线
    im = Image.open(img_name)
    #图像二值化
    im = im.convert('L')
    data = im.load()
    w,h = im.size
    for i in range(w):
        for j in range(h):
            if data[i, j] > 125:
                data[i, j] = 255  # 纯白
            else:
                data[i, j] = 0  # 纯黑
    # im.show()
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    data = im.getdata()
    # im.show()
    black_point = 0
    bp = 0
    for x in range(1,w-1):
        for y in range(1,h-1):
            mid_pixel = data[w*y+x] #中央像素点像素值
            if mid_pixel == 0: #找出上下左右四个方向像素点像素值
                top_pixel = data[w*(y-1)+x]
                left_pixel = data[w*y+(x-1)]
                down_pixel = data[w*(y+1)+x]
                right_pixel = data[w*y+(x+1)]
                right_pixel2 = data[w*y+(x+2)]
                right_pixel3 = data[w*y+(x+3)]

                tl_pixel = data[w*(y-1)+x-1]
                ld_pixel = data[w*(y+1)+(x-1)]
                rd_pixel = data[w*(y+1)+(x+1)]
                tr_pixel = data[w*(y-1)+(x+1)]
                if right_pixel != 0 and left_pixel != 0 and right_pixel2 != 0 and right_pixel3 != 0:
                    im.putpixel((x,y), 255)

                #判断上下左右的黑色像素点总个数
                if top_pixel == 0:
                    black_point += 1
                if left_pixel == 0:
                    black_point += 1
                if down_pixel == 0:
                    black_point += 1
                if right_pixel == 0:
                    black_point += 1
                if black_point >= 3:
                    im.putpixel((x,y),0)
                elif black_point < 2:
                    im.putpixel((x,y), 255)
                #print black_point
                black_point = 0
                bp = 0
    # for x in range(1,w-1):
    #     for y in range(1,h-1):
    #         mid_pixel = data[w*y+x] #中央像素点像素值
    #         if mid_pixel == 0: #找出上下左右四个方向像素点像素值
    #             top_pixel = data[w*(y-1)+x]
    #             left_pixel = data[w*y+(x-1)]
    #             down_pixel = data[w*(y+1)+x]
    #             right_pixel = data[w*y+(x+1)]
    #             right_pixel2 = data[w*y+(x+2)]
    #             right_pixel3 = data[w*y+(x+3)]

    #             tl_pixel = data[w*(y-1)+x-1]
    #             ld_pixel = data[w*(y+1)+(x-1)]
    #             rd_pixel = data[w*(y+1)+(x+1)]
    #             tr_pixel = data[w*(y-1)+(x+1)]
    #             if right_pixel != 0 and left_pixel != 0 and right_pixel2 != 0 and right_pixel3 != 0:
    #                 im.putpixel((x,y), 255)

    #             #判断上下左右的黑色像素点总个数
    #             if top_pixel == 0:
    #                 black_point += 1
    #             if left_pixel == 0:
    #                 black_point += 1
    #             if down_pixel == 0:
    #                 black_point += 1
    #             if right_pixel == 0:
    #                 black_point += 1
    #             if black_point >= 3:
    #                 im.putpixel((x,y),0)
    #             elif black_point < 2:
    #                 im.putpixel((x,y), 255)
    #             #print black_point
    #             black_point = 0
    #             bp = 0
    # im.putpixel((x,y), 0)
    # im.show()
    im.save(output_path)
    return im
