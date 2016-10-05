import numpy as np


def separate_matrix(m):
    upper_half, lower_half = np.vsplit(m, 2)
    a11, a12 = np.hsplit(upper_half, 2)
    a21, a22 = np.hsplit(lower_half, 2)
    return a11, a12, a21, a22


def mul(a, b):
    if a.size == 1:
        return np.dot(a, b)
    else:
        a11, a12, a21, a22 = separate_matrix(a)
        b11, b12, b21, b22 = separate_matrix(b)
        p1 = mul(a11 + a22, b11 + b22)
        p2 = mul(a21 + a22, b11)
        p3 = mul(a11, b12 - b22)
        p4 = mul(a22, b21 - b11)
        p5 = mul(a11 + a12, b22)
        p6 = mul(a21 - a11, b11 + b12)
        p7 = mul(a12 - a22, b21 + b22)
        с11 = p1 + p4 - p5 + p7
        с12 = p3 + p5
        с21 = p2 + p4
        с22 = p1 - p2 + p3 + p6
        return np.vstack((np.hstack((с11, с12)),
                          np.hstack((с21, с22))))


def near_bigger_pow2(x):
    c = 1
    while x > c:
        c *= 2
    return c


def read_matrix(n):
    a = np.zeros((near_bigger_pow2(n), near_bigger_pow2(n)), dtype=np.int)
    for i in range(n):
        a[i, :n] = np.array(input().split(), dtype=np.int)
    return a


def print_matrix(a):
    for matrix_row in a:
        print(*matrix_row)


if __name__ == '__main__':
    n = int(input())
    a = read_matrix(n)
    b = read_matrix(n)
    res_matrix = mul(a, b)
    print_matrix(res_matrix[:n, :n])
