import numpy as np
import argparse
import imutils
import cv2
import random

# --------------- Aquí empieza el main ---------------
# 1. Obtener imagen
imgName = 'iguales.jpg'
original = cv2.imread(imgName)
#resized_og = cv2.resize(original, (256,256), interpolation = cv2.INTER_AREA)
original_gray = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
#cv2.imshow('original', original)
#cv2.waitKey(0)
img_bw = cv2.threshold(original_gray, 128, 255, cv2.THRESH_BINARY)[1] # convertir a blanco y negro
#print('og\n', image)

#resized_bw = cv2.resize(img_bw, (256,256), interpolation = cv2.INTER_AREA)

cv2.imshow('original', img_bw)
cv2.waitKey(0)

# Taking a matrix of size 5 as the kernel
kernel = np.ones((2,2), np.uint8)
img_dilation = cv2.erode(img_bw, kernel, iterations=1)

# find the contours
cnts = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print("Encontre {} figuras".format(len(cnts)))
circulos=0;
cuadrados=0;
rectangulos=0;
penta=0;
hexa=0;
trian=0;
shape = []
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.01 * peri, True)
    if len(approx) == 3:
        shape.append( "triangle" )
        trian=trian+1;
        original = cv2.fillPoly(original, pts =[c], color=(255,0,0))
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        if ar >= 0.75 and ar <= 1.35:
            shape.append( "square" )
            cuadrados=cuadrados+1;
            original = cv2.fillPoly(original, pts =[c], color=(100,100,0))
        else:
            shape.append( "rectangle" )
            rectangulos=rectangulos+1;
            original = cv2.fillPoly(original, pts =[c], color=(126,255,126))
    elif len(approx) == 5:
        shape.append( "pentagon" )
        penta=penta+1;
        original = cv2.fillPoly(original, pts =[c], color=(255,255,0))
    elif len(approx) == 6:
        shape.append( "hexagon" )
        hexa=hexa+1;
        original = cv2.fillPoly(original, pts =[c], color=(25,50,100))
    else:
        shape.append( "circle" )
        circulos=circulos+1;
        original = cv2.fillPoly(original, pts =[c], color=(0,0,255))
    
print('Encontre',len(list(set(shape))),'tipos distintos de figuras')
print('Encontre',cuadrados,'Rombos')
print('Encontre',circulos,'Circulos')
print('Encontre',rectangulos,'Rectangulos')


cv2.imshow(" ", original)
cv2.waitKey()
