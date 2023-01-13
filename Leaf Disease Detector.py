################################################################
#       This program has been written by Branis GHOUL        #
################################################################

from tkinter import filedialog

import cv2
import numpy as np
import os
import sys
import tkinter


def ProcessImage(self):
    OriginalImage = cv2.imread(filename, 1)
    assert len(OriginalImage.shape) == 3, 'the image must contain all three RGB channels'

    cv2.imshow("Original Image", OriginalImage)
    b, g, r = cv2.split(OriginalImage)

    cv2.imshow("Red Channel", r)
    cv2.imshow("Green Channel", g)
    cv2.imshow("Blue Channel", b)
    Disease = r - g
    global Alpha
    Alpha = (r > 200).astype(int) * (g > 200).astype(int) * (b > 200).astype(int) * 255.0
    cv2.imshow("Alpha Channel", Alpha)
    ProcessingFactor = S.get()
    for row, col in np.argwhere(g > ProcessingFactor): 
        Disease[row, col] = 255.0

    cv2.imshow("Disease Image", Disease)
    DisplayDiseasePercentage(Disease)
    S.bind('<ButtonRelease-1>', ProcessImage)
    MainWindow.mainloop()



def GetFile():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return filedialog.askopenfilename(title="Select Image")


def DisplayDiseasePercentage(Disease):
    Count = 0
    Res = 0
    for i in range(0, Disease.shape[0]):
        for j in range(0, Disease.shape[1]):
            if Alpha[i, j] == 0:
                Res += 1
            if Disease[i, j] < S.get():
                Count += 1
    Percent = (Count / Res) * 100
    DiseasePercent.set("Percentage Disease: " + str(round(Percent, 2)) + "%")

if __name__ == "__main__":
    Alpha = None
    MainWindow = tkinter.Tk()
    MainWindow.title("Plant Disease Detector by Nahush Kulkarni")

    S = tkinter.Scale(MainWindow, from_=0, to=255, length=500, orient=tkinter.HORIZONTAL,
                    background='white', fg='black', troughcolor='white', label="Processing Factor")
    S.pack()
    S.set(150)

    DiseasePercent = tkinter.StringVar()
    L = tkinter.Label(MainWindow, textvariable=DiseasePercent)
    L.pack()

    filename = GetFile()
    try:
        ProcessImage(None)
    except Exception as e:
        print(e); sys.exit()
