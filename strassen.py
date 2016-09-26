import numpy as np


def mul(a, b):
    width, height = a.shape
    mid = width//2
    m = np.arange(width * width).reshape(width, width)
    if width == 1:
        return a[0, 0] * b[0, 0]
    else:
        a11 = a[:mid, :mid]
        a12 = a[:mid, mid:]
        a21 = a[mid:, :mid]
        a22 = a[mid:, mid:]
        b11 = b[:mid, :mid]
        b12 = b[:mid, mid:]
        b21 = b[mid:, :mid]
        b22 = b[mid:, mid:]
        p1 = mul(a11 + a22, b11 + b22)
        p2 = mul(a21 + a22, b11)
        p3 = mul(a11, b12 - b22)
        p4 = mul(a22, b21 - b11)
        p5 = mul(a11 + a12, b22)
        p6 = mul(a21 - a11, b11 + b12)
        p7 = mul(a12 - a22, b21 + b22)
        m[:mid, :mid] = p1 + p4 - p5 + p7
        m[:mid, mid:] = p3 + p5
        m[mid:, :mid] = p2 + p4
        m[mid:, mid:] = p1 - p2 + p3 + p6
        return m


def degree_of_2(x):
    c = 1
    while (x > c):
        c = c * 2
    return c


def new_array(a):
    x, y = a.shape
    z = degree_of_2(x)
    m = np.zeros(z * z).reshape(z, z)
    m[0:x, 0:x] = a
    return m


if __name__ == '__main__':
    i=int(input())
    a=np.arange(i * i).reshape(i, i)
    for p in range(i):
        for q in range(i):
            a[p, q]=input()
    b=new_array(a)
    print(mul(b, b))
