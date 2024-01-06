import cv2
import numpy as np
import keyboard
import pyautogui
import mss
from time import sleep

pyautogui.PAUSE = 0

## Start the script by pressing "s"
keyboard.wait("s")

## Manually measured dimensions of the area of play 
dim = {
    'left': 615,
    'top': 295,
    'width': 665,
    'height': 665
}

## Manually collected image of one of tbe black tiles
black_tile = cv2.imread(r"C:\Users\Sayle\OneDrive\Documents\Python\BlackTile.png.png")

## Initialize screenshots
mss = mss.mss()

w = black_tile.shape[1]
h = black_tile.shape[0]

while 1:
    if keyboard.is_pressed("q"):
        break
        
    ## Get screenshot of area of play
    scr = np.array(mss.grab(dim))
    ## Had to remove alpha as this caused incompatibility issues
    scr_remove = scr[:,:,:3]

    ## Template matching algorithm to find and evaluate places where tiles deteced
    result = cv2.matchTemplate(scr_remove, black_tile, cv2.TM_CCOEFF_NORMED)
    y_val, x_val = np.where(result >= 0.60)

    ## Removing duplicate detections as this would cause more than one tap on a tile and end the game
    rectangles = []
    for (x, y) in zip(x_val, y_val):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, _ = cv2.groupRectangles(rectangles, 1, 0.2)
    ## Click on all tiles detected
    for r in rectangles:
        pyautogui.click(650 + r[0], 330 + r[1])
        
    sleep(0.10) # Can use 0.07 when not recording with obs for better results



