import numpy as np
def mul(a,b):#функция принимает квадратный массив с линейными размерами вида num^2 
    x,y=a.shape
    m=np.arange(x*x).reshape(x,x)
    if x==1:
        return a[0,0]*b[0,0]
    else:
        p1=mul(a[0:x//2,0:x//2]+a[x//2:x,x//2:x],b[0:x//2,0:x//2]+b[x//2:x,x//2:x])
        p2=mul(a[x//2:x,0:x//2]+a[x//2:x,x//2:x],b[0:x//2,0:x//2])
        p3=mul(a[0:x//2,0:x//2],b[0:x//2,x//2:x]-b[x//2:x,x//2:x])
        p4=mul(a[x//2:x,x//2:x],b[x//2:x,0:x//2]-b[0:x//2,0:x//2])
        p5=mul(a[0:x//2,0:x//2]+a[0:x//2,x//2:x],b[x//2:x,x//2:x])
        p6=mul(a[x//2:x,0:x//2]-a[0:x//2,0:x//2],b[0:x//2,0:x//2]+b[0:x//2,x//2:x])
        p7=mul(a[0:x//2,x//2:x]-a[x//2:x,x//2:x],b[x//2:x,0:x//2]+b[x//2:x,x//2:x])
       
        m[0:x//2,0:x//2]=p1+p4-p5+p7
        m[0:x//2,x//2:x]=p3+p5
        m[x//2:x,0:x//2]=p2+p4
        m[x//2:x,x//2:x]=p1-p2+p3+p6
        return m
def f(x):
    c=1
    while (x>c):
        c=c*2
    return (c)
def g(a):
    x,y=a.shape
    z=f(x)
    m=np.arange(z*z).reshape(z,z)
    m=m*0
    m[0:x,0:x]=a
    return m
if __name__=='__main__':
    a=np.arange(25).reshape(5,5)
    b=g(a)
    print(mul(b,b))
