# -*- coding: utf-8 -*-
from tnbalancelib import *
from pof2bin import *

import sys

import argparse
"""
CD=CONNECTED_DEVICE()
print CD
serial=0
addres=('255.255.255.255', 4880)
d,error_code= CONNECTED_DEVICE().send_request(PING)
# print d[('192.168.0.7', 4880)].proto.lun ,7
"""
#  cmd_write --addr 192.168.0.7 --lun 7 -N 0 -I WC01 -V 1 -S 1
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--addr'  ,default='192.168.0.0' ,help=u'адрес накопителя в составе сети',)
parser.add_argument('-f', '--file'  , help=u'файл инициализации "pof/sof"')
parser.add_argument('-I', '--ID'    , help=u'ID модуля')
parser.add_argument('-V', '--VER'   , help=u'версия модуля')
parser.add_argument('-S', '--SER'   , help=u'новый серийный номер модуля')
parser.add_argument('-L', '--lun'   , help=u'логический номер накопителя в составе сети',type=int)
parser.add_argument('-N', '--Num'   , help=u'номер иодуля в составе накопителя',type=int)
parser.add_argument('-l', '--log'   , help=u'')
parser.add_argument('-C', '--CSW'   , help=u'')
h=parser.parse_args()






def show_progress(value,max):
    #sys.stderr.write('%d\r' % value)
    mi=100/(max-1)
    #sys.stderr.write("\r"+u"■"*value+u" "*(max-value)+u'%d'% (value*mi)+'%')
    sys.stderr.write("\r" + u'%d' % (value * mi) )

def run_progress():
    for i in xrange(26):
        time.sleep(0.2)
        show_progress(i,26)

class module_():
    def __init__(self,mod,list ):
        ID, VER, SER,Name = list
        self.mod=mod
        self.ID=ID
        self.VER=VER
        self.SER=SER
        self.Name=Name

    def update(self):

        #print self.ID.text()

        def readk(num):
            num = str(num)
            #print num[0:2]
            if num[0:2]=="0x" :
                return int(num,16)
            elif num.find(".")>-1:
                num=num.split(".")
                return (int(num[0])<<8)|int(num[1])
            else :
                return int(num)
        #print int(self.ID.text())
        if len(self.ID)!=4:
            return

        self.write_ID_VER(str(self.ID),readk(self.VER),readk(self.SER))

    def update_sofwhere(self):
        data=read_pof(self.Name,"pofs\\"+self.ID+"\\")
        #print self.ID.text()

        self.write_sofwhere(data)
        #self.write_ID_VER(str(self.ID.text()),readk(self.VER.text()),readk(self.SER.text()))



    def write_ID_VER(self,ID,VER,SER):

        module=self.mod
        module.wait_status()
        s, error = module.status_command_eeprom()

        s = Flash_HEADER.from_buffer_copy(s[4:16])
        #print_struct(s)
        #print "read"
        dat = module.read_page( s.sys_id_addr, s.page_size)
        addres =s.sys_id_addr- ((s.sys_id_addr >> s.page_size) << s.page_size)
        if type(ID)!=str:
            #print "error1"
            return
        elif len(ID)!=4 :
            #print "error2"
            return
        #print "redact:"
        dat=dat[0:addres]+ID+struct2string(uint16_t(VER))+struct2string(uint16_t(SER))+dat[addres+8:]
        module.wait_status()
        #print "erase:"
        module.status_command_eeprom( (s.sys_id_addr >> s.page_size) << s.page_size)
        #module.status_command_eeprom(0)
        module.wait_status()
        #print "write:"
        module.write_page( s.sys_id_addr, s.page_size, dat,std=True )
        #module.write_page(s.sys_id_addr, s.page_size, dat, self.progress)
        module.wait_status()
        print "complete:"

    def write_sofwhere(self,data):
        module=self.mod
        module.wait_status()
        s, error = module.status_command_eeprom()

        s = Flash_HEADER.from_buffer_copy(s[4:16])
        #print_struct(s)
        #print "read:"
        print
        page_size=1<<s.page_size
        N_pages=len(data)/page_size+(len(data)%page_size!=0)
        page_addr=s.prog_addr
        #self.progress.setMaximum(N_pages - 1)
        for i in xrange(N_pages):
            dt=data[page_size*i:page_size*(1+i)]
            if len(dt)!=page_size:
                dt=dt+chr(0)*(page_size-len(dt))
            #print "erase:"
            module.status_command_eeprom(page_size*i)
            module.wait_status()
            #print "write:"
            module.write_page( page_size*i, s.page_size, dt )
            #print "wait_status:"
            module.wait_status()
            #self.progress.setValue(i)
        print "complete:"
        self.update()



if type(h.lun)==int and type(h.addr)==str:
    i=CONNECTED_DEVICE(lun=h.lun, address=(h.addr,4880))
    i.get_modules()
    if type(h.log)!=type(None):
        for j in i.modules :
            print u"\n\tномер модуля", j
            print unicode(i.modules[j])

    if type(h.Num)==int:
        m=module_( i.modules[h.Num],(h.ID, h.VER, h.SER,h.file))
        m.update()
else:
    print "error:"
exit()