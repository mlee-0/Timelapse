# https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
# https://towardsdatascience.com/adding-text-on-image-using-python-2f5bf61bf448

import glob
import time

import numpy as np
from PIL import Image, ImageFont, ImageDraw


IMAGE_DURATION = 1/30  # Duration of a single image (seconds)
FRAMERATE = 30
RESOLUTION = (330, 440)

# Get all .jpg files in the current folder.
filenames = glob.glob('*.jpg')
# Sort files by the number following the underscore: <name>_<number>.jpg.
filenames.sort(key=lambda string: int(string.split('.')[0].split('_')[-1]))

# Load all image files and add text to each.
frames = []
for index, filename in enumerate(filenames):
    try:
        images = [Image.open(filename), Image.open(filenames[index+1])]
    except IndexError:
        images= [Image.open(filename), Image.open(filename)]
    for i, image in enumerate(images):
        if image.size != RESOLUTION:
            image = image.resize(RESOLUTION)
            images[i] = image
    
    # Create each frame by blending two consecutive images.
    if index == len(filenames)-1:
        IMAGE_DURATION *= 10
    for alpha in np.arange(0, 1, 1 / (IMAGE_DURATION * FRAMERATE)):
        image = Image.blend(images[0], images[1], alpha)

        # Draw text.
        if index < len(filenames) - 1:
            font = ImageFont.truetype('arial.ttf', round(RESOLUTION[1]/10))
            text = filename.split('.')[0].split('_')[1]
            draw = ImageDraw.Draw(image)
            w, h = draw.textsize(text, font=font)
            position = ((RESOLUTION[0]-w)//2, RESOLUTION[1]//10-h//2)
            draw.text(position, text, fill=(255,255,255), font=font, stroke_width=round(RESOLUTION[1]/200), stroke_fill=(0,0,0))

        frames.append(image)
image, *frames = frames

# Write images to video.
image.save(f'timelapse_{len(filenames)-1}.gif', format='GIF', append_images=frames, save_all=True, duration=1000/FRAMERATE, loop=0)