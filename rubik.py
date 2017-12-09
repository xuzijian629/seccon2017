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

def get_file(f):
    return f[44:-1] + f[-1]

def crop_image(image):
    xys = [(0,0,81,81), (0,82,81,163),(0,164,81,245),
           (82,0,163,81), (82,82,163,163),(82,164,163,245),
           (164,0,245,81), (164,82,245,163),(164,164,245,245)]
    return map(lambda x: image.crop(x), xys)

def rotates(image):
    return map(lambda x: x.rotate(x), [0,90,180,270])

def get_all_pieces(images):
    ret = []
    for image in images:
        for c in crop_image(image):
            ret += rotates(c)
    return ret

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
    for img in generate_png_url(url):
        urllib.urlretrieve(img, get_file(img))
        with open(get_file(img), 'rb') as image_file:
            image = Image.open(image_file)
            image.load()
        code = zbarlight.scan_codes('qrcode', image)[0]
        print code
        if code[0:4] == 'http':
            url = code.replace('http://qubicrube.pwn.seccon.jp:33654/', 'http://qubicrube.pwn.seccon.jp:33654/images/')
