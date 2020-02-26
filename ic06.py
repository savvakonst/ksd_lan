# -*- coding: utf-8 -*-
"""
git remote add origin https://savvakonst:ansskata18@github.com/savvakonst/ksd_lan.git


"""
__docformat__ = "restructuredtext"




from tnbalancelib import *







CD=CONNECTED_DEVICE()
d,error_code= CONNECTED_DEVICE().send_request(PING)


devices=[CONNECTED_DEVICE(csw=csw,address=k) for k,csw in d.items() ]
kk=0



from functools import partial
import sys
import time


#List_of_dirs= [x[0].split("\\")[-1] for x in os.walk("POFS")]

def tr(x,i):
    return ctypes.c_uint64.from_buffer_copy(x[0+i*4:8+i*4])


class MDIO_AD(Structure):
    _fields_ = [("DEVAD", uint8_t),
                ("PRTAD", uint8_t),
                ("REGAD", uint16_t)]



def setup0x20_reg(module,MDIO_ACCESS):
    module.set_custom_params(0x6,[MDIO_ACCESS,])


def setup0x21_reg(module,MDIO_DEVAD,MDIO_PRTAD,MDIO_REGAD):
    mdio_ad=MDIO_AD()
    mdio_ad.DEVAD=MDIO_DEVAD
    mdio_ad.PRTAD=MDIO_PRTAD
    mdio_ad.REGAD=MDIO_REGAD
    s=c_uint32()
    ctypes.memmove(ctypes.pointer(s),ctypes.pointer(mdio_ad),4)
    module.set_custom_params(0x7,[s.value,])
    
def get0x20_reg(module):
    c=module.get_custom_params(0x10)    
    mdio=uint32_t.from_buffer_copy(c[0:4])
    print struct2string_(mdio)


def get0x21_reg(module):
    c=module.get_custom_params(0x11)    
    mdio=MDIO_AD.from_buffer_copy(c[0:4])
    print struct2string_(mdio)
    



id_=0
count=0
for i in devices:
    m=i.get_modules()
    print i.saCtl[0]
    id2_=0
    
    for j in i.modules:

        print j
        module=i.modules[j]
        print struct2string_(uint32_t(module.dwID))

        tsk=module.get_module_task()
        

        st=struct2string(uint16_t(32702))

        time.sleep(2.5)

        print struct2txt(tsk)
        #print read_samples(module)

  









