import urllib, urllib2
import qrcode

host = 'http://qubicrube.pwn.seccon.jp:33654/'
img = 'images/01000000000000000000_B.png'

d = qrcode.Decoder()
if d.decode('out'):
    print 'result: ' + d.result
else:
    print 'error: ' + d.error
