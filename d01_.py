# -*- coding: utf-8 -*-
"""
git remote add origin https://savvakonst:ansskata18@github.com/savvakonst/ksd_lan.git


"""
__docformat__ = "restructuredtext"




from tnbalancelib import *
from qt.d01_ import *
from data_recive.d01__recive import *




d=None
count =0
run_autodetection=True


while (d is None ) and count<20 and run_autodetection:
    count+=1
    CD=CONNECTED_DEVICE()
    print CD
    d,error_code= CONNECTED_DEVICE().send_request(PING)
    print d

if count>0:
    exit

#for k,csw in d.items() :print "csw",struct2txt(csw) ;print "address",k
if run_autodetection:
    devices = [CONNECTED_DEVICE(csw=csw, address=k) for k, csw in d.items()]
else:
    devices = [CONNECTED_DEVICE(csw=4   ,address=('192.168.0.4', 4880))]
kk=0

id_ = 0
count = 0
for i in devices:
    i.get_modules()
    #print i.saCtl[0]

    s=i.get_main_module(1024)
    #print ":".join("{:03d}".format(ord(c)) for c in s[0:712])
    #print ":".join("{:03d}".format(ord(c)) for c in s[142:144])
    data_ip   = ".".join("{:d}".format(ord(c)) for c in s[160:164])
    data_port = int("".join("{:02x}".format(ord(c)) for c in s[142:144]),16)

    src=(data_ip,data_port)
    print src
    D01__module_num=0
    activModuleCount=2
    for j in i.modules:
        print j
        module = i.modules[j]
        txt_module_id =struct2string_(uint32_t(module.dwID))

        tsk = module.get_module_task()  # get task

        if txt_module_id=="D01_":
            D01__module=module
            D01__module_num=activModuleCount
        activModuleCount += tsk.smt.wFlag

    if D01__module_num>0:
        print D01__module_num,activModuleCount
        create_widget(D01__module , src, D01__module_num, activModuleCount)