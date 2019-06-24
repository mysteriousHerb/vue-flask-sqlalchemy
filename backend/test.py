import pickle
import hashlib
import os
import pickle
import json
import face_recognition
from PIL import Image, ImageDraw

# get an image
filepath = 'temp\\unknown_face_6.jpg'
source_img = Image.open(filepath).convert("RGB")

draw = ImageDraw.Draw(source_img)
top, right, bottom, left = (29, 175, 185, 29)
new_rect= [left, top, right, bottom]
# [x0, y0, x1, y1] = left, top, right, bottom
draw.rectangle((new_rect), fill="black")

filepath_out = 'temp\\unknown_face_1_mod.jpg'
source_img.save(filepath_out, "JPEG")