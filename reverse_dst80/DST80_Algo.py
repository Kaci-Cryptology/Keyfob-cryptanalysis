import binascii
import math, sys

def bit(x,n): return (x>>n)&1

def bit_slice(x,msb,lsb): return (x&((2<<msb)-1))>>lsb

def bv2i(*args):
    o=0
    for i in args: o=(o<<1)|i
    return o

def fa(x): return bit(0x3a35acc5,x)

def fb(x): return bit(0xac35742e,x)

def fc(x): return bit(0xb81d8bd1,x)

def fd(x): return bit(0x5acc335a,x)

def fe(x): return bit(0xe247,x)

def fg(x): return bit(0x4e72,x)

def h(x): return (0x1f9826f4>>(2*x))&3
#def h(x): return [0,1,3,3,2,1,2,0,0,2,1,2,3,3,1,0][x]

def fn(s,k):
    return (
        fd(bv2i(bit(s,32),bit(k,32),bit(s,24),bit(k,24),bit(s,16))),
        fe(bv2i(bit(k,16),bit(s, 8),bit(k, 8),bit(k, 0))),
        fb(bv2i(bit(s,33),bit(k,33),bit(s,25),bit(k,25),bit(s,17))),
        fe(bv2i(bit(k,17),bit(s, 9),bit(k, 9),bit(k, 1))),

        fd(bv2i(bit(s,34),bit(k,34),bit(s,26),bit(k,26),bit(s,18))),
        fc(bv2i(bit(k,18),bit(s,10),bit(k,10),bit(s, 2),bit(k, 2))),
        fb(bv2i(bit(s,35),bit(k,35),bit(s,27),bit(k,27),bit(s,19))),
        fa(bv2i(bit(k,19),bit(s,11),bit(k,11),bit(s, 3),bit(k, 3))),

        fd(bv2i(bit(s,36),bit(k,36),bit(s,28),bit(k,28),bit(s,20))),
        fc(bv2i(bit(k,20),bit(s,12),bit(k,12),bit(s, 4),bit(k, 4))),
        fb(bv2i(bit(s,37),bit(k,37),bit(s,29),bit(k,29),bit(s,21))),
        fa(bv2i(bit(k,21),bit(s,13),bit(k,13),bit(s, 5),bit(k, 5))),

        fd(bv2i(bit(s,38),bit(k,38),bit(s,30),bit(k,30),bit(s,22))),
        fc(bv2i(bit(k,22),bit(s,14),bit(k,14),bit(s, 6),bit(k, 6))),
        fb(bv2i(bit(s,39),bit(k,39),bit(s,31),bit(k,31),bit(s,23))),
        fa(bv2i(bit(k,23),bit(s,15),bit(k,15),bit(s, 7),bit(k, 7))),
    )[::-1]

def g(s,k):
    fx=fn(s,k)
    return (
        fg(bv2i(*fx[ :4])),
        fg(bv2i(*fx[4:8])),
        fg(bv2i(*fx[8:12])),
        fg(bv2i(*fx[12:]))
    )[::-1]

def f(k,s):
    return h(bv2i(*g(s,k)))

def p1(x):
    out=x&(0b10100101)
    out|=bit(x,6)<<3
    out|=bit(x,4)<<1
    out|=bit(x,3)<<6
    out|=bit(x,1)<<4
    return out
    
def p2(x):
    out=0
    for i in range(0,40,8): 
        byte=bit_slice(x,i+8,i)
        out|=(p1(byte)<<i)
    return out

def dst80_merge(keyl,keyr):
    keyl = p2(keyl)
    keyr = p2(keyr)
    if bit(keyl,39)==1: keyl = 0x7fffffffff^keyl
    if bit(keyr,39)==1: keyr = 0x7fffffffff^keyr
    return (bit_slice(keyl,39,20)<<20)|bit_slice(keyr,39,20)
    
def lfsr_round(x):
    return (x>>1)|((bit(x,0)^bit(x,2)^bit(x,19)^bit(x,21))<<39)

def dst80_round(keyl,keyr,s):
    k=dst80_merge(keyl,keyr)
    s=(s>>2)|((f(k,s)^(s&3))<<38)
    keyr=lfsr_round(keyr)
    keyl=lfsr_round(keyl)
    return keyl,keyr,s

def dst80_rounds(keyl,keyr,s,nrounds):
    for i in range(nrounds):
        keyl,keyr,s=dst80_round(keyl,keyr,s)
    return s

def dst80(keyl,keyr,challenge):
    return dst80_rounds(keyl,keyr,challenge,200)&0xffffff

