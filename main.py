# https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
# https://towardsdatascience.com/adding-text-on-image-using-python-2f5bf61bf448

import glob
import time

import numpy as np
from PIL import Image, ImageFont, ImageDraw


IMAGE_DURATION = 1/10  # Duration of a single image (seconds)
FRAMERATE = 30
RESOLUTION = (768, 1024)

# Get all .jpg files in the current folder.
filenames = glob.glob('*.jpg')
# Sort files by the number following the underscore: <name>_<number>.jpg.
filenames.sort(key=lambda string: int(string.split('.')[0].split('_')[-1]))

# Load all image files and add text to each.
frames = []
for index in range(len(filenames)-1):
    images = [Image.open(filenames[index]), Image.open(filenames[index+1])]
    for i, image in enumerate(images):
        if image.size != RESOLUTION:
            image = image.resize(RESOLUTION)
            images[i] = image
    
    # Create each frame by blending two consecutive images.
    for alpha in np.arange(0, 1, 1 / (IMAGE_DURATION * FRAMERATE)):
        image = Image.blend(images[0], images[1], alpha)

        # Draw text.
        font = ImageFont.truetype('arial.ttf', round(RESOLUTION[1]/10))
        text = filenames[index].split('.')[0].split('_')[1]
        draw = ImageDraw.Draw(image)
        w, h = draw.textsize(text, font=font)
        position = ((RESOLUTION[0]-w)//2, RESOLUTION[1]//10-h//2)
        draw.text(position, text, fill=(255,255,255), font=font, stroke_width=round(RESOLUTION[1]/200), stroke_fill=(0,0,0))

        frames.append(image)
image, *frames = frames

# Write images to video.
image.save('timelapse.gif', format='GIF', append_images=frames, save_all=True, duration=1000/FRAMERATE, loop=0)