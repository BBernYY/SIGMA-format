from PIL import Image, ImageEnhance
import numpy as np
from colors import colors
from os import path
import colors as c
COLORS = np.array([list(i) for i in colors.keys()])
with Image.open('bake_texture.bmp') as f:
    pixel_map = f.load()

def println(*data):
    if LOG:
        print(*data)
def closest(color):
    r, g, b = color
    return c.colors[pixel_map[g*256+b,r]]


def to_sigma(name, effects=None):
    println(f"Converting {name} to .sigma file...")
    out = ""
    with Image.open(name) as f:
        f = f.convert('RGB')
        if effects:
            f = effects(f)
        pixel_map = f.load()
        width, height = f.width, f.height
    for y in range(height):
        out = ""
        for x in range(width):
            pixel = pixel_map[x,y]
            out += closest(pixel)+"\t"
        yield out[:-1]+"\n"
        if y % STEP == 0:
            println(f"row {y} of {height-1}")
    println(f"row {y} of {height-1}")
    println("DONE")




def from_sigma(name):
    println(f"Converting {name} to image file...")
    with open(name) as f:
        f2 = f.read().replace('\x00', '').replace('\n\n', '\n')
        data = [i.split('\t') for i in f2.split("\n")][:-1]
        data2: list[tuple[int, int, int]] = np.full((*np.shape(data), 3), (0.0, 0.0, 0.0), dtype=int)
    for x in range(len(data)):
        for y in range(len(data[x])):
            data2[x][y] = c.names[data[x][y]]
        if x % STEP == 0:
            println(f"row {x} of {len(data)-1}")
    println(f"row {x} of {len(data)-1}\nSaving as file...")
    img = Image.fromarray(np.array(data2.astype(np.uint8)))
    img.save(path.splitext(name)[0]+'_out'+path.splitext(NAME)[1])
    println("DONE")

def increase_saturation(img):
    converter = ImageEnhance.Color(img)
    return converter.enhance(1)

LOG = False
STEP = 10
NAME = "assets\\biden.png"
with open(path.splitext(NAME)[0]+".sigma", 'w') as f:
    for i in to_sigma(NAME, increase_saturation):
        f.write(i+"\n")
from_sigma(path.splitext(NAME)[0]+".sigma")