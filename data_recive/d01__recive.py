# -*- coding: utf-8 -*-

import ctypes as ct;
import socket
import threading
import tnstruct
import time

uint8_t = ct.c_uint8
uint16_t = ct.c_uint16
uint32_t = ct.c_uint32

int16_t = ct.c_int16
int32_t = ct.c_int32


VALUE_BYTE_SIZE=2


def toStruct(struct,buff):
    struct.from_buffer_copy(buff[0:ct.sizeof(struct)])


class Ethernet(threading.Thread):
    def __init__(self,indexArray,src=( '192.168.0.101', 13330),NumberOfModule=3,totalN=2,parent=None):

        self.channelCount=16*6
        class Header(ct.Structure):
            _fields_ = [('len', uint16_t),
                        ('time', uint32_t),
                        ('size', int16_t * totalN),
                        ('summ', uint16_t)]
            _pack_ = 1

        self.Header=Header
        self.Header_size = ct.sizeof(Header)

        threading.Thread.__init__(self)
        self.daemon = True

        self.NumberOfModule =NumberOfModule
        self.data    = [list() for i in xrange(self.channelCount)]
        self.index   = 0
        self.enable  = True
        self.pause  =  True
        self.waitSecondPoint = False

        self.parent=parent
        self.data_IP, self.data_port = src
        self.indexArray=indexArray


    def updateDataCount(self,indexArray):
        self.indexArray=indexArray


    def run(self):
        def secondStart(timeVar):
            return (timeVar%1024)==0

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        s.bind((socket.gethostbyname(socket.gethostname()), self.data_port))
        self.so=s
        state_counter=0

        while self.enable:
            while self.pause:
                self.data = [list() for i in xrange(self.channelCount)]
                self.waitSecondPoint=True

            IP = ""
            while IP != self.data_IP:
                data, IP = s.recvfrom(1024*4)
                IP = IP[0]
                if self.enable==False:
                    s.close()
                    return



            packetHeader = self.Header.from_buffer_copy(data[0:self.Header_size])
            modules_num=packetHeader.len & 0xf
            data_offset =sum(packetHeader.size[0:self.NumberOfModule])+self.Header_size
            data_length =packetHeader.size[self.NumberOfModule]
            data_end    = data_offset+data_length
            array_length=data_length/VALUE_BYTE_SIZE

            if secondStart(packetHeader.time):
                state_counter = 0
                self.waitSecondPoint=False
                if self.parent!=None:
                    self.parent.update(self.data)


            if data_length>0 and not self.waitSecondPoint:
                data = (ct.c_int16 * array_length).from_buffer_copy(data[data_offset:data_end])[0:array_length]
                #print data_offset, data_length, modules_num
                for i in data:
                    index=self.indexArray[state_counter]
                    self.data[index].append(i)
                    state_counter=(state_counter+1)%len(self.indexArray)


        s.close()




if __name__ == "__main__":
    ethernet = Ethernet(( '192.168.0.101', 13330),NumberOfModule=2,totalN=3)
    ethernet.start()
    while 1:
        pass







