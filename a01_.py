# -*- coding: utf-8 -*-
"""
This example module shows various types of documentation available for use
with pydoc.  To generate HTML documentation for this module issue the
command:

    pydoc -w foo

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


def read_samples(module,input_val=0,samples=512*16*64):
    module.set_sample_nums(samples)
    out=True
    while out:
        val=module.read_sample_nums()[0]
        time.sleep(0.2)
        f=uint32_t.from_buffer_copy(val[4:8]).value
        #print f,'\n'
        out=f<samples
        

    val=module.read_samples()[0]
    arr=[]
    for j in xrange(32):
        E=float(tr(val,j*4  ).value)/float(f)-float(input_val)
        EE=tr(val,j*4  ).value
        
        #print E 
        S=abs(tr(val,j*4+2 ).value)#-EE*EE
        print E, float(S)/f -E**2
        arr.append(E)
    print'\n'
    return sum(arr)/32

def print_calibration_value_from_ROM(module):
    print uint16_t.from_buffer_copy(module.read_calibration(0,2)[0][0:2]).value
    
def calibration(module,input_val=10000*2):
        samples=512*16*16
        gain=(3<<13)
        last_gain=(3<<13)
        shf=12
        module.set_gain(uint16_t(gain))
        while shf>0:
        
            module.set_sample_nums(samples)
            out=True
            while out:
                val=module.read_sample_nums()[0]
                time.sleep(0.2)
                f=uint32_t.from_buffer_copy(val[4:8]).value
                #print f,'\n'
                out=f<samples
            

            



            val=module.read_samples()[0]
            arr=[]
            for j in xrange(32):
                E=float(tr(val,j*4  ).value)/float(f)-float(input_val)
                print E
                S=long (tr(val,j*4+2 ).value)
                arr.append(E)
            print'\n'
            print sum(arr)/32
            
            last_gain=gain
            if sum(arr)/32>0:
                gain+=1<<shf
            else :
                gain-=1<<shf
            print bin(gain)
            print gain
            shf-=1
            
            module.set_gain(uint16_t(gain))
        Nun=40
        while Nun>0:
            time.sleep(0.2)
            
            Nun-=1
        print gain
        #st=struct2string(uint16_t(last_gain))
        #module.write_calibration(0,2,st) 

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
        
        #OLD st=struct2string(uint16_t(32728))
        st=struct2string(uint16_t(32702))
        #st=struct2string(uint16_t((1<<16)-1))
        #module.write_calibration(0,2,st)
        time.sleep(2.5)
        #print_calibration_value_from_ROM(module)
        #module.set_gain(uint16_t(0))
        #calibration(module,10000*2.5)
        print struct2txt(tsk)
        #print read_samples(module)

  









