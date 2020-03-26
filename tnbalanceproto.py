# -*- coding: utf-8 -*-
"""

:class:`tnbalanceproto.MODULE_IDENT` 


Управляющие структуры
========================

:class:`tnbalanceproto.PROTO_HEADER` 

:class:`tnbalanceproto.CxW_PARAMS` 

:class:`tnbalanceproto.CBW` 

:class:`tnbalanceproto.CSW` 

:class:`tnbalanceproto.DBW` 

:class:`tnbalanceproto.DSW` 

╨Ю╨┐╨╕╤Б╨░╨╜╨╕╨╡
========================
"""




from ctypes import POINTER,sizeof, c_void_p, c_int, c_bool ,c_uint64 ,addressof
from ctypes import c_uint8, c_uint16, c_uint32, Structure, Union ,string_at
from ctypes.wintypes import  BYTE, WORD, DWORD
import ctypes
from tnstruct import *
import sys
import time
from tncommon import *



#MIB_GET_ID = 0x41

GET_ID    =0x41
GET_TASK  =0x42
SET_TASK  =0x02
GET_STATUS=0x40

GET_EX_COMMAND_FROM_PC =0x09
GET_EX_DATA_FROM_PC    =0x08
GET_EX_DATA_TO_PC      =0x48

le_uint8_t=ctypes.c_uint8
le_uint16_t=ctypes.c_uint16
le_uint32_t=ctypes.c_uint32
uint8_t=ctypes.c_uint8
uint16_t=ctypes.c_uint16
uint32_t=ctypes.c_uint32

MAX_DEVICES_NUMBER  =  3
MAX_SLOTS_NUMBER    =  10

CBW_SIG=0x4243
CSW_SIG=0x5343
DBW_SIG=0x4244
DSW_SIG=0x5344


NO_DATA=0
PC_TH3=0    #PC->T╨Э3
TH3_PC=0x80  #T╨Э3->PC


TASK_MEMORY_REQUEST 	= 0x01
RW_EXCHANGE_BUFFER      = 0x10
MODULE_REQUEST_         = 0x11
PING = 0


MAX_INPUT_BUFFER_SIZE 	= 65536
COMMAND_BLOCK_WRAPPER_SIGNATURE = 0x4243
LUN_ANY = 0



def show_progress(value,max):
    #sys.stderr.write('%d\r' % value)
    mi=100/(max-1)
    sys.stderr.write(u"■"*value+u" "*(max-value)+u'%d'% (value*mi)+'%\r')

def run_progress():
    for i in xrange(26):
        show_progress(i,26)


class Flash_HEADER(Structure):
    _fields_=[  ('page_size',uint32_t),
                ('pages',uint16_t),
                ('prog_addr',uint16_t),
                ('sys_id_addr',uint32_t)]
    _pack_=1


def MODULE_REQUEST(request,mibaddr,lenght):
    cxw = CxW_PARAMS()
    cxw.u32[0] = long(request) << 24 | int(mibaddr) << 16 | lenght
    return cxw

def EX_MODULE_REQUEST(request,param=[]):
    cxw = CxW_PARAMS()
    cxw.u32[0]=long(request)
    k=1
    for i in param:
        cxw.u32[k]=long(i)
        k+=1
    return cxw

def struct2string_(cbw):
    sizeof_cbw=sizeof(cbw)
    return string_at(addressof(cbw),sizeof_cbw)





class MODULE_IDENT(Structure):
    """
    Attributes:
        u32ID (ctypes.c_uint32)
            
    Attributes:
        u16Version (ctypes.c_uint16) 
    
    Attributes:
        u16SerialNumber (ctypes.c_uint16)
        
    """
    _fields_=[('dwID',c_uint32),
              ('wVersion',c_uint16),
              ('wSerialNumber',c_uint16)]

    def __init__(self,**kwargs):
        Structure.__init__(self,**kwargs)
        self.device=None
        self.number == -1
    def __str__(self):
        s=u"\tИдентификатор модуля="+unicode(str(struct2string_(uint32_t(self.dwID))))
        s+=u"\n\tВерсия="+unicode(hex(uint16_t(self.wVersion).value))
        s+=u"\n\tСерийный номер"+unicode(hex(uint16_t(self.wSerialNumber).value))
        return s

    def get_module_task(self):
        if self.number == -1:
            raise module_error("error")
        #print type(self.device)
        return self.device.get_module_task(self.number)

    def set_module_task(self,task_data):
        status =self.device.wr_exchange_buffer(task_data)
        if status != 0:
            return None,status
        if type(task_data)==str :
            sizeof_data=len(task_data)
        else :
            sizeof_data = sizeof(task_data)

        cxw = MODULE_REQUEST(SET_TASK, self.number, sizeof_data)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status!=0:
            return None,status

        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        # g_ExBuffer - буфер данных 1024 байта (0x48 отправить данные компьютеру ) (0x08 принять данные с компьютера)
        # g_ExCommand - буфер доп_команд 32 байта (0x09 считать доп команду)
        return s, error_code



    def get_module_id(self):
        if self.number == -1:
            raise module_error("error")
        return self.device.get_module_id(self.number)


    def send_ex_command_without_data(self,command):
        status=self.device.wr_exchange_buffer(command)
        if status!=0:
            return None,status

        cxw = MODULE_REQUEST(GET_EX_COMMAND_FROM_PC, self.number, 32)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        # "status" ,s.status
        if status != 0:
            return None,status
        return s , 0




    def send_ex_command_with_data(self,command,data):
        status =self.device.wr_exchange_buffer(data)
        if status != 0:
            return None,status
        if type(data)==str :
            sizeof_data=len(data)
        else :
            sizeof_data = sizeof(data)
        cxw = MODULE_REQUEST(GET_EX_DATA_FROM_PC, self.number, sizeof_data)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status!=0:
            return None,status

        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        # g_ExBuffer - буфер данных 1024 байта (0x48 отправить данные компьютеру ) (0x08 принять данные с компьютера)
        # g_ExCommand - буфер доп_команд 32 байта (0x09 считать доп команду)
        return self.send_ex_command_without_data(command)


    def get_status(self):
        cxw = MODULE_REQUEST(GET_STATUS, self.number, 8)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            #print status
            return None,status

        return self.device.rd_exchange_buffer(data=MODULE_STATUS)


    def write_calibration(self,addres=0,offset=4,data=''):
        addres=addres
        ex_r=EX_MODULE_REQUEST(0x01,[addres,offset,]) # 0x01 write data
        csw, status =self.send_ex_command_with_data(ex_r,data)
        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)


    def read_calibration(self,addres=0,offset=4):
        addres=addres
        ex_r=EX_MODULE_REQUEST(0x00,[addres,offset,]) # 0x00 read data
        csw,status=self.send_ex_command_without_data(ex_r)

        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)

    def write_eeprom(self,addres=0,data=''):
        if is_structure(data) or hasattr(data,"__sizeof__"):
            data=struct2string(data)
        addres=addres
        ex_r=EX_MODULE_REQUEST(0x22,[addres]) # 0x23 read data
        csw, status =self.send_ex_command_with_data(ex_r,data)
        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)


    def read_eeprom(self,addres=0):
        addres=addres
        ex_r=EX_MODULE_REQUEST(0x23,[addres,]) # 0x23 read data
        csw,status=self.send_ex_command_without_data(ex_r)

        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)


    def set_gain(self,data=''):
        if is_structure(data)or hasattr(data,"__sizeof__"):
            data=str(struct2string_(data))
            
        ex_r=EX_MODULE_REQUEST(0x06,[0,]) # 0x06 set gain
        csw, status =self.send_ex_command_with_data(ex_r,data)
        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)


    def set_sample_nums(self,nums=128):
        data=b'aaaa'
            
        ex_r=EX_MODULE_REQUEST(0x10,[nums,]) # 0x10 set gain
        csw, status =self.send_ex_command_with_data(ex_r,data)
        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)

    def read_sample_nums(self,addres=0):
        ex_r=EX_MODULE_REQUEST(0x11,[0,]) # 0x11 read sample nums
        csw,status=self.send_ex_command_without_data(ex_r)

        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)



    def set_custom_params(self,command=0x0,param=[0,]):
        data=b'aaaa'
            
        ex_r=EX_MODULE_REQUEST(command,param) # 0x10 set gain
        csw, status =self.send_ex_command_with_data(ex_r,data)
        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)

    def get_custom_params(self,command=0x0,param=[0,]):
        ex_r=EX_MODULE_REQUEST(command,param) # 0x11 read sample nums
        csw,status=self.send_ex_command_without_data(ex_r)

        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)



    def read_samples(self,addres=0):
        ex_r=EX_MODULE_REQUEST(0x04,[0,]) # 0x04 read samples
        csw,status=self.send_ex_command_without_data(ex_r)

        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        if error_code != 0:
            return None,error_code

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=1024
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        return self.device.rd_exchange_buffer(N=data_len)


    def status_command_eeprom(self,control=0xffffffff):
        ex_r=EX_MODULE_REQUEST(0x24,[control]) # 0x23 read data
        csw,status=self.send_ex_command_without_data(ex_r)

        if status != 0:
            return None,status
        #print "sd"
        s, error_code=self.get_status()
        #print hex(s.dwStatus)
        if error_code != 0  :
            return None,error_code

        if  s.dwStatus!=0 :
            return None,  s.dwStatus

        #print "Command=",s.dwCommand ," , Status=",s.dwStatus

        data_len=32
        cxw = MODULE_REQUEST(GET_EX_DATA_TO_PC, self.number, data_len)
        s, status = self.device.send_request(MODULE_REQUEST_, params=cxw)
        if status != 0:
            return None,status

        s,error_code=self.device.rd_exchange_buffer(N=data_len)
        #s=uint32_t.from_buffer_copy( s[0:4])
        return s,error_code


    def wait_status(self):
        s = 1
        k=0
        while s :
            s, error = self.status_command_eeprom()

            k+=1
            if k%10==9:
                None
                #time.sleep(0.5)
                #print "status wait"

            if error > 0:
                s = 1
            else:
                ss = Flash_HEADER.from_buffer_copy(s[4:16])
                s=uint32_t.from_buffer_copy(s[0:4]).value

                #print bin(s),ss.pages, error, "error wr"
                s=s&3
        #print bin(s), error, "error wr"
        #print "s"


    def read_page(self,addres,page_size):
        dt=""
        addres=(addres>>page_size)<<page_size

        for i in xrange((1<<page_size)/1024):
            error=1
            while error:
                s,error=self.read_eeprom(addres + i * 1024)
            dt+=s
        return dt

    def write_page(self,addres,page_size,data,progress=None,std=False):

        addres=(addres>>page_size)<<page_size
        bool_ = True
        while bool_:
            max_=(1 << page_size) / 1024
            if type(progress) != type(None):
                progress.setMaximum(max_-1)
            for i in xrange((1<<page_size)/1024):
                s,error=self.write_eeprom(addres + i * 1024,data[i*1024:(i+1)*1024])
                if type(progress) != type(None):
                    progress.setValue(i)
                if std:
                    print 'progress:' ,int(i*100.0/max_)
                self.wait_status()

            s=self.read_page(addres,page_size)
            bool_=s!=data
        if std:
            print 'progress:', 100

class PROTO_HEADER(Structure):
    """
    Attributes:
        signature (ctypes.c_uint16)
            Идентификатор управляющей структуры
    
    Attributes:
        lun (ctypes.c_uint16)
            логический номер накопителя в составе сети,
            равен серийному номеру или 0, если адресуются все накопители

    
    Attributes:
        reqid (ctypes.c_uint16)
            уникальный идентификатор запроса, все последующие
            пакеты CS/DB/DS содержат копию этого поля из CB,
            для однозначной идентификации пакетов в составе
            одной транзакции


    Attributes:
        seqcnt (ctypes.c_uint16)
            инкрементальный счётчик в пределах одной
            транзакции увеличивается на единицу с каждым
            переданным/принятым управляющим пакетом;
            предназначен для контроля целостности транзакции
            (отсутствие потери пакетов). То есть,
            если CBW устанавливает seqcnt = 0,
            то ответный CS будет содержать seqcnt = 1,
            если затем следует DB seqcnt = 2,
            ответный DSW seqcnt = 3 и т.д.
    
    """
    _fields_=[('signature',le_uint16_t),
              ('lun',le_uint16_t),
              ('reqid',le_uint16_t),
              ('seqcnt',le_uint16_t)]

    _pack_=1

class CxW_PARAMS(Structure):
    """
    Attributes:
        proto (ctypes.c_uint32*12)
        
    """
    _fields_=[('u32',le_uint32_t*12)] 
    


class CBW(Structure):
    """
    Attributes:
        proto (tnbalanceproto.PROTO_HEADER)
            proto.CB = 0x4243
            
    Attributes: 
        dataTransferLength (ctypes.c_uint32)
            размер (в байтах)
            предполагаемый для передачи или приёма устройством управления

    
    Attributes:
        requestCode (ctypes.c_uint8)
            идентификатор команды [0…255]

    Attributes:
        flags (ctypes.c_uint8)
            битовая маска флагов команды
            7 бит- направление передачи данных,
            ‘0’ – PC->TН3, ‘1’ – TН3->PC
            6..0- зарезервированы
            Если предполагаемый размер блока данных равен 0 значение бита 7 не имеет значения и игнорируется

    
    Attributes:
        reserved (ctypes.c_uint16)
            зарезервировано, значение игнорируется

    Attributes:
        params (CxW_PARAMS)
            Параметры команды, значение
            этих полей зависит от идентификатора команды requestCode

    """
    _fields_=[('proto',PROTO_HEADER),
              ('dataTransferLength',le_uint32_t),
              ('requestCode',le_uint8_t),
              ('flags',le_uint8_t),
              ('reserved',le_uint16_t),
              ('params',CxW_PARAMS)]
    

class CSW(Structure):
    """
    Attributes:
        proto (tnbalanceproto.PROTO_HEADER)
        proto.CB = 0x5343
                
    Attributes: 
        dataTransferLength (ctypes.c_uint32)
            точный размер (в байтах) для передачи или приёма накопителем, всегда меньше
            или равен CB.length Например, если устройство управления запросило для передачи
            от накопителя 4000 байт данных в CB, однако накопитель имеет только 2000 байт для
            выполнения запроса, в CSW.dataTransferLength будет возвращено 2000 и устройство управления
            должно соответствующим образом cформировать запросы DB/DS


        
    Attributes:
        status (ctypes.c_uint32)
            статус выполнения команды
            0 – команда выполнена успешно
            не 0– код ошибки
            В случае ненулевого статуса стадия передачи данных DB/DS
            не инициируется накопителем
       
    Attributes:
        params (CxW_PARAMS)

            Дополнительные данные статуса
            выполнения команды

    """
    _fields_=[('proto',PROTO_HEADER),
              ('dataTransferLength',le_uint32_t),
              ('status',le_uint32_t),
              ('params',CxW_PARAMS)]
    _pack_=1

class DBW(Structure):
    """
    
        Attributes:
            proto (tnbalanceproto.PROTO_HEADER)
                proto.CB = 0x4244
                
        Attributes: 
            dataTransferLength (ctypes.c_uint32)
                размер (в байтах) данных содержащихся в текущем пакете <= 1024
        
        Attributes:
            status (ctypes.c_uint32)
                0 – блок данных валиден, продолжаем обмен
                не 0 – код ошибки, прекращаем обмен
       
        Attributes:
            params (CxW_PARAMS)
                Зарезервировано


    """
    _fields_=[('proto',PROTO_HEADER),
              ('dataTransferLength',le_uint32_t),
              ('status',le_uint32_t),
              ('params',le_uint32_t*4)]

class DSW(Structure):
    """
    
        Attributes:
            proto (tnbalanceproto.PROTO_HEADER)
                proto.CB = 0x5344
                
        Attributes: 
            dataTransferLength (ctypes.c_uint32)
                Резерв

        Attributes:
            status (ctypes.c_uint32)
                0 – блок данных валиден, продолжаем обмен
                не 0 – код ошибки, прекращаем обмен

        Attributes:
            params (CxW_PARAMS)
                Зарезервировано


    """
    _fields_=[('proto',PROTO_HEADER),
              ('dataTransferLength',le_uint32_t),
              ('status',le_uint32_t),
              ('params',le_uint32_t*4)]

class EX_COMMAND(Structure):
    _fields_=[('command',le_uint32_t),
              ('data',le_uint32_t*7)]


    
#class Uy(Union):
#    _fields_ = [("csw", CSW),
#                ("str", ctypes.c_char * sizeof(CSW))]
#class Uy(Union):
#    _fields_ = [("csw", CSW),
#                ("strt", ctypes.c_char * 64)]






sizeof_cbw=sizeof(CBW)        
sizeof_csw=sizeof(CSW)    
sizeof_dbw=sizeof(DBW)        
sizeof_dsw=sizeof(DSW)

LP_PROTO_HEADER=POINTER(PROTO_HEADER)
LP_CxW_PARAMS=POINTER(CxW_PARAMS)
LP_CBW=POINTER(CBW)
LP_CSW=POINTER(CSW)
