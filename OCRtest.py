import mydefs
import sys
from PIL import Image
import numpy as np

imgfile = sys.argv[1]
lang = sys.argv[2] if len(sys.argv) == 3 else 'eng'
mydefs.LANG = sys.argv[2] if len(sys.argv) == 3 else 'eng'

img = Image.open(imgfile)

print(mydefs.OCRmain(img, lang=lang))