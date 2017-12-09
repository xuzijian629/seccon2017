import urllib, urllib2
from PIL import Image
import zbarlight
import random

colors = [
    (255, 255, 255), # U
    (0, 81, 186), # D
    (0, 158, 96), # F
    (255, 213, 0), # B
    (196, 30, 58), # R
    (255, 88, 0), # L
]

pieces = [(0,0,82,82), (0,82,82,164),(0,164,82,246),
       (82,0,164,82), (82,82,164,164),(82,164,164,246),
       (164,0,246,82), (164,82,246,164),(164,164,246,246)]

def get_file(f):
    return f[44:-1] + f[-1]

def crop_image(image):
    return map(lambda x: image.crop(x), pieces)

def rotates(image):
    return map(lambda x: image.rotate(x), [0,90,180,270])

def get_all_pieces(images):
    ret = []
    for image in images:
        for c in crop_image(image):
            ret += rotates(c)
    return ret

def fileter_by_color(color, images):
    return filter(lambda x: get_main_color(x) == color, images)

def generate_image(color_images):
    sample = random.sample(range(9), 9)
    image = Image.new('RGB', (246,246))
    for i in range(9):
        lefttop = (pieces[i][0], pieces[i][1])
        image.paste(color_images[sample[i]], lefttop)
    return image

def get_main_color(image):
    x = random.randint(0,81)
    y = random.randint(0,81)
    while not (image.getpixel((x,y)) in colors):
        x = random.randint(0,81)
        y = random.randint(0,81)
    return image.getpixel((x,y))

def generate_png_url(url):
    suffix = ['_U', '_D', '_L', '_R', '_F', '_B']
    return map(lambda s: url + s + '.png', suffix)

url = 'http://qubicrube.pwn.seccon.jp:33654/images/01000000000000000000'

for _ in range(1):
    images = []
    for img in generate_png_url(url):
        urllib.urlretrieve(img, get_file(img))
        with open(get_file(img), 'rb') as image_file:
            image = Image.open(image_file)
            image.load()
            images.append(image)
    pcs = get_all_pieces(images)
    whites = fileter_by_color(colors[0], pcs)
    while 1:
        img = generate_image(whites)
        try:
            code = zbarlight.scan_codes('qrcode', img)[0]
            print code
            break
        except TypeError:
            continue
