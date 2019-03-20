# -*- coding: cp866 -*-


import os
from ctypes import POINTER,sizeof, c_void_p, c_int, c_bool ,c_uint64 ,string_at
from ctypes import c_uint8, c_uint16, c_uint32, Structure, Union,c_char ,addressof
#from ctypes.wintypes import  BYTE, WORD, DWORD
import ctypes
char=c_char
uint8_t=ctypes.c_uint8
uint16_t=ctypes.c_uint16
uint32_t=ctypes.c_uint32
#import getopt

#args = '-a -b -cfoo -d bar a1 a2'.split()




class HEAD(Structure):
    _fields_=[('wtype',uint16_t),
              ('dwlen',uint32_t)]
    _pack_=1


def revers(h,s=8):
    result=0
    for i in xrange(s):
        result=(h&0x1)|(result<<1)
        h=h>>1
    return result


#def read_pof(arg,dir=os.getcwd()):


#def control_reg(page_addr=0xfffff,sector_addr=0x7,wp=int("11111",2)):
#    return (page_addr & 0xfffff) | ((long(sector_addr) & 0x7) << 20) | ( wp<<23 )

def read_pof(arg,path=""):
    f=open(path+arg,"rb")
    s=f.read()
    f.close()

    if s[0:3]!="POF" and s[0:3]!="JIC":
        print "df"
        return  1

    pos=12
    sizeof_HEAD=sizeof(HEAD)

    sections="None"
    wtype=0
    while wtype!=0x8:
        h = HEAD.from_buffer_copy(s[pos:pos + sizeof_HEAD])
        pos += sizeof_HEAD
        wtype=h.wtype
        if wtype==0x2 :
            devise_name=s[pos:pos+h.dwlen]
        elif wtype==0x11 or  wtype==0x1c:
            data=s[pos+12:pos+h.dwlen]
        elif wtype==0x1a :
            sections=s[pos:pos+h.dwlen]
        pos += h.dwlen

    #devise_name.find("EPCS")>-1 or
    if  devise_name.find("10M")>-1:
        inv=0
        print arg
        #print devise_name
        sections=sections.split(";")
        CFM=sections[1].split()
        UFM=sections[0].split()
        #print int(CFM[1])
        #print data[long(CFM[1],16):long(CFM[1],16)+11]
        print hex(long(CFM[2],16)/8)
    elif devise_name.find("EPCS")>-1:
        inv = 1
        sections=sections.split(";")
        CFM=sections[0].split()
        #CFM[2] = hex(len(data) * 8)
    else :
        sections=sections.split(";")
        inv = 1
        #print "aaaa"
        CFM=["","0",""]
        CFM[2]=hex(len(data)*8)
        #CFM[2] = hex((len(data) / 4) * 8 * 4 - 1024 * 8 * (64 + 32))

    print long(CFM[2], 16)%8
    offset = (long(CFM[2], 16) / 8)
    data=data[long(CFM[1],16):long(CFM[1],16)+offset]
    data2=''
    if inv :
        for i in xrange(len(data)/4):
            for j in (0, 1, 2, 3):
                data2 += chr(revers(ord(data[i * 4 + j])))
    else :
        for i in xrange(len(data)/4) :
            for j in (3,2,1,0) :
                data2+=chr(revers (ord(data[i * 4 + j])))

    return data2


def read_rbf(arg,path=""):
    f=open(path+arg,"rb")
    data=f.read()
    f.close()
    data2 = ''
    for i in xrange(len(data)/4) :
        for j in (0,1,2,3) :
            data2+=chr(revers (ord(data[i * 4 + j])))

    return data2

#data_a=read_pof('output_file.jic')
#data_a=read_pof('module1.pof')
#data_a=read_rbf('output_file.rbf')
#type
#f = open("module"+".txt",'wb')
#f.write(data_a)
#f.close()

#f=open("SC01_1.txt","rb")
#data_b=f.read()
#f.close()

#compare=data_a==data_b[0:len(data_a)]
#for i in xrange()
#print compare
#from os import listdir
#for i in listdir("pofs"):
#    #print i
#    read_pof(i,"pofs//")