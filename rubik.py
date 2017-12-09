import urllib, urllib2
from PIL import Image
import zbarlight

def get_file(f):
    return f[7:-1] + f[-1]

host = 'http://qubicrube.pwn.seccon.jp:33654/'
img = 'images/01000000000000000000_B.png'

urllib.urlretrieve(host + img, get_file(img))
with open(get_file(img), 'rb') as image_file:
    image = Image.open(image_file)
    image.load()

codes = zbarlight.scan_codes('qrcode', image)
print('QR codes: %s' % codes)
