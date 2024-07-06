from PIL import Image
import webcolors
import numpy as np
from colors import colors
from copy import copy
from colorsys import rgb_to_hsv, hsv_to_rgb
from os import path

COLORS = [list(i) for i in colors.keys()]
def closest(color):
    colors = np.array(COLORS)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance 


def to_sigma(name, log=True):
    out = ""
    prev_value = 0
    with Image.open(name) as f:
        f = f.convert('RGB')
        pixel_map = f.load()
        width, height = f.width, f.height
    for x in range(width):
        for y in range(height):
            pixel = pixel_map[x,y]
            out += webcolors.rgb_to_name(tuple(closest(list(pixel))[0]))+"\t"
        out = out[:-1]+"\n"
        percent_value = x*100//width
        if percent_value > prev_value and log:
            print(x*100//width, "%")
        prev_value = copy(percent_value)
    return out[:-1]

def from_sigma(name):
    with open(name) as f:
        f2 = f.read().replace('\x00', '').replace('\n\n', '\n')
        data = [i.split('\t') for i in f2.split("\n")]
        data2: list[tuple[int, int, int]] = np.full((*np.shape(data), 3), (0.0, 0.0, 0.0), dtype=int)
    for y in range(len(data)):
        for x in range(len(data[y])):
            a = data[y][x]
            a2 = tuple(webcolors.name_to_rgb(a))
            # ans = rgb_to_hsv(a2[0]/255, a2[1]/255, a2[2]/255)
            # ans2 = hsv_to_rgb(ans[0], ans[1], ans[2])
            # data2[y][x] = int(ans2[0]*255), int(ans2[1]*255), int(ans2[2]*255)
            # OMG I LITERALLY WASTED TWO HOURS ON THIS AND THE IMAGE WAS JUST FLIPPED
            # im gonna keep this here out of spite
            data2[y][x] = a2
    img = Image.fromarray(np.array(data2.astype(np.uint8)))
    img = img.rotate(-90)
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(path.splitext(name)[0]+'_out.jpg')
NAME = "assets\\biden.png"
with open(path.splitext(NAME)[0]+".sigma", 'w') as f:
    out = to_sigma(NAME)
    f.write(out)
from_sigma(path.splitext(NAME)[0]+".sigma")