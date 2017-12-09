import urllib, urllib2
from PIL import Image
import zbarlight

def get_file(f):
    return f[44:-1] + f[-1]

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
