from PIL import Image
from collections import Counter

colors = [
    (255, 255, 255), # U
    (0, 81, 186), # D
    (0, 158, 96), # F
    (255, 213, 0), # B
    (196, 30, 58), # R
    (255, 88, 0), # L
]

names = ['U', 'D', 'F', 'B', 'R', 'L']

def solve(name):
    u_img = Image.open("{}_U.png".format(name), 'r')
    d_img = Image.open("{}_D.png".format(name), 'r')
    f_img = Image.open("{}_F.png".format(name), 'r')
    b_img = Image.open("{}_B.png".format(name), 'r')
    r_img = Image.open("{}_R.png".format(name), 'r')
    l_img = Image.open("{}_L.png".format(name), 'r')

    images = [u_img, d_img, f_img, b_img, r_img, l_img]
    new_images = [
        Image.new(u_img.mode, (246, 246)),
        Image.new(u_img.mode, (246, 246)),
        Image.new(u_img.mode, (246, 246)),
        Image.new(u_img.mode, (246, 246)),
        Image.new(u_img.mode, (246, 246)),
        Image.new(u_img.mode, (246, 246)),
    ]
    faces = []
    for image in images:
        face = []
        for y in range(3):
            for x in range(3):
                counter = Counter()
                for dy in range(82):
                    for dx in range(82):
                        pixel = image.getpixel((x * 82 + dx, y * 82 + dy))
                        try:
                            index = colors.index(pixel)
                            counter[index] += 1
                        except:
                            pass

                color_index, count = counter.most_common(1)[0]
                face.append(color_index)
        faces.append(face)

    corners = [
        ((faces[0][6], 0, 6), (faces[2][0], 2, 0), (faces[5][2], 5, 2)),
        ((faces[0][8], 0, 8), (faces[4][0], 4, 0), (faces[2][2], 2, 2)),
        ((faces[0][2], 0, 2), (faces[3][0], 3, 0), (faces[4][2], 4, 2)),
        ((faces[0][0], 0, 0), (faces[5][0], 5, 0), (faces[3][2], 3, 2)),
        ((faces[1][6], 1, 6), (faces[5][8], 5, 8), (faces[2][6], 2, 6)),
        ((faces[1][8], 1, 8), (faces[2][8], 2, 8), (faces[4][6], 4, 6)),
        ((faces[1][2], 1, 2), (faces[4][8], 4, 8), (faces[3][6], 3, 6)),
        ((faces[1][0], 1, 0), (faces[3][8], 3, 8), (faces[5][6], 5, 6)),
    ]

    for corner in corners:
        colorset = list(map(lambda x: x[1], list(corner)))
        colorset_rotations = [
            (colorset[0], colorset[1], colorset[2]),
            (colorset[1], colorset[2], colorset[0]),
            (colorset[2], colorset[0], colorset[1]),
        ]

        for index, rotation in enumerate(colorset_rotations):
            for corner0 in corners:
                colorset0 = tuple(map(lambda x: x[0], list(corner0)))
                if colorset0 == rotation:
                    print(colorset, colorset0, index, corner, corner0)
                    for part_index, part in enumerate(corner):
                        area = images[corner0[(part_index - index) % 3][1]].crop((
                            (corner0[(part_index - index) % 3][2] % 3) * 82,
                            (corner0[(part_index - index) % 3][2] // 3) * 82,
                            (corner0[(part_index - index) % 3][2] % 3) * 82 + 82,
                            (corner0[(part_index - index) % 3][2] // 3) * 82 + 82
                        ))
                        copy_area = area.copy()
                        new_images[part[1]].paste(copy_area, ((
                            (part[2] % 3) * 82,
                            (part[2] // 3) * 82,
                            (part[2] % 3) * 82 + 82,
                            (part[2] // 3) * 82 + 82
                        )))

    new_images[0].save("{}.png".format(names[0]), 'png')
    new_images[1].save("{}.png".format(names[1]), 'png')
    new_images[2].save("{}.png".format(names[2]), 'png')
    new_images[3].save("{}.png".format(names[3]), 'png')
    new_images[4].save("{}.png".format(names[4]), 'png')
    new_images[5].save("{}.png".format(names[5]), 'png')

    return u_img;

if __name__=="__main__":
    print(solve('02c286df1bbd7923d1f7'))
