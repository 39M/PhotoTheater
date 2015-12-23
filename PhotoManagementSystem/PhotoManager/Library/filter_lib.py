from PIL import Image, ImageFilter
import numpy as ny
import math
import random
import facep


def blur(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.BLUR)
    result.save(dst)
    return 0


def detail(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.DETAIL)
    result.save(dst)
    return 0


def edgeenhance(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.EDGE_ENHANCE)
    result.save(dst)
    return 0


def contour(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.CONTOUR)
    result.save(dst)
    return 0


def emboss(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.EMBOSS)
    result.save(dst)
    return 0


def findedge(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.FIND_EDGES)
    result.save(dst)
    return 0


def smooth(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.SMOOTH)
    result.save(dst)
    return 0


def sharpen(src, dst):
    im = Image.open(src)
    im = im.convert("RGB")
    result = im.filter(ImageFilter.SHARPEN)
    result.save(dst)
    return 0


processAB = [64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
             64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64,
             64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 65, 66, 68, 69, 70, 71, 72, 73, 75, 76, 77, 78, 79, 80, 82, 83,
             84, 85, 86, 87, 89, 90, 91, 92, 93, 95, 96, 97, 98, 99, 100, 102, 103, 104, 105, 106, 107, 109, 110, 111,
             112, 113, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125, 126, 127, 129, 130, 131, 132, 133, 134, 136,
             137, 138, 139, 139, 140, 142, 143, 144, 145, 146, 147, 149, 150, 151, 152, 153, 154, 156, 157, 158, 159,
             160, 161, 163, 164, 165, 166, 167, 169, 170, 171, 172, 173, 174, 176, 177, 178, 179, 180, 181, 183, 184,
             185, 186, 187, 189, 190, 191, 192, 193, 194, 196, 197, 198, 199, 200, 201, 203, 204, 205, 206, 207, 208,
             210, 211, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212,
             212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212,
             212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212, 212,
             212, 212, 212, 212]
processAG = [57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57,
             57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57,
             57, 57, 57, 57, 57, 57, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 73, 73, 74, 75, 76, 77,
             78, 79, 80, 81, 83, 84, 85, 85, 86, 87, 88, 89, 90, 91, 93, 94, 95, 96, 96, 97, 98, 99, 100, 102, 103, 104,
             105, 106, 107, 108, 108, 109, 110, 112, 113, 114, 115, 116, 117, 118, 119, 120, 120, 122, 123, 124, 125,
             126, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 142, 143, 143, 144, 145,
             146, 147, 148, 149, 150, 152, 153, 154, 155, 155, 156, 157, 158, 159, 160, 162, 163, 164, 165, 166, 167,
             167, 168, 169, 170, 172, 173, 174, 175, 176, 177, 178, 179, 179, 181, 182, 183, 184, 185, 186, 187, 188,
             189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 202, 202, 203, 204, 205, 206, 207, 208, 209,
             210, 212, 213, 214, 214, 215, 216, 217, 218, 219, 221, 222, 223, 224, 225, 226, 226, 227, 228, 229, 231,
             232, 233, 234, 235, 236, 237, 237, 238, 239, 241, 242, 243, 244, 245, 246, 247, 248, 249, 249, 251, 252,
             253, 254]
processAR = [81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81,
             81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 81, 82, 84, 84,
             85, 86, 88, 88, 89, 91, 92, 93, 93, 95, 96, 97, 98, 99, 100, 101, 103, 103, 104, 106, 107, 107, 108, 110,
             111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 121, 122, 123, 125, 126, 126, 128, 129, 130, 131, 132,
             133, 134, 135, 136, 137, 138, 140, 140, 141, 143, 144, 145, 145, 147, 148, 149, 150, 151, 152, 154, 154,
             155, 156, 158, 159, 159, 161, 162, 163, 164, 164, 165, 166, 167, 168, 169, 170, 171, 173, 173, 174, 176,
             177, 178, 178, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 191, 192, 192, 193, 195, 196, 196, 198,
             199, 200, 201, 202, 203, 204, 206, 206, 207, 208, 210, 210, 211, 213, 214, 215, 215, 217, 218, 219, 220,
             221, 222, 223, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225,
             225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225,
             225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225, 225,
             225, 225, 225, 225, 225, 225, 225, 225, 225, 225]


class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=5, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


def filter1977(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph)
    result = ny.uint8(ny.zeros([height, width, 3]))
    for row in range(height):
        for col in range(width):
            result[row, col, 0] = processAR[source[row, col, 0]]
            result[row, col, 1] = processAG[source[row, col, 1]]
            result[row, col, 2] = processAB[source[row, col, 2]]

    result = Image.fromarray(ny.uint8(result)).convert('RGB')
    result.save(dst)
    return 0


def fcolor(l, percent, height, width):
    l_sort = ny.zeros([height, width])
    l_sort[:, :] = l[:, :]
    l_sort = l_sort.flatten()
    l_sort.sort()

    l_out = ny.zeros([height, width])
    l_out[:, :] = l[:, :]

    if percent == 0:
        l_min = min(l_sort)
        l_max = max(l_sort)
    else:
        l_min = l_sort[math.floor(height * width * percent)]
        l_max = l_sort[math.floor(height * width * (1 - percent))]

    for i in range(height):
        for j in range(width):
            if l[i, j] < l_min:
                l_out[i, j] = l_min
            elif l[i, j] > l_max:
                l_out[i, j] = 1
            else:
                l_out[i, j] = (l[i, j] - l_min) * (1 - l_min) / (l_max - l_min) + l_min

    return l_out


def autolevel(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph, 'f')
    result = source / 255
    R = result[:, :, 0]
    G = result[:, :, 1]
    B = result[:, :, 2]
    percent = 0.1
    result[:, :, 0] = fcolor(R, percent, height, width)
    result[:, :, 1] = fcolor(G, percent, height, width)
    result[:, :, 2] = fcolor(B, percent, height, width)
    result = ny.uint8(result * 255)

    result = Image.fromarray(result).convert('RGB')
    result.save(dst)
    return 0


def blackwhite(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]
    max_dic = {0: 1.16, 1: 1.25, 2: 0.21}
    max_mid = [
        {1: 1.16, 2: 0.47}, {0: 1.16, 2: -0.25}, {0: 0.47, 1: -0.25}
    ]

    source = ny.double(ny.array(graph))
    result = ny.uint8(ny.zeros([height, width]))
    for row in range(height):
        for col in range(width):
            index = ny.argsort(source[row, col])
            x = source[row, col, index[2]]
            d = source[row, col, index[1]]
            n = source[row, col, index[0]]
            xd = x - d
            dn = d - n
            result[row, col] = max(0, min(255, xd * max_dic[index[2]] + dn * max_mid[index[1]][index[2]] + n))

    result = Image.fromarray(result).convert('RGB')
    result.save(dst)
    return 0


def blackwhite2(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph)
    red = ny.matrix(ny.double(source[:, :, 0]))
    green = ny.matrix(ny.double(source[:, :, 1]))
    blue = ny.matrix(ny.double(source[:, :, 2]))
    # R = sum(sum(red).T) * 1.0 / width / height
    # red /= R
    result = ny.matrix(0.3 * red + 0.59 * green + 0.11 * blue)
    npercent = 1.5
    brightness = sum(sum(result).T) / width / height / 128
    result /= brightness
    result = brightness + (result - brightness) * npercent
    temp = 0.5 * red / ((green + blue + 1) / 2)
    # result *= temp
    for x in range(height):
        for y in range(width):
            result[x, y] *= temp[x, y]
            # result[x, y] *= (red[x, y] * 1.5)
            # if result[x, y] > 30:
            #     result[x, y] *= (result[x, y] * 4.0 / 255)
            # else:
            #     result[x, y] *= (result[x, y] * 2.0 / 255)
            result[x, y] = max(0, min(255, result[x, y]))

    result = Image.fromarray(ny.uint8(result)).convert('RGB')
    result.save(dst)
    return 0


def gauss(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    gaussin = graph.convert('RGB')

    gaussin = gaussin.filter(MyGaussianBlur())

    result = Image.fromarray(ny.uint8(gaussin)).convert('RGB')
    result.save(dst)
    return 0


def glow(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    source = graph.convert('RGB')
    Gauss = graph.convert('RGB')
    source = ny.double(ny.array(source))

    Gauss = Gauss.filter(MyGaussianBlur(radius=15))
    Gauss = ny.double(ny.array(source))

    Result = ny.zeros([height, width, 3])
    for row in range(height):
        for col in range(width):
            for k in range(3):
                if source[row, col, k] <= 128:
                    value = Gauss[row, col, k] * source[row, col, k] / 128
                    Result[row, col, k] = min(255, max(0, value))
                else:
                    value = 255 - (255 - Gauss[row, col, k]) * (255 - source[row, col, k]) / 128
                    Result[row, col, k] = min(255, max(0, value))

    result = Image.fromarray(ny.uint8(Result)).convert('RGB')
    result.save(dst)
    return 0


def oil(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    N = 1
    source = ny.array(graph)
    result = source
    for h in range(1 + N, height - N):
        for w in range(1 + N, width - N):
            k1 = random.random() - 0.5
            k2 = random.random() - 0.5
            m = k1 * (N * 2 - 1)
            n = k2 * (N * 2 - 1)
            hnew = int((h + m) % height)
            wnew = int((w + n) % width)
            wnew = width if wnew == 0 else wnew
            hnew = width if hnew == 0 else hnew
            result[h][w] = source[hnew][wnew]

    Image.fromarray(result).save(dst)
    return 0


def mode(base, mix):
    base = float(base)
    mix = float(mix)
    if mix > 128:
        res = int(base + (mix + mix - 255.0) * ((math.sqrt(base / 255.0)) * 255.0 - base) / 255.0)
    else:
        res = int(base + (mix + mix - 255.0) * (base - base * base / 255.0) / 255.0)
    return min(255, max(0, res))


def oldmovie(src, dst):
    graph = Image.open(src)
    mask = Image.open('PhotoManager/Library/mask.png')
    size = graph.size
    width = size[0]
    height = size[1]

    mask = mask.resize((width, height))
    mask = ny.uint16(ny.array(mask))
    result = ny.uint16(ny.array(graph))

    b = 10
    g = 130
    r = 200
    gray = 0
    for row in range(height):
        for col in range(width):
            gray = (result[row, col, 0] + result[row, col, 1] + result[row, col, 2]) / 3
            b = mode(gray, b)
            g = mode(gray, g)
            r = mode(gray, r)
            result[row, col, 0] = mode(b, mask[row, col, 0])
            result[row, col, 1] = mode(g, mask[row, col, 1])
            result[row, col, 2] = mode(r, mask[row, col, 2])

    result = Image.fromarray(ny.uint8(result)).convert('RGB')
    result.save(dst)
    return 0


def oldphoto(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.double(ny.array(graph))
    Result = ny.zeros([height, width, 3], dtype=ny.double)
    # Result[:, :] = source[:, :]
    Result[:, :, 0] = 0.393 * source[:, :, 0] + 0.769 * source[:, :, 1] + 0.189 * source[:, :, 2]
    Result[:, :, 1] = 0.349 * source[:, :, 0] + 0.686 * source[:, :, 1] + 0.168 * source[:, :, 2]
    Result[:, :, 2] = 0.272 * source[:, :, 0] + 0.534 * source[:, :, 1] + 0.131 * source[:, :, 2]

    result = Image.fromarray(ny.uint8(Result/1.4)).convert('RGB')
    result.save(dst)
    return 0


def processing(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    # source = ny.uint16(ny.array(graph))
    result = ny.int32(ny.array(graph))

    rMap = ny.int32(ny.zeros([256]))
    gMap = ny.int32(ny.zeros([256]))
    bMap = ny.int32(ny.zeros([256]))
    for i in range(256):
        value = i if i < 128 else 256 - i
        gray = int(math.pow(value, 3.0) / 64.0 / 256.0)
        rMap[i] = gray if i < 128 else 256 - gray
        gray = int(math.pow(value, 2) / 128.0)
        gMap[i] = gray if i < 128 else 256 - gray
        bMap[i] = i / 2 + 0x25

    for row in range(height):
        for col in range(width):
            b = bMap[result[row, col, 2]]
            g = gMap[result[row, col, 1]]
            r = rMap[result[row, col, 0]]
            b = min(255, max(0, b))
            g = min(255, max(0, g))
            r = min(255, max(0, r))
            result[row, col, 0] = r
            result[row, col, 1] = g
            result[row, col, 2] = b

    result = Image.fromarray(ny.uint8(result)).convert('RGB')
    result.save(dst)
    return 0


def sketch(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph)

    N = ny.zeros([height, width])
    g = ny.zeros([height, width])
    imggray = ny.zeros([height, width])
    for i in range(height):
        for j in range(width):
            imggray[i, j] = (source[i, j, 0] * 30 + source[i, j, 1] * 59 + source[i, j, 2] * 11 + 50) / 100
    out = ny.zeros([height, width])

    for i in range(height):
        for j in range(width):
            N[i, j] = 255 - imggray[i, j]

    # Get the Gauss template
    R = 5
    F = ny.zeros([2 * R + 1, 2 * R + 1])
    sigma = R / 3
    r = 0
    K = 0
    for x in range(2 * R + 1):
        for y in range(2 * R + 1):
            r = (x - R) * (x - R) + (y - R) * (y - R)
            F[x, y] = math.exp(-r / (2 * sigma * sigma))
            K = K + F[x, y]

    # Imfilter(N, F) / K
    for i in range(height):
        for j in range(width):
            top = min(height, i + R)
            bottom = max(0, i - R)
            left = max(0, j - R)
            right = min(width, j + R)
            temp = 0
            for x in range(bottom, top):
                for y in range(left, right):
                    temp += F[x - bottom, y - left] * N[x, y]
            g[i, j] = temp / K

    for i in range(height):
        for j in range(width):
            b = float(g[i, j])
            a = float(imggray[i, j])
            temp = a + a * b / (256 - b)
            out[i, j] = int(min(temp, 255))

    result = Image.fromarray(ny.uint8(out)).convert('RGB')
    result.save(dst)
    return 0


def spherize(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    pIn = ny.array(graph)
    pOut = ny.array(graph)
    cenY = height / 2
    cenX = width / 2
    offsetX = 0
    offsetY = 0
    newX = 0
    newY = 0
    radian = 0.0
    for row in range(height):
        for col in range(width):
            offsetX = col - cenX
            offsetY = row - cenY
            radian = math.atan2(offsetY, offsetX)
            radius = int((offsetX * offsetX + offsetY * offsetY) / max(cenX, cenY))
            newX = int(radius * math.cos(radian)) + cenX
            newY = int(radius * math.sin(radian)) + cenY
            newX = min(width - 1, max(0, newX))
            newY = min(height - 1, max(0, newY))
            pOut[row, col, 0] = pIn[newY, newX, 0]
            pOut[row, col, 1] = pIn[newY, newX, 1]
            pOut[row, col, 2] = pIn[newY, newX, 2]

    result = Image.fromarray(ny.uint8(pOut)).convert('RGB')
    result.save(dst)
    return 0


def spin(src, dst):
    graph = Image.open(src)
    size = graph.size
    width = size[0]
    height = size[1]

    source = ny.array(graph)
    I = ny.double(source)

    Image_new = ny.zeros([height, width, 3])
    Image_new[:] = I[:]
    Center_X = (width + 1) / 2.0
    Center_Y = (height + 1) / 2.0
    validPoint = 1
    angle = 10
    radian = angle * math.pi / 180.0
    radian2 = radian * radian
    Num = 30
    Num2 = Num * Num
    for D in range(3):
        for i in range(height):
            for j in range(width):
                validPoint = 1
                x0 = j - Center_X
                y0 = Center_Y - i
                x1 = x0
                y1 = y0
                Sum_Pixel = I[i, j, D]
                for k in range(Num):
                    x0 = x1
                    y0 = y1
                    x1 = x0 + radian * y0 / Num - radian2 * x0 / Num2
                    y1 = y0 - radian * x0 / Num - radian2 * y0 / Num2
                    x = int(x1 + Center_X)
                    y = int(Center_Y - y1)
                    if 0 < x < width - 1 and 0 < y < height - 1:
                        validPoint += 1
                        Sum_Pixel = Sum_Pixel+I[y, x, D]
                Image_new[i, j, D] = Sum_Pixel / validPoint

    result = Image.fromarray(ny.uint8(Image_new)).convert('RGB')
    result.save(dst)
    return 0


def sundancekid(src, dst):
    graph = Image.open(src)

    source = ny.double(ny.array(graph))
    result = source
    for dim in range(3):
        # temp = ny.uint8(source[:, :, dim] * 3 / 255)
        # result[:, :, dim] = 20 * temp * temp + 45 * temp + 42
        temp = ny.uint8(source[:, :, dim] * 2 / 255)
        result[:, :, dim] = 122 * temp + 61

    result = Image.fromarray(ny.uint8(result)).convert('RGB')
    result.save(dst)
    return 0


class Beeps(object):

    def __init__(self):
        pass

    def main(self, src, dst):

        graph = Image.open(src)
        resultjson = facep.detect(src)
        if resultjson != -1:
            land_mark = resultjson

            # Operate area
            size = graph.size
            width = size[0]
            height = size[1]

            contour_left3 = int(land_mark['result'][0]['landmark']['contour_left3']['x'] * width / 100) / 2 * 2
            left_eyebrow_upper_middle = int(land_mark['result'][0]['landmark']['left_eyebrow_upper_middle']['y'] * height / 100 * 0.97) / 2 * 2
            contour_right3 = int(land_mark['result'][0]['landmark']['contour_right3']['x'] * width / 100) / 2 * 2
            contour_right7 = int(land_mark['result'][0]['landmark']['contour_right7']['y'] * height / 100) / 2 * 2

            box = (contour_left3, left_eyebrow_upper_middle, contour_right3, contour_right7)
            self.graph = graph.crop(box)
            self.size = self.graph.size
            self.width = self.size[0]
            self.height = self.size[1]

            self.photometricDec = 10.0
            self.spatialDecay = 1.0

            self.gain_mu = (1.0 - self.spatialDecay) / (1.0 + self.spatialDecay)
            self.rho = 1.0 + self.spatialDecay
            self.c = -0.5/(self.photometricDec * self.photometricDec)

            self.hv_graph = ny.double(ny.zeros([self.height, self.width, 3]))
            self.vh_graph = ny.double(ny.zeros([self.height, self.width, 3]))
            self.result = ny.double(ny.zeros([self.height, self.width, 3]))
            self.graph = ny.double(self.graph)

            for d in range(3):
                self.hv_graph = self.graph[:, :, d]
                self.vh_graph = self.graph[:, :, d]

                self.beeps_hv()
                self.beeps_vh()

                for row in range(self.height):
                    for col in range(self.width):
                        self.result[row, col, d] = (self.vh_graph[row, col] + self.hv_graph[row, col]) / 2

            self.result = self.result[0:self.height-2, 0:self.width-2, :]
            self.result = Image.fromarray(ny.uint8(self.result)).convert('RGB')
            box = (contour_left3, left_eyebrow_upper_middle, contour_right3-2, contour_right7-2)
            graph.paste(self.result, box)
            graph.save(dst)
            return 0
        else:
            graph.save(dst)
            return -1

    def beeps_hv(self):
        g = ny.double(ny.zeros([self.height, self.width]))
        p = ny.double(ny.zeros([self.height, self.width]))
        r = ny.double(ny.zeros([self.height, self.width]))
        g[:] = self.hv_graph[:]
        p[:] = self.hv_graph[:]
        r[:] = self.hv_graph[:]

        for row in range(self.height):
            # BEEPSProgressive(g, row * width, width)
            g[row, 0] /= self.rho
            for col in range(1, self.width):
                mu = g[row, col] - self.rho * g[row, col - 1]
                mu = self.spatialDecay * math.exp(self.c * mu * mu)
                g[row, col] = g[row, col - 1] * mu + g[row, col] * (1 - mu) / self.rho

            # BEEPSGain (p, row * width, width)
            for col in range(self.width):
                p[row, col] *= self.gain_mu

            # BEEPSRegressive(r, width * col, width)
            r[row, self.width - 1] /= self.rho
            for col in range(self.width - 2, 0, -1):
                mu = r[row, col] - self.rho * r[row, col + 1]
                mu = self.spatialDecay * math.exp(self.c * mu * mu)
                r[row, col] = r[row, col + 1] * mu + r[row, col] * (1 - mu) / self.rho

                r[row, col] += g[row, col] - p[row, col]

        gnew = ny.double(ny.zeros([self.width, self.height]))
        pnew = ny.double(ny.zeros([self.width, self.height]))
        rnew = ny.double(ny.zeros([self.width, self.height]))
        for row in range(self.width):
            for col in range(self.height):
                gnew[row, col] = r[col, row]
                pnew[row, col] = r[col, row]
                rnew[row, col] = r[col, row]

        for row in range(self.width):
            # BEEPSProgressive(gnew, row*height,height)
            gnew[row, 0] /= self.rho
            for col in range(1, self.height):
                mu = gnew[row, col] - self.rho * gnew[row, col - 1]
                mu = self.spatialDecay * math.exp(self.c * mu * mu)
                gnew[row, col] = gnew[row, col - 1] * mu + gnew[row, col] * (1 - mu) / self.rho

            # BEEPSGain(pnew,row*height,height)
            for col in range(self.height):
                pnew[row, col] *= self.gain_mu

            # BEEPSRegressive(r,height*row,height)
            rnew[row, self.height - 1] /= self.rho
            for col in range(self.height - 2, 0, -1):
                mu = rnew[row, col] - self.rho * rnew[row, col + 1]
                mu = self.spatialDecay * math.exp(self.c * mu * mu)
                rnew[row, col] = rnew[row, col + 1] * mu + rnew[row, col] * (1 - mu) / self.rho

                rnew[row, col] += gnew[row, col] - pnew[row, col]
                self.hv_graph[col, row] = rnew[row, col]

    def beeps_vh(self):
        g = ny.double(ny.zeros([self.width, self.height]))
        p = ny.double(ny.zeros([self.width, self.height]))
        r = ny.double(ny.zeros([self.width, self.height]))
        for row in range(self.width):
            for col in range(self.height):
                g[row, col] = self.vh_graph[col, row]
                p[row, col] = self.vh_graph[col, row]
                r[row, col] = self.vh_graph[col, row]

        for row in range(self.width):
            # BEEPSProgressive(g, k1 * height, height)
            g[row, 0] /= self.rho
            for col in range(1, self.height):
                mu = g[row, col] - self.rho * g[row, col - 1]
                mu = self.spatialDecay * math.exp(self.c * mu * mu)
                g[row, col] = g[row, col - 1] * mu + g[row, col] * (1 - mu) / self.rho
            # BEEPSGain(p, k1 * height, height)
            for col in range(self.height):
                p[row, col] *= self.gain_mu
            # BEEPSRegressive(r, height * k1, height)
            r[row, self.height - 1] /= self.rho
            for col in range(self.height - 2, 0, -1):
                mu = r[row, col] - self.rho * r[row, col + 1]
                mu = self.spatialDecay * math.exp(self.c * mu * mu)
                r[row, col] = r[row, col + 1] * mu + r[row, col] * (1 - mu) / self.rho

                r[row, col] += g[row, col] - p[row, col]

        gnew = ny.double(ny.zeros([self.height, self.width]))
        pnew = ny.double(ny.zeros([self.height, self.width]))
        rnew = ny.double(ny.zeros([self.height, self.width]))
        for row in range(self.height):
            for col in range(self.width):
                gnew[row, col] = r[col, row]
                pnew[row, col] = r[col, row]
                rnew[row, col] = r[col, row]

        for row in range(self.height):
            # BEEPSProgressive(g, row * width, width)
            gnew[row, 0] /= self.rho
            for col in range(1, self.width):
                mu = gnew[row, col] - self.rho * gnew[row, col - 1]
                mu = self.spatialDecay * math.exp(self.c * mu * mu)
                gnew[row, col] = gnew[row, col - 1] * mu + gnew[row, col] * (1 - mu) / self.rho

            # BEEPSGain (p, row * width, width)
            for col in range(self.width):
                pnew[row, col] *= self.gain_mu

            # BEEPSRegressive(r, width * col, width)
            rnew[row, self.width - 1] /= self.rho
            for col in range(self.width - 2, 0, -1):
                mu = rnew[row, col] - self.rho * rnew[row, col + 1]
                mu = self.spatialDecay * math.exp(self.c * mu * mu)
                rnew[row, col] = rnew[row, col + 1] * mu + rnew[row, col] * (1 - mu) / self.rho

                self.vh_graph[row, col] = rnew[row, col] + gnew[row, col] - pnew[row, col]


def beeps(src, dst):
    B = Beeps()
    return Beeps.main(B, src, dst)


def baozou(src, dst):
    graph = Image.open(src)
    resultjson = facep.detect(src)
    if resultjson != -1:
        land_mark = resultjson

        # Operate area
        size = graph.size
        width = size[0]
        height = size[1]

        source = ny.array(graph)
        result = ny.matrix(0.3 * source[:, :, 1] + 0.59 * source[:, :, 2] + 0.11 * source[:, :, 2])
        npercent = 2
        # average = 128
        brightness = sum(sum(result).T) / width / height / 128 / 4
        # result += brightness * 0.9
        result /= brightness
        # result = average + (result - average) * npercent
        for x in range(height):
            for y in range(width):
                if result[x, y] > 220:
                    result[x, y] *= (result[x, y] * 2.0 / 255)
                result[x, y] = max(0, min(255, result[x, y]))
        result = Image.fromarray(ny.uint8(result)).convert('RGB')

        left_eyebrow_left_corner = int(land_mark['result'][0]['landmark']['left_eyebrow_left_corner']['x'] * width / 100) / 2 * 2
        left_eyebrow_upper_middle = int(land_mark['result'][0]['landmark']['left_eyebrow_upper_middle']['y'] * height / 100 * 0.97) / 2 * 2
        contour_right7x = int(land_mark['result'][0]['landmark']['contour_right7']['x'] * width / 100) / 2 * 2
        contour_right7y = int(land_mark['result'][0]['landmark']['contour_right7']['y'] * height / 100) / 2 * 2

        box = (left_eyebrow_left_corner, left_eyebrow_upper_middle, contour_right7x, contour_right7y)
        result = result.crop(box)
        size = result.size
        width = size[0]
        height = size[1]

        template = Image.open('PhotoManager/Library/template.jpg')
        temp = (width + height) * 2
        template = template.resize([temp, temp])
        per = 0.30
        x1 = int(temp / 2 - width / 2) / 2 * 2
        y1 = int(temp * per - height / 2) / 2 * 2
        x2 = int(temp / 2 + width / 2) / 2 * 2
        y2 = int(temp * per + height / 2) / 2 * 2
        tbox = [x1, y1, x2, y2]
        template.paste(result, tbox)

        result = Image.fromarray(ny.uint8(template)).convert('RGB')
        result.save(dst)
        return 0
    else:
        graph.save(dst)
        return -1


def enlarge(src, dst):
    # -*- coding: utf-8 -*-
    graph = Image.open(src)
    resultjson = facep.detect(src)
    if resultjson != -1:
        land_mark = resultjson

        # Operate area
        size = graph.size
        width = size[0]
        height = size[1]

        pIn = ny.array(graph)
        ptemp = pIn

        cenX = int(land_mark['result'][0]['landmark']['left_eye_bottom']['y'] * height / 100)
        cenY = int(land_mark['result'][0]['landmark']['left_eye_bottom']['x'] * width / 100)
        left_eye_left_corner = int(land_mark['result'][0]['landmark']['left_eye_left_corner']['x'] * width / 100)
        left_eye_right_corner = int(land_mark['result'][0]['landmark']['left_eye_right_corner']['x'] * width / 100)
        left_eye_top = int(land_mark['result'][0]['landmark']['left_eye_top']['y'] * height / 100)
        left_eye_bottom = int(land_mark['result'][0]['landmark']['left_eye_bottom']['y'] * height / 100)
        R = left_eye_right_corner - left_eye_left_corner
        # R = left_eye_bottom - left_eye_top
        R *= 1.1
        theta = math.pi
        for k in range(3):
            for x in range(1 - cenX, left_eye_bottom - cenX):
                for y in range(1 - cenY, width - cenY):
                    disX = int(1.2 * x)
                    disY = int(1.2 * y)

                    dis = disX * disX + disY * disY
                    r = math.sqrt(dis)
                    if r <= R and dis != 0:
                        xx = 2 * R * disX * math.acos(math.sqrt(R * R - dis) / R) / (theta * r) + cenX
                        yy = 2 * R * disY * math.acos(math.sqrt(R * R - dis) / R) / (theta * r) + cenY

                        xx = ny.around(ny.array(xx))
                        yy = ny.around(ny.array(yy))
                        if width >= yy >= 1 and height >= xx >= 1:
                            ptemp[x + cenX, y + cenY, k] = pIn[xx, yy, k]
                    else:
                        ptemp[x + cenX, y + cenY, k] = pIn[x + cenX, y + cenY, k]

        pOut = ptemp
        bias = height / 64
        cenX = int(land_mark['result'][0]['landmark']['right_eye_bottom']['y'] * height / 100) + bias
        cenY = int(land_mark['result'][0]['landmark']['right_eye_bottom']['x'] * width / 100)
        right_eye_left_corner = int(land_mark['result'][0]['landmark']['right_eye_left_corner']['x'] * width / 100)
        right_eye_right_corner = int(land_mark['result'][0]['landmark']['right_eye_right_corner']['x'] * width / 100)
        right_eye_top = int(land_mark['result'][0]['landmark']['right_eye_top']['y'] * height / 100)
        right_eye_bottom = int(land_mark['result'][0]['landmark']['right_eye_bottom']['y'] * height / 100)
        R = right_eye_right_corner - right_eye_left_corner
        # R = left_eye_bottom - left_eye_top
        R *= 1.1
        for k in range(3):
            for x in range(1 - cenX, right_eye_bottom + bias - cenX):
                for y in range(1 - cenY, width - cenY):
                    disX = int(1.2 * x)
                    disY = int(1.2 * y)

                    dis = disX * disX + disY * disY
                    r = math.sqrt(dis)
                    if r <= R and dis != 0:
                        xx = 2 * R * disX * math.acos(math.sqrt(R * R - dis) / R) / (theta * r) + cenX
                        yy = 2 * R * disY * math.acos(math.sqrt(R * R - dis) / R) / (theta * r) + cenY

                        xx = ny.around(ny.array(xx))
                        yy = ny.around(ny.array(yy))
                        if width >= yy >= 1 and height >= xx >= 1:
                            pOut[x + cenX, y + cenY, k] = pIn[xx, yy, k]
                    else:
                        pOut[x + cenX, y + cenY, k] = pIn[x + cenX, y + cenY, k]

        result = Image.fromarray(ny.uint8(pOut)).convert('RGB')
        result.save(dst)
        return 0
    else:
        graph.save(dst)
        return -1
