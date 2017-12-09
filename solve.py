from PIL import Image

def solve(name):
    img = Image.open("{}_U.png".format(name), 'r')
    return img;

if __name__=="__main__":
    print(solve('02c286df1bbd7923d1f7'))
