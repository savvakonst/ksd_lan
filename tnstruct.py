# -*- coding: utf-8 -*-
from ctypes import POINTER,sizeof, c_void_p, c_int, c_bool ,c_uint64 ,string_at
from ctypes import c_uint8, c_uint16, c_uint32, Structure, Union,c_char ,addressof
#from ctypes.wintypes import  BYTE, WORD, DWORD
import ctypes
char=c_char
uint8_t=ctypes.c_uint8
uint16_t=ctypes.c_uint16
uint32_t=ctypes.c_uint32

int8_t=ctypes.c_int8
int16_t=ctypes.c_int16
int32_t=ctypes.c_int32



class module_error(Exception):
    def __init__(self,text):
        module_error.txt = text



class MODULE_STATUS(Structure):
    _fields_=[('dwCommand',uint32_t),
              ('dwStatus',uint32_t)]

class STANDART_MODULE_TASK(Structure):
    _fields_=[('dwSize',uint32_t),
              ('dwID',uint32_t),
              ('wSlot',uint16_t),
              ('wVersion',uint16_t),
              ('wCheckSumm',uint16_t),
              ('wFlag',uint16_t),
              ('wDimension',uint16_t),
              ('wSyncMode',uint16_t),
              ('wUnit',uint16_t),
              ('Reserved10',uint8_t*10)]

    
#print sizeof(STANDART_MODULE_TASK)
    
class TN3_DATE(Structure):
    _fields_=[  ('wYear',uint16_t),
                ('bMonth',uint8_t),
                ('bDay',uint8_t)]
    _pack_=1
    
class TN3_TIME(Structure):
    _fields_=[  ('bHour',uint8_t),
                ('bMinute',uint8_t),
                ('bSecond',uint8_t),
                ('bCentisecond',uint8_t)]
    _pack_=1    

class TN3_TASK_HEADER(Structure):
    _fields_=[  ('dwTaskSize',uint32_t),
                ('dwHeaderSize',uint32_t),
                ('wTaskVersion',uint16_t),
                ('wCheckSumm',uint16_t),
                ('czPlaneType',char*16),
                ('rdDate',TN3_DATE),
                ('Reserved_a',uint8_t*4),
                ('dwPlaneNo',uint32_t),
                ('wFlyNo',uint16_t),
                ('wMinVersion',uint16_t),
                ('dwDeviceID',uint32_t),
                ('wSyncSrc',uint16_t),
                ('Reserved_c',uint8_t*14)]
    _pack_=1
    
z="""
class U_CHANNEL_ANLG0(Union):
    _fields_=[  ('bDenominatorR',uint8_t),
                ('bDenominatorVb',uint8_t),
                ('bFreqCutoffCode',uint8_t)]

class U_CHANNEL_ANLG1(Union):
    _fields_=[  ('bGainA',uint8_t),
                ('bDenominatorC',uint8_t),
                ('bICP',uint8_t),
                ('bDenominatorVi',uint8_t),
                ('Reserved1',uint8_t)]

class U_CHANNEL_ANLG2(Union):
    _fields_=[  ('',uint8_t),
                ('Reserved2',uint8_t),
                ('bType',uint8_t)]

class S_CHANNEL_ANLG0(Structure):
    _anonymous_ = ("u1","u2")
    _fields_=[  ('u1',U_CHANNEL_ANLG1),
                ('u2',U_CHANNEL_ANLG2)]
   
class U_CHANNEL_ANLG3(Union):
    _anonymous_=("s",)
    _fields_=[  ('wCurrentSupply_uA',uint16_t),("s",S_CHANNEL_ANLG0)]

class CHANNEL_ANLG (Structure):
    _anonymous_=("u1","u2")
    _fields_=[  ('bDenominatorF',uint8_t),
                ("u1",U_CHANNEL_ANLG0) ]
"""


             
class CHANNEL_ANLG_SC01 (Structure):
    _fields_=[  ('bDenominatorF',uint8_t),
                ('bDenominatorVb',uint8_t),
                ('bDenominatorVi',uint8_t),
                ('bType',uint8_t)]
    _pack_=1

class SETTINGS_ANLG_SC01(Structure):
    _fields_=[  ('dwFrequencyOfADC',uint32_t),
                ('dwVoltageBase',uint32_t),
                ('dwVoltageIn',uint32_t),
                ('cnl',CHANNEL_ANLG_SC01*4)]
    _pack_=1
    
class MODULE_SC01(Structure):
    _fields_=[  ('smt',STANDART_MODULE_TASK),
                ('adc',SETTINGS_ANLG_SC01)]
    _pack_=1


class CHANNEL_ANLG_AD32 (Structure):
    _fields_=[  ('lower_voltage_limit',uint8_t),
                ('upper_limit_of_voltage',uint8_t),
                ('decimation_code',uint8_t),
                ('reserved',uint8_t)]
    _pack_=1

class SETTINGS_ANLG_AD32(Structure):
    _fields_=[  ('dwFrequencyOfADC',uint32_t),
                ('cnl',CHANNEL_ANLG_AD32*32)]
    _pack_=1
    
class MODULE_AD32(Structure):
    _fields_=[  ('smt',STANDART_MODULE_TASK),
                ('adc',SETTINGS_ANLG_AD32)]
    _pack_=1


class CHANNEL_ANLG_A01_ (Structure):
    _fields_=[  ('frequency_code',uint8_t),
                ('reserved',uint8_t*2),
                ('flags',uint8_t),
                ('upper_limit_of_voltage',int32_t),
                ('lower_voltage_limit',int32_t),
                ('ureserved',uint32_t)]
    _pack_=1


class SETTINGS_ANLG_A01_(Structure):
    _fields_=[  ('cnl',CHANNEL_ANLG_A01_*32)]
    _pack_=1

    
class MODULE_A01_(Structure):
    _fields_=[  ('smt',STANDART_MODULE_TASK),
                ('adc',SETTINGS_ANLG_A01_)]
    _pack_=1


modules=[MODULE_SC01,MODULE_AD32,MODULE_A01_]
#print ctypes.c_uint32.from_buffer_copy(modules[0].__name__.split("_")[-1]).value
modules={i.__name__.split("_", 1)[-1]:i for i in modules}

