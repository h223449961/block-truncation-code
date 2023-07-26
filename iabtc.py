# -*- coding: utf-8 -*-
'''
一、統計所有 pixel 值量
二、計數 pixel 大於平均數的數量
'''
import cv2
import threading
import time
import sys
import numpy as np
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
def btcoding(image, height, width, bs):
	lheight, lwidth = int(height/bs), int(width/bs)
	tot = bs*bs

    
	for i in range(0, lheight):
		for j in range(0, lwidth):
			tempImg = image[i*bs:i*bs+bs,j*bs:j*bs+bs]
			mean = cv2.meanStdDev(tempImg)[0]
			std = cv2.meanStdDev(tempImg)[1]
            
			if i+j==0:
				print(tempImg)
				print(mean,std)
            
			for x in range(0, bs):
				for y in range(0, bs):
					if tempImg[x][y] > mean:
						tempImg[x][y] = 1
					else:
						tempImg[x][y] = 0

			sumPos = np.float32(np.sum(tempImg))
			if(sumPos == 0):
				sumPos = 1
            
			a = mean - (std * np.sqrt(float(sumPos)/abs(tot - sumPos)))
			b = mean + (std * np.sqrt(float(tot-sumPos)/abs(sumPos)))
			for x in range(0, bs):
				for y in range(0, bs):
					if tempImg[x][y] == 1:
						image[i*bs+x][j*bs+y] = b
					else:
						image[i*bs+x][j*bs+y] = a
	return np.uint8(image)
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img
def oas(filename):
    plt.cla()
    global b
    b = tk.Label(root)
    gray = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,250)),cv2.COLOR_BGR2GRAY)
    g = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,250)),cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,250)),cv2.COLOR_BGR2GRAY)
    y = np.zeros((256))
    count = 0
    m=gray.shape[0]*gray.shape[1]
    (mean,stddv) = cv2.meanStdDev(gray)
    for i in range(0,gray.shape[0]):
        for j in range(0,gray.shape[1]):
            y[gray[i,j]] += 1
            if(gray[i,j]>mean):
                count += 1
    sa = np.sqrt(count/(m-count))
    sb = np.sqrt((m-count)/count)
    a = mean-(stddv*sa)
    b = mean+(stddv*sb)
    l =[0,1,0,0,0,1,1,0]
    print('0 1 mask',l)
    for i in range(len(l)):
        if(l[i]==1):
            l[i]=int(b)
        if(l[i]==0):
            l[i]=int(a)
    print('h L mask',l)
    for i in range(0,gray.shape[0]):
        for j in range(0,gray.shape[1]):
            if(gray[(i,j)]>mean):
                gray[(i,j)]=b
            if(gray[(i,j)]<=mean):
                gray[(i,j)]=a
    print('original photo\n',gray)
    print('original',gray[0,0:len(l)])
    for i in range(len(l)):
        if(gray[(0,i)]!=l[i]):
            gray[(0,i)]=l[i]
    print('change',gray[0,0:len(l)])
    print('chage photo\n',gray)
    output=btcoding(g2,250,500,4)
    #cv2.imshow('Color input', output)
    #cv2.waitKey(0)
    btc=Image.fromarray(output)
    imgtk = ImageTk.PhotoImage(image=btc)
    b = tk.Label(image=imgtk)
    b.pack()
    b.imgtk = imgtk
    b.configure(image = imgtk)
    cvphoto = Image.fromarray(g)
    imgtk = ImageTk.PhotoImage(image=cvphoto)
    media.imgtk = imgtk
    media.configure(image=imgtk)
    plt.bar(np.arange(0,256),y,color="gray",align="center")
    canva.draw()
def opfile():
    b.destroy()
    sfname = filedialog.askopenfilename(title='選擇',filetypes=[('All Files','*'),("jpeg files","*.jpg"),("png files","*.png"),("gif files","*.gif")])
    return sfname
def oand():
    filename = opfile()
    oas(filename)
def main():
    global root
    root = tk.Tk()
    global b
    b = tk.Label(root)
    mediaFrame = tk.Frame(root).pack()
    global media
    media = tk.Label(mediaFrame)
    media.pack()
    fig = plt.figure()
    plot =fig.add_subplot(111)
    global canva
    canva = FigureCanvasTkAgg(fig,root)
    canva.get_tk_widget().pack(side='right')
    b1 = tk.Button(root, text="打開",command = oand).pack()
    root.mainloop()
if __name__=='__main__':
    main()