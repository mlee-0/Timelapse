# https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
# https://towardsdatascience.com/adding-text-on-image-using-python-2f5bf61bf448

import glob

import numpy as np
from PIL import Image, ImageFont, ImageDraw


FRAMERATE = 1

# Get all .jpg files in the current folder.
filenames = glob.glob('*.jpg')
# Sort files by the number following the underscore: <name>_<number>.jpg.
filenames.sort(key=lambda string: int(string.split('.')[0].split('_')[-1]))

# Load all image files and add text to each.
images = []
for filename in filenames:
    image = Image.open(filename)
    try:
        if image.size != size:
            image = image.resize(size)
    except NameError:
        size = image.size
    
    font = ImageFont.truetype('arial.ttf', round(size[1]/10))
    text = filename.split('.')[0].split('_')[1]
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(text, font=font)
    position = ((size[0]-w)//2, size[1]//10-h//2)
    draw.text(position, text, fill=(255,255,255), font=font, stroke_width=round(size[1]/200), stroke_fill=(0,0,0))

    images.append(image)
image, *images = images

# Write images to video.
image.save('timelapse.gif', format='GIF', append_images=images, save_all=True, duration=1000/FRAMERATE, loop=0)