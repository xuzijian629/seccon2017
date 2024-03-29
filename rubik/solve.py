from PIL import Image
from collections import Counter
import zbarlight
import urllib

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
    face_colors = []
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
                if x == 1 and y == 1:
                    face_colors.append(color_index)
        faces.append(face)

    rev_face_colors = [0,0,0,0,0,0]
    for index, color in enumerate(face_colors):
        rev_face_colors[color] = index

    corners = [
        ((faces[0][6], face_colors[0], 6), (faces[2][0], face_colors[2], 0), (faces[5][2], face_colors[5], 2)),
        ((faces[0][8], face_colors[0], 8), (faces[4][0], face_colors[4], 0), (faces[2][2], face_colors[2], 2)),
        ((faces[0][2], face_colors[0], 2), (faces[3][0], face_colors[3], 0), (faces[4][2], face_colors[4], 2)),
        ((faces[0][0], face_colors[0], 0), (faces[5][0], face_colors[5], 0), (faces[3][2], face_colors[3], 2)),
        ((faces[1][6], face_colors[1], 6), (faces[3][8], face_colors[3], 8), (faces[5][6], face_colors[5], 6)),
        ((faces[1][8], face_colors[1], 8), (faces[4][8], face_colors[4], 8), (faces[3][6], face_colors[3], 6)),
        ((faces[1][2], face_colors[1], 2), (faces[2][8], face_colors[2], 8), (faces[4][6], face_colors[4], 6)),
        ((faces[1][0], face_colors[1], 0), (faces[5][8], face_colors[5], 8), (faces[2][6], face_colors[2], 6)),
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
                    # print(colorset, colorset0, index, corner, corner0)
                    for part_index, part in enumerate(corner):
                        area = images[rev_face_colors[corner0[(part_index - index) % 3][1]]].crop((
                            (corner0[(part_index - index) % 3][2] % 3) * 82,
                            (corner0[(part_index - index) % 3][2] // 3) * 82,
                            (corner0[(part_index - index) % 3][2] % 3) * 82 + 82,
                            (corner0[(part_index - index) % 3][2] // 3) * 82 + 82
                        ))
                        copy_area = area.copy()

                        if corner0[(part_index - index) % 3][2] == 0:
                            rotate_from = 0
                        elif corner0[(part_index - index) % 3][2] == 2:
                            rotate_from = 1
                        elif corner0[(part_index - index) % 3][2] == 8:
                            rotate_from = 2
                        elif corner0[(part_index - index) % 3][2] == 6:
                            rotate_from = 3

                        if part[2] == 0:
                            rotate_to = 0
                        elif part[2] == 2:
                            rotate_to = 1
                        elif part[2] == 8:
                            rotate_to = 2
                        elif part[2] == 6:
                            rotate_to = 3

                        if (rotate_to - rotate_from + 4) % 4 == 3:
                            copy_area = copy_area.transpose(Image.ROTATE_90)
                        elif (rotate_to - rotate_from + 4) % 4 == 2:
                            copy_area = copy_area.transpose(Image.ROTATE_180)
                        elif (rotate_to - rotate_from + 4) % 4 == 1:
                            copy_area = copy_area.transpose(Image.ROTATE_270)

                        new_images[rev_face_colors[part[1]]].paste(copy_area, ((
                            (part[2] % 3) * 82,
                            (part[2] // 3) * 82,
                            (part[2] % 3) * 82 + 82,
                            (part[2] // 3) * 82 + 82
                        )))

    edges = [
        ((faces[0][7], face_colors[0], 7), (faces[2][1], face_colors[2], 1)),
        ((faces[0][5], face_colors[0], 5), (faces[4][1], face_colors[4], 1)),
        ((faces[0][1], face_colors[0], 1), (faces[3][1], face_colors[3], 1)),
        ((faces[0][3], face_colors[0], 3), (faces[5][1], face_colors[5], 1)),

        ((faces[2][5], face_colors[2], 5), (faces[4][3], face_colors[4], 3)),
        ((faces[4][5], face_colors[4], 5), (faces[3][3], face_colors[3], 3)),
        ((faces[3][5], face_colors[3], 5), (faces[5][3], face_colors[5], 3)),
        ((faces[5][5], face_colors[5], 5), (faces[2][3], face_colors[2], 3)),

        ((faces[1][7], face_colors[1], 7), (faces[3][7], face_colors[3], 7)),
        ((faces[1][5], face_colors[1], 5), (faces[4][7], face_colors[4], 7)),
        ((faces[1][1], face_colors[1], 1), (faces[2][7], face_colors[2], 7)),
        ((faces[1][3], face_colors[1], 3), (faces[5][7], face_colors[5], 7)),
    ]

    for edge in edges:
        colorset = list(map(lambda x: x[1], list(edge)))
        colorset_rotations = [
            (colorset[0], colorset[1]),
            (colorset[1], colorset[0]),
        ]

        for index, rotation in enumerate(colorset_rotations):
            for edge0 in edges:
                colorset0 = tuple(map(lambda x: x[0], list(edge0)))
                if colorset0 == rotation:
                    # print(colorset, colorset0, index, edge, edge0)
                    for part_index, part in enumerate(edge):
                        area = images[rev_face_colors[edge0[(part_index - index) % 2][1]]].crop((
                            (edge0[(part_index - index) % 2][2] % 3) * 82,
                            (edge0[(part_index - index) % 2][2] // 3) * 82,
                            (edge0[(part_index - index) % 2][2] % 3) * 82 + 82,
                            (edge0[(part_index - index) % 2][2] // 3) * 82 + 82
                        ))
                        copy_area = area.copy()

                        if edge0[(part_index - index) % 2][2] == 1:
                            rotate_from = 0
                        elif edge0[(part_index - index) % 2][2] == 5:
                            rotate_from = 1
                        elif edge0[(part_index - index) % 2][2] == 7:
                            rotate_from = 2
                        elif edge0[(part_index - index) % 2][2] == 3:
                            rotate_from = 3

                        if part[2] == 1:
                            rotate_to = 0
                        elif part[2] == 5:
                            rotate_to = 1
                        elif part[2] == 7:
                            rotate_to = 2
                        elif part[2] == 3:
                            rotate_to = 3

                        if (rotate_to - rotate_from + 4) % 4 == 3:
                            copy_area = copy_area.transpose(Image.ROTATE_90)
                        elif (rotate_to - rotate_from + 4) % 4 == 2:
                            copy_area = copy_area.transpose(Image.ROTATE_180)
                        elif (rotate_to - rotate_from + 4) % 4 == 1:
                            copy_area = copy_area.transpose(Image.ROTATE_270)

                        new_images[rev_face_colors[part[1]]].paste(copy_area, ((
                            (part[2] % 3) * 82,
                            (part[2] // 3) * 82,
                            (part[2] % 3) * 82 + 82,
                            (part[2] // 3) * 82 + 82
                        )))

    for face in range(6):
        for rotate in range(4):
            new_image = new_images[face].copy()
            center = images[face].crop((82, 82, 82 * 2, 82 * 2))
            center = center.copy()
            if rotate == 1:
                center = center.transpose(Image.ROTATE_90)
            elif rotate == 2:
                center = center.transpose(Image.ROTATE_180)
            elif rotate == 3:
                center = center.transpose(Image.ROTATE_270)

            new_image.paste(center, (82, 82, 82 * 2, 82 * 2))
            new_image.save("{}_{}.png".format(names[face], rotate), 'png')

    return u_img;

def get_file(f):
    return f[37:-1] + f[-1]

def get_file_name(f):
    return f[44:-1] + f[-1]

def generate_png_url(url):
    suffix = ['_U', '_D', '_L', '_R', '_F', '_B']
    return map(lambda s: url + s + '.png', suffix)

if __name__=="__main__":
    answers = []
    for i in ['U', 'D', 'L', 'R', 'F', 'B']:
        for j in [0,1,2,3]:
            answers.append("%s_%d.png" % (i,j))

    link = '01000000000000000000'
    for _ in range(50):
        solve(link)
        for i in range(24):
            with open(answers[i], 'rb') as f:
                img = Image.open(f)
                img.load()
                try:
                    code = zbarlight.scan_codes('qrcode', img)[0]
                    print(code)
                    if code[0:4] == 'http':
                        link = get_file(code)
                        for p in generate_png_url('http://qubicrube.pwn.seccon.jp:33654/images/' + link):
                            urllib.urlretrieve(p, get_file_name(p))
                except TypeError:
                    continue
