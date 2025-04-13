import cv2
import numpy as np

img = cv2.imread('Back.png')
res = cv2.resize(img, dsize=(54, 140), interpolation=cv2.INTER_CUBIC)