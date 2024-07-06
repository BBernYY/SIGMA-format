from PIL import Image, ImageEnhance
import webcolors
import numpy as np
from colors import colors
from copy import copy
from os import path

COLORS = [list(i) for i in colors.keys()]
def closest(color):
    colors = np.array(COLORS)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance 


def to_sigma(name, effects=None, log=True):
    out = ""
    prev_value = 0
    with Image.open(name) as f:
        f = f.convert('RGB')
        if effects:
            f = effects(f)
        pixel_map = f.load()
        width, height = f.width, f.height
    for y in range(height):
        for x in range(width):
            pixel = pixel_map[x,y]
            out += webcolors.rgb_to_name(tuple(closest(list(pixel))[0]))+"\t"
        out = out[:-1]+"\n"
        percent_value = y*100//height
        if percent_value > prev_value and log:
            print(y*100//height, "%")
        prev_value = copy(percent_value)
    return out[:-1]

def from_sigma(name):
    with open(name) as f:
        f2 = f.read().replace('\x00', '').replace('\n\n', '\n')
        data = [i.split('\t') for i in f2.split("\n")]
        data2: list[tuple[int, int, int]] = np.full((*np.shape(data), 3), (0.0, 0.0, 0.0), dtype=int)
    for x in range(len(data)):
        for y in range(len(data[x])):
            a = data[x][y]
            a2 = tuple(webcolors.name_to_rgb(a))
            
            data2[x][y] = a2
    img = Image.fromarray(np.array(data2.astype(np.uint8)))
    img.save(path.splitext(name)[0]+'_out.jpg')

def increase_saturation(img):
    converter = ImageEnhance.Color(img)
    return converter.enhance(4)


NAME = "assets\\pfp.jpg"
out = to_sigma(NAME, increase_saturation)
with open(path.splitext(NAME)[0]+".sigma", 'w') as f:
    f.write(out)
from_sigma(path.splitext(NAME)[0]+".sigma")