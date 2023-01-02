from mydefs.myimage import cropPicture
from PIL import Image
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

im = Image.open('testdata/defeat_elimination2.png')
im1, im2, im3, im4, im5, im6 = cropPicture(im)

fig = plt.figure()

ax1 = fig.add_subplot(2, 3, 1)
ax1.imshow(im1)

ax2 = fig.add_subplot(2, 3, 2)
ax2.imshow(im2)

ax3 = fig.add_subplot(2, 3, 3)
ax3.imshow(im3)

ax4 = fig.add_subplot(2, 3, 4)
ax4.imshow(im4)

ax5 = fig.add_subplot(2, 3, 5)
ax5.imshow(im4)

ax6 = fig.add_subplot(2, 3, 6)
ax6.imshow(im4)

plt.show()