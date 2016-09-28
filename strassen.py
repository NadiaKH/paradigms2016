import numpy as np


def separate_matrix(mtrx,mid):
    a11 = mtrx[:mid, :mid]
    a12 = mtrx[:mid, mid:]
    a21 = mtrx[mid:, :mid]
    a22 = mtrx[mid:, mid:]
    return a11, a12, a21, a22 

def mul(a, b):
    width, height = a.shape
    mid = width//2
    m = np.zeros((width, width), dtype=np.int)
    if width == 1:
        return a[0, 0] * b[0, 0]
    else:
        a11, a12, a21, a22 = separate_matrix(a, mid)
        b11, b12, b21, b22 = separate_matrix(b, mid)
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


def near_bigger_pow2(x):
    c = 1
    while x > c:
        c = c * 2
    return c


def array_extend_with_zero(a):
    width, height = a.shape
    pow2 = near_bigger_pow2(width)
    m = np.zeros(pow2 * pow2).reshape(pow2, pow2)
    m[:width, :height] = a
    return m


def input_of_matrix(a,n):
    for i in range(n):
        a[i]=np.asarray(input().split(' '),dtype=np.int)


def output_of_matrix(a,n):
    for i in range(n):
        for j in range(n):
            print(a[i,j],'',end="")
        print(end='\n')

        
if __name__ == '__main__':
    n = int(input())
    a = np.zeros((n, n), dtype=np.int)
    b = np.zeros((n, n), dtype=np.int)
    input_of_matrix(a,n)
    input_of_matrix(b,n)
    c = array_extend_with_zero(a)
    d = array_extend_with_zero(b)
    res_matrix = array_extend_with_zero(b)
    res_matrix = mul(c, d)
    output_of_matrix(res_matrix,n)
    
