# -*- coding: utf-8 -*-
"""

Функции
========================

:func:`tnbalancelib.is_structure` \n
:func:`tnbalancelib.send_request` \n
:func:`tnbalancelib.wr_exchange_buffer` \n
:func:`tnbalancelib.rd_exchange_buffer` \n

Классы
========================

:func:`tnbalancelib.is_structure` \n
:func:`tnbalancelib.send_request` \n
:func:`tnbalancelib.wr_exchange_buffer` \n
:func:`tnbalancelib.rd_exchange_buffer` \n


Описание
========================

"""
__docformat__ = "restructuredtext"
#from ctypes import POINTER, Structure,Union,sizeof, c_void_p, c_int, c_bool ,c_uint64
#from ctypes import string_at,addressof,c_uint8, c_uint16, c_uint32
#from ctypes.wintypes import  BYTE, WORD, DWORD
#import ctypes as ct
from tncommon import *
from tnbalanceproto import *


import socket as so
import inspect


# iStatus = iorequest_sync(h, request::READ_TASK_MEMORY, 0x80 / * hostread * /, p   , uSize, & uTres       , & cbw_params, NULL, TIMEOUT);   ReadTaskMemory
# iStatus = iorequest_sync(h, request::MIB_EXT_EXECUTE , 0x00 / *          * /, NULL, 0    , & uTransferred, & cbw_params, NULL, TIMEOUT);   MIB_Exec
# iStatus = iorequest_sync(h, request::MIB_EXT_RWBUFFER, 0x80 / * hostread * /, data, iSize, & uTransferred, NULL        , NULL, TIMEOUT);   MIB_ReadBuffer


def send_request(mod,request,request_type=NO_DATA,params=CxW_PARAMS(),data_len=0):
    """
    Parameters
    ----------
    mod : tnbalanceproto.EX_COMMAND
    N : int
    data : экземпляр класса наследованного от  Structure ,str

    Returns  
    -------
        int :
            0 - транзакция успешна , не 0 -код ошибки

    """
    error_code=None
    mod.seqcnt=0
    mod.reqid+=1
    seqcnt=0
    
    sizeof_DBW=sizeof(DBW)    
    header=PROTO_HEADER(CBW_SIG,mod.wLun,mod.reqid,seqcnt)

    temp=request_type & PC_TH3

    cbw=CBW(header,data_len,request,request_type|PC_TH3,params=params)
    string = struct2string(cbw)
    mod.so.sendto(string, 0,  mod.saCtl)
    
    if mod.wLun==0:
        c=0
        csw=dict()
        while c<MAX_DEVICES_NUMBER:
            try:
                str_, k = mod.so.recvfrom(sizeof_cbw)
                csw.update({k:CSW.from_buffer_copy(str_)})
                seqcnt += 1
            except:
                pass
            c+=1
        if seqcnt==0:
            return error_code, inspect.currentframe().f_lineno

    else:
        try :
            str_,k=mod.so.recvfrom(sizeof_cbw)
            csw = CSW.from_buffer_copy(str_)
            seqcnt += 1
        except:
            return error_code,inspect.currentframe().f_lineno

        if not( (csw.status==0 )& (csw.proto.reqid ==mod.reqid) & (csw.proto.seqcnt==seqcnt) ):
            #print  struct2txt(csw)
            return error_code ,inspect.currentframe().f_lineno
    return csw ,0
    

def wr_exchange_buffer(mod,data):
    """
    Parameters
    ----------
    mod : tnbalanceproto.EX_COMMAND
    data : экземпляр класса наследованного от  Structure ,str

    Returns  
    -------
        int :
            0 - транзакция успешна , не 0 -код ошибки

    """
    error_code=1
    seqcnt=0
    mod.reqid+=1
    if type(data)==str:
        data_len=len(data)
    elif is_structure(data):
        data=struct2string(data)
        data_len=len(data)
    elif type(data)!=str:
        return inspect.currentframe().f_lineno

    
    header=PROTO_HEADER(CBW_SIG,mod.wLun,mod.reqid,seqcnt)
    cbw=CBW(header,data_len,RW_EXCHANGE_BUFFER,PC_TH3)
    string = struct2string(cbw)
    mod.so.sendto(string, 0,  mod.saCtl)
    try :
        str_,k=mod.so.recvfrom(sizeof_cbw)
    except:
        return inspect.currentframe().f_lineno
    
    csw=CSW.from_buffer_copy(str_)
    seqcnt+=1
    if ((csw.status==0) & (csw.proto.reqid ==mod.reqid) & (csw.proto.seqcnt==seqcnt) ):
        seqcnt+=1
        header=PROTO_HEADER(DBW_SIG,mod.wLun,mod.reqid,seqcnt)
        dbw=DBW(header,data_len,0)
        string=struct2string(dbw)+data
        mod.so.sendto(string, 0,  mod.saCtl)
    else :
        return inspect.currentframe().f_lineno
    
    try :
        str_,k=mod.so.recvfrom(sizeof_dsw)
        dsw=DSW.from_buffer_copy(str_)
        seqcnt+=1
    except:
        return inspect.currentframe().f_lineno
      
    if ((dsw.status==0) & (dsw.proto.reqid ==mod.reqid) & (dsw.proto.seqcnt==seqcnt) ):
        return 0
    return inspect.currentframe().f_lineno


def rd_exchange_buffer(mod,data=None,N=0):
    """
    Parameters
    ----------
        mod : tnbalanceproto.EX_COMMAND
        data : класс наследованный от  Structure
        N : int
            размер принимаемых данных , если параметр  data-определен то по умолчанию N=sizeof(data) .
            if N>sizeof(data): N=N  else N=sizeof(data)


    Returns 
    -------
        str/Structure :
            экземпляр класса data ,если data
            наследованн от Structure ,в
            противном случае будет возвращена строка (str) длинной N
        int :
            0 - транзакция успешна , не 0 -код ошибки
            
    """

    mod.reqid+=1
    seqcnt=0
    sizeof_DBW=sizeof(DBW)
    error_code=''
    
    if is_structure(data):
        data_len=sizeof(data)
        if N>data_len:
            data_len=N
    elif N>0:
        data_len=N
    else :
        return error_code,inspect.currentframe().f_lineno
    
    header=PROTO_HEADER(CBW_SIG,mod.wLun,mod.reqid,seqcnt)
    cbw=CBW(header,data_len,RW_EXCHANGE_BUFFER,TH3_PC)
    mod.so.sendto(struct2string(cbw), 0,  mod.saCtl)
    try :
        str_,k=mod.so.recvfrom(sizeof_cbw)
    except:
        return error_code,inspect.currentframe().f_lineno
    
    csw=CSW.from_buffer_copy(str_)
    seqcnt+=1

    if not((csw.status==0) & (csw.proto.reqid ==mod.reqid) & (csw.proto.seqcnt==seqcnt) ):
        return error_code,inspect.currentframe().f_lineno
    
    received_data_len=0
    string=''
    while data_len>received_data_len:
        try :
            str_,k=mod.so.recvfrom(1056*2)
        except:
            return error_code,inspect.currentframe().f_lineno
            
        seqcnt+=1
        dbw=DBW.from_buffer_copy(str_[0:sizeof_dbw])
            
        if not((dbw.status==0) & (dbw.proto.reqid ==mod.reqid) & (dbw.proto.seqcnt==seqcnt) ):
            return error_code,inspect.currentframe().f_lineno
            
        string=string+str_[sizeof_dbw:sizeof_dbw+dbw.dataTransferLength]
        received_data_len+=dbw.dataTransferLength

        seqcnt+=1
        header=PROTO_HEADER(DSW_SIG,mod.wLun,mod.reqid,seqcnt)
        dsw=DSW(header,dbw.dataTransferLength)
        mod.so.sendto(struct2string(dsw), 0,  mod.saCtl)

    
    if is_structure(data)==1:
        return data.__class__.from_buffer_copy(string[0:sizeof(data)]),0
    elif is_structure(data)==2 :
        return data.from_buffer_copy(string[0:sizeof(data)]),0
    else :
        return string,0


def send_request_rd(mod,request,request_type=NO_DATA,params=CxW_PARAMS(),data=None,data_len=0):

    N=data_len
    mod.reqid += 1
    seqcnt = 0
    sizeof_DBW = sizeof(DBW)
    error_code = ''

    if is_structure(data):
        data_len = sizeof(data)
        if N > data_len:
            data_len = N
    elif N > 0:
        data_len = N
    else:
        return error_code, inspect.currentframe().f_lineno







    header=PROTO_HEADER(CBW_SIG,mod.wLun,mod.reqid,seqcnt)
    cbw=CBW(header,data_len,RW_EXCHANGE_BUFFER, TH3_PC            )
    cbw=CBW(header,data_len,request           ,request_type|PC_TH3,params=params)

    mod.so.sendto(struct2string(cbw), 0, mod.saCtl)
    try:
        str_, k = mod.so.recvfrom(sizeof_cbw)
    except:
        return error_code, inspect.currentframe().f_lineno

    csw = CSW.from_buffer_copy(str_)
    seqcnt += 1

    if not ((csw.status == 0) & (csw.proto.reqid == mod.reqid) & (csw.proto.seqcnt == seqcnt)):
        return error_code, inspect.currentframe().f_lineno

    received_data_len = 0
    string = ''
    while data_len > received_data_len:
        try:
            str_, k = mod.so.recvfrom(1056 * 2)
        except:
            return error_code, inspect.currentframe().f_lineno

        seqcnt += 1
        dbw = DBW.from_buffer_copy(str_[0:sizeof_dbw])

        if not ((dbw.status == 0) & (dbw.proto.reqid == mod.reqid) & (dbw.proto.seqcnt == seqcnt)):
            return error_code, inspect.currentframe().f_lineno

        string = string + str_[sizeof_dbw:sizeof_dbw + dbw.dataTransferLength]
        received_data_len += dbw.dataTransferLength

        seqcnt += 1
        header = PROTO_HEADER(DSW_SIG, mod.wLun, mod.reqid, seqcnt)
        dsw = DSW(header, dbw.dataTransferLength)
        mod.so.sendto(struct2string(dsw), 0, mod.saCtl)

    if is_structure(data) == 1:
        return data.__class__.from_buffer_copy(string[0:sizeof(data)]), 0
    elif is_structure(data) == 2:
        return data.from_buffer_copy(string[0:sizeof(data)]), 0
    else:
        return string, 0
    

class CONNECTED_DEVICE(Structure):
    '''
    Parameters
    ----------
        address : str , int
            по умолчанию ('192.168.0.7', 4880)
        socket : so.socket
            не рекомендуется использовать
        csw : tnbalanceproto.CSW
            задает идентификатор модуля .
        wLun : int
            задает идентификатор модуля , если не используется csw


    .. code-block:: pycon

        >>> from tnbalancelib import *
        >>> CD=CONNECTED_DEVICE()
        >>> print CD
        serial=0
        addres=('255.255.255.255', 4880)
        >>> d,error_code= CONNECTED_DEVICE().send_request(PING)
        >>> print d , error_code
        {('192.168.0.7', 4880): <tnbalanceproto.CSW object at 0x0000000002FFB748>} 0
        >>> devices=[CONNECTED_DEVICE(csw=csw,address=k) for k,csw in d.items() ]
        >>> print devices
        [<tnbalancelib.CONNECTED_DEVICE object at 0x0000000002F30648>]
        >>> for i in devices:
        ...     k=0
        ...     print i,"\\n"
        ...     while k<MAX_SLOTS_NUMBER:
        ...     cxw=CxW_PARAMS()
        ...        cxw.u32[0]=int("41",16)<<24|int(k)<<16|8
        ...        s,status=i.send_request(MODULE_REQUEST_,params=cxw)
        ...        if status==0:
        ...            o,h =i.rd_exchange_buffer(data=MODULE_IDENT,N=06)
        ...            print o
        ...            k+=1 ,"\\n"


        serial=7
        addres=('192.168.0.7', 4880)
        \tИдентификатор модуля=SC01
        \tВерсия=0x100
        \tСерийный номер=0x1

        \tИдентификатор модуля=AD32
        \tВерсия=0x116
        \tСерийный номер=0x1f

        serial=21
        addres=('192.168.0.21', 4880)
        \tИдентификатор модуля=TS02
        \tВерсия=0x23a
        \tСерийный номер=0x1

        \tИдентификатор модуля=TS02
        \tВерсия=0x302
        \tСерийный номер=0x16

    '''
    reqid=0
    _fields_=[('MID',MODULE_IDENT),
            ('wLun',uint16_t),
            ('uDvcID',uint32_t),
            ('bOutEnabled',uint8_t),
            ('Reserved',uint8_t)]

    
    send_request=send_request
    send_request_rd=send_request_rd
    wr_exchange_buffer=wr_exchange_buffer
    rd_exchange_buffer=rd_exchange_buffer
    
    def __init__(self,**kwargs):
        Structure.__init__(self)
        #wLun
        csw=kwargs.get("csw",None)

        if type(csw)==CSW:
            self.wLun=csw.proto.lun
        else:
            self.wLun=kwargs.get("wLun", LUN_ANY)

        self.so=kwargs.get("socket",None)

        if  type(self.so)!=so.socket:
            self.so=self.__iter_socket__()

        self.saCtl = kwargs.get("address", ("255.255.255.255", 4880))
        if self.saCtl !=("255.255.255.255", 4880):
            self.wLun=int(self.saCtl[0].split(".")[-1])

        if self.wLun==0 :
            self.so.setsockopt(so.SOL_SOCKET, so.SO_BROADCAST, 1)
            #print self.saCtl ,self.so

        self.seqcnt=0
        self.saDataOut=None
        self.reqid=0
        self.modules={}

    def __str__(self):
        s="serial="+str(uint16_t(self.wLun).value)
        s+="\naddres="+str(self.saCtl)
        return s

    def get_modules(self):
        k=0
        while k < MAX_SLOTS_NUMBER:
            cxw = MODULE_REQUEST(GET_ID, k, 8)
            s, status = self.send_request(MODULE_REQUEST_, params=cxw)
            if status == 0:
                o, h = self.rd_exchange_buffer(data=MODULE_IDENT)
                o.device=self
                o.number=k
                self.modules.update({k: o})
            k += 1
        return self.modules

    def get_main_module(self,data_len=0):
        cxw = MODULE_REQUEST(0, 0, 0)
        s, status = self.send_request_rd(TASK_MEMORY_REQUEST,0x80 ,params=cxw,data_len=data_len)
        #print status,s
        if status == 0:
            #print "status"
            #o, status = self.rd_exchange_buffer()
            print "status",status
            return s
        return "err"


    def get_module_id(self,k):

        cxw = MODULE_REQUEST(GET_ID, k, 8)
        s, status = self.send_request(MODULE_REQUEST_, params=cxw)
        if status == 0:
            o, status2 = self.rd_exchange_buffer(data=MODULE_IDENT)
            if status2 > 0: raise module_error('ошибка передачи данных. tnbalancelib.py стр. '+str(status2))
        else :
            raise module_error('ошибка передачи данных. tnbalancelib.py стр.  '+str(status))
        return o

    def get_module_task(self,k):
        m=self.modules.get(k, None)
        if type(m)==type(None):
            m=self.get_module_id(k)
        print 
        mod = modules.get(struct2string_(uint32_t(m.dwID)), None)
        print "MOD:",mod ,", sizeof",sizeof(mod)
        if type(mod) == type(None):
            raise module_error("tnstruct.py не содержит описания структуры задания для "+struct2string_(uint32_t(m.dwID)))
        else:
            cxw = MODULE_REQUEST(GET_TASK, k, sizeof(mod))
            s, status = self.send_request(MODULE_REQUEST_, params=cxw)
            
            if status == 0:
                o, h = self.rd_exchange_buffer(data=mod)
            else :
                print 'error-'+hex(status)
                
            return o


    def __iter_socket__(self):
        soPing_=so.socket(so.AF_INET, so.SOCK_DGRAM, so.IPPROTO_UDP)
        iRbs=32 * 1024 * 1024
        soPing_.setsockopt( so.SOL_SOCKET, so.SO_RCVBUF, iRbs)
        bRbs = 1
        soPing_.setsockopt( so.SOL_SOCKET, so.SO_REUSEADDR, bRbs)
        uiTimeout = 1000
        soPing_.setsockopt( so.SOL_SOCKET, so.SO_RCVTIMEO, uiTimeout)
        return soPing_

class MODULE():

    def __init__(self):
        soPing=self.__iter_socket__()



    def get_module_task(self,k):
        m=self.modules.get(k, None)
        if type(m)==type(None):
            m=self.get_module_id(k)
        mod = modules.get(struct2string_(uint32_t(m.dwID)), None)

        if type(mod) == type(None):
            raise module_error("tnstruct.py не содержит описания структуры задания для "+struct2string_(uint32_t(m.dwID)))
        else:
            cxw = MODULE_REQUEST(GET_TASK, k, sizeof(mod))
            s, status = self.send_request(MODULE_REQUEST_, params=cxw)
            if status == 0:
                o, h = self.rd_exchange_buffer(data=mod)
            return o

