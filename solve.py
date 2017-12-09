from PIL import Image

colors = [
    (255, 255, 255), # U
    (0, 81, 186), # D
    (0, 158, 96), # F
    (255, 213, 0), # B
    (196, 30, 58), # R
    (255, 88, 0), # L
]

def solve(name):
    u_img = Image.open("{}_U.png".format(name), 'r')
    d_img = Image.open("{}_D.png".format(name), 'r')
    f_img = Image.open("{}_F.png".format(name), 'r')
    b_img = Image.open("{}_B.png".format(name), 'r')
    r_img = Image.open("{}_R.png".format(name), 'r')
    l_img = Image.open("{}_L.png".format(name), 'r')

    images = [u_img, d_img, f_img, b_img, r_img, l_img]
    for image in images:
        for y in range(3):
            for x in range(3):
                print(image.getpixel((x, y)))

    return u_img;

if __name__=="__main__":
    print(solve('02c286df1bbd7923d1f7'))
