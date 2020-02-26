# -*- coding: utf-8 -*-
from ctypes import POINTER,sizeof, c_void_p, c_int, c_bool ,c_uint64 ,addressof
from ctypes import c_uint8, c_uint16, c_uint32, Structure, Union ,string_at
from ctypes.wintypes import  BYTE, WORD, DWORD
import ctypes
from tnstruct import *
import sys
import time

le_uint8_t=ctypes.c_uint8
le_uint16_t=ctypes.c_uint16
le_uint32_t=ctypes.c_uint32
uint8_t=ctypes.c_uint8
uint16_t=ctypes.c_uint16
uint32_t=ctypes.c_uint32




def struct2string(cbw):
    sizeof_cbw=sizeof(cbw)
    return string_at(addressof(cbw),sizeof_cbw)

def is_structure(obj):
    """
    Parameters
    ----------
    obj : любой тип данных

    Returns  
    -------
        int :
            2 если obj - класса  наследованный от  Structure, \n
            1 если obj - экземпляр класса  наследованного от  Structure,\n
            0 в остальных случаях
    """

    if hasattr(obj,"__bases__"):
        base=obj.__bases__
        if len(base)>0:
            if obj.__bases__.count(Structure):
                return 2   
    elif hasattr(obj.__class__,"__bases__"):
        base=obj.__class__.__bases__
        if len(base)>0:
            if obj.__class__.__bases__.count(Structure):
                return 1        
    
    return 0


def struct2txt(obj,N=0,txt=""):
    #len(obj)
    #print obj._fields_

    if is_structure(obj):
        for i in obj._fields_:
            txt+= " "*N+i[0]+"\n"
            
            #getattr(inst,i[0])
            attr=obj.__getattribute__(i[0])
            txt=struct2txt(attr,N+1,txt)
            #print is_structure(inst.__dict__[i[0]])
            #print inst.__dict__[i[0]]
    elif hasattr(obj,"__len__"):
        index=0
        for attr in obj:
            txt+= " "*N+"["+str(index)+"] "+"\n"
            txt=struct2txt(attr,N+1,txt)
            index+=1
    else :
        txt=txt[0:-2]
        num=30-(len(txt[txt.rfind("\n"):])-N)
        txt+=" "*num+hex(obj)+"\n"
        return txt 
    return txt

'''
def print_struct(obj,N=0):
    #len(obj)
    #print obj._fields_

    if is_structure(obj):
        for i in obj._fields_:
            print " "*N+i[0] #+"{\n"
            
            #getattr(inst,i[0])
            attr=obj.__getattribute__(i[0])
            print_struct(attr,N+1)
            #print is_structure(inst.__dict__[i[0]])
            #print inst.__dict__[i[0]]
    elif hasattr(obj,"__len__"):
        for attr in obj:
            print_struct(attr,N+1)
    else :
        print " "*N,obj
'''

def print_struct(obj,N=0):
    return struct2txt(obj,N)
