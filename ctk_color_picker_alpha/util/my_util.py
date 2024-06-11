# https://math.stackexchange.com/questions/556341/rgb-to-hsv-color-conversion-algorithm
def rgb_to_hsv(r, g, b):
    r /= 255
    g /= 255
    b /= 255
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, round(v*100)
    s = (maxc - minc) / maxc
    rc = (maxc - r) / (maxc - minc)
    gc = (maxc - g) / (maxc - minc)
    bc = (maxc - b) / (maxc - minc)
    if r == maxc:
        h = 0.0 + bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = (h / 6.0) % 1.0
    return [round(h * 360), round(s * 100), round(v * 100)]


# https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
def hsv_to_rgb(h, s, v):
    if s:
        if h == 1.0:
            h = 0.0
        i = int(h * 6.0)
        f = h * 6.0 - i

        w = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))

        v = round(v * 255)
        t = round(t * 255)
        w = round(w * 255)
        q = round(q * 255)

        if i == 0:
            return [v, t, w]
        if i == 1:
            return [q, v, w]
        if i == 2:
            return [w, v, t]
        if i == 3:
            return [w, q, v]
        if i == 4:
            return [t, w, v]
        if i == 5:
            return [v, w, q]
    else:
        return [v, v, v]


def convert_to_value_100_rgb(r, g, b):
    hsv = rgb_to_hsv(r, g, b)
    return hsv_to_rgb(hsv[0]/360, hsv[1]/100, 1)
