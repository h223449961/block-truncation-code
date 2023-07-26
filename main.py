# -*- coding: utf-8 -*-
import cv2
import math
import numpy as np
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import zip_longest
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img
def psnr(original, contrast):
    mse = np.mean((original - contrast) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    PSNR = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return PSNR
def ninter(i):
    cop = np.copy(i)
    iupd,ileftr=cop.shape
    upd = int(iupd*2)
    leftr = int(ileftr*2)
    o = np.zeros((upd,leftr)) # 輸出圖片
    for i in range(upd):
        for j in range(leftr):
            scrx=round((i+1)*(iupd/upd))
            scry=round((j+1)*(ileftr/leftr))
            o[i,j]=cop[scrx-1,scry-1]
    return o.astype(np.uint8)
def binter(image):
    copy = np.copy(image)# 輸入圖像的副本
    iupD, ileftR = copy.shape # 輸入圖像的尺寸（行、列）
    upD = int(iupD * 2)# 輸出圖像的尺寸
    leftR = int(ileftR * 2)
    o = np.zeros((upD, leftR)) # 輸出圖片
    for i in range(upD):
        for j in range(leftR):
            # 輸出圖片中座標 （i，j）對應至輸入圖片中的最近的四個座標（x1，y1）（x2, y2），（x3， y3），(x4，y4)的均值
            temp_x = i / upD * iupD
            temp_y = j / leftR * ileftR
            x1 = int(temp_x)
            y1 = int(temp_y)
            x2 = x1
            y2 = y1 + 1
            x3 = x1 + 1
            y3 = y1
            x4 = x1 + 1
            y4 = y1 + 1
            u = temp_x - x1
            v = temp_y - y1
            # 防止越界
            if x4 >= iupD:
                x4 = iupD - 1
                x2 = x4
                x1 = x4 - 1
                x3 = x4 - 1
            if y4 >= ileftR:
                y4 = ileftR - 1
                y3 = y4
                y1 = y4 - 1
                y2 = y4 - 1
            # 插值
            o[i, j] = (1-u)*(1-v)*int(copy[x1, y1]) + (1-u)*v*int(copy[x2, y2]) + u*(1-v)*int(copy[x3, y3]) + u*v*int(copy[x4, y4])
    return o.astype(np.uint8)
def btc(image,bs):
    height = image.shape[0]
    width = image.shape[1]
    lheight, lwidth = int(height/bs), int(width/bs)
    m = bs*bs
    for i in range(0, lheight):
        for j in range(0, lwidth):
            tempImg = image[i*bs:i*bs+bs,j*bs:j*bs+bs]
            mean = cv2.meanStdDev(tempImg)[0]
            std = cv2.meanStdDev(tempImg)[1]
            '''
            在還沒 btc 處理前，展示第一個 block
            '''
            if(i+j==0):
                print('第二步，放大後展示第一個 block\n'+str(image[i*8:i*8+8,j*8:j*8+8]))
            for x in range(0, bs):
                for y in range(0, bs):
                    if tempImg[x][y] > mean:
                        tempImg[x][y] = 1
                    else:
                        tempImg[x][y] = 0
            sumPos = np.float32(np.sum(tempImg))
            if(sumPos == 0):
                sumPos = 1
            l = mean - (std*np.sqrt((sumPos)/abs(m - sumPos)))
            o1 = (m-sumPos)
            o2 = np.log(m-sumPos)
            h = mean + (std*np.sqrt((o2)/abs(sumPos)))
            for x in range(0, bs):
                for y in range(0, bs):
                    if tempImg[x][y] == 1:
                        image[i*bs+x][j*bs+y] = h
                    else:
                        image[i*bs+x][j*bs+y] = l
            '''
            在已經 btc 處理後，展示第一個 block
            '''
            #if(i+j==0):
                #print('在還沒 BTC 處理前 展示第一個 block\n'+str(tempImg))
    return np.uint8(image)
def oas(filename):
    plt.cla()
    global b
    b = tk.Label(root)
    '''
    原照片
    '''
    gray = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,250)),cv2.COLOR_BGR2GRAY)
    '''
    原本對比照片
    '''
    graycopy = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,250)),cv2.COLOR_BGR2GRAY)
    '''
     btc 照片
    '''
    graycopy2 = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,250)),cv2.COLOR_BGR2GRAY)
    '''
    畫照片的直方圖
    '''
    y = np.zeros((256))
    for i in range(0,gray.shape[0]):
        for j in range(0,gray.shape[1]):
            y[gray[i,j]] += 1
    plt.bar(np.arange(0,256),y,color="purple",align="center")
    canva.draw()
    '''
    雙線性插值
    '''
    n = binter(gray)
    nn = binter(graycopy2)
    '''
     btc 處理
    '''
    m = btc(n,4)
    p = round(psnr(m,nn),2)
    print(p)
    BTCimgtk = ImageTk.PhotoImage(image=Image.fromarray(m))
    b = tk.Label(image=BTCimgtk,text="processed and PSNR = "+str(p),font='Helvetica 24 bold',fg="black",compound = 'bottom',justify="center")
    b.pack()
    b.imgtk = BTCimgtk
    b.configure(image = BTCimgtk)
    '''
    原本對比
    '''
    OriginalImgtk = ImageTk.PhotoImage(image=Image.fromarray(graycopy))
    original.imgtk = OriginalImgtk
    original.configure(image=OriginalImgtk,text="Original",font='Helvetica 24 bold',fg="black",compound = 'bottom',justify="center")
def opfile():
    b.destroy()
    sfname = filedialog.askopenfilename(title='選擇',filetypes=[('All Files','*'),("jpeg files","*.jpg"),("png files","*.png"),("gif files","*.gif")])
    return sfname
def oand():
    
        filename = opfile()
        oas(filename)
    
        print('fin')
def main():
    global root
    root = tk.Tk()
    global b
    b = tk.Label(root)
    Originalframe = tk.Frame(root).pack()
    global original
    original = tk.Label(Originalframe)
    original.pack()
    fig = plt.figure()
    plot =fig.add_subplot(111)
    global canva
    canva = FigureCanvasTkAgg(fig,root)
    canva.get_tk_widget().pack(side='right')
    button = tk.Button(root, text="Open",command = oand).pack()
    root.mainloop()
if __name__=='__main__':
    main()