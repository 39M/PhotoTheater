from PIL import Image
import numpy as ny
import math
import facepp


class Beeps(object):

    def __init__(self, src, dst):
        API_KEY = 'e6999ac68d52bfb7ba47e3f2f779a225'
        API_SECRET = '8yEc6T_9GCIFQl6UFzl6mJ2jL1YkCFWc'

        api = facepp.API(API_KEY, API_SECRET)

        IMAGE = src

        # Detect face in the picture and find out his position and attributes

        face = api.detection.detect(img=facepp.File(IMAGE), mode='oneface')

        face_id = face['face'][0]['face_id']

        land_mark = api.detection.landmark(api_key=API_KEY, api_secret=API_SECRET, face_id=face_id)

        # Operate area
        graph = Image.open(src)
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
    Beeps(src=src, dst=dst)


def baozou(src, dst):
    API_KEY = 'e6999ac68d52bfb7ba47e3f2f779a225'
    API_SECRET = '8yEc6T_9GCIFQl6UFzl6mJ2jL1YkCFWc'

    api = facepp.API(API_KEY, API_SECRET)

    IMAGE = src

    # Detect face in the picture and find out his position and attributes

    face = api.detection.detect(img=facepp.File(IMAGE), mode='oneface')

    face_id = face['face'][0]['face_id']

    land_mark = api.detection.landmark(api_key=API_KEY, api_secret=API_SECRET, face_id=face_id)

    # Operate area
    graph = Image.open(src)
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

    template = Image.open('../PhotoManager/Library/template.jpg')
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


def enlarge(src, dst):
    # -*- coding: utf-8 -*-

    API_KEY = 'e6999ac68d52bfb7ba47e3f2f779a225'
    API_SECRET = '8yEc6T_9GCIFQl6UFzl6mJ2jL1YkCFWc'

    api = facepp.API(API_KEY, API_SECRET)

    IMAGE = src

    # Detect face in the picture and find out his position and attributes

    face = api.detection.detect(img=facepp.File(IMAGE), mode='oneface')

    face_id = face['face'][0]['face_id']

    land_mark = api.detection.landmark(api_key=API_KEY, api_secret=API_SECRET, face_id=face_id, type='25P')

    # Operate area
    graph = Image.open(src)
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
