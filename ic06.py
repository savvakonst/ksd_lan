# -*- coding: utf-8 -*-
"""
git remote add origin https://savvakonst:ansskata18@github.com/savvakonst/ksd_lan.git


"""
__docformat__ = "restructuredtext"




from tnbalancelib import *





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
    devices=[CONNECTED_DEVICE(csw=4,address=('192.168.0.4', 4880))]
kk=0



from functools import partial
import sys
import time


#List_of_dirs= [x[0].split("\\")[-1] for x in os.walk("POFS")]
class Incr :
    def __init__(self,N=0):
        self.N=N+1

    def incr(self):
        self.N-=1
        return self.N>0

def Cycl(N):
    return 1,Incr(N)

def tr(x,i):
    return ctypes.c_uint64.from_buffer_copy(x[0+i*4:8+i*4])


class MDIO_AD(Structure):
    _fields_ = [("DEVAD", uint8_t),
                ("PRTAD", uint8_t),
                ("REGAD", uint16_t)]



c_short=ctypes.c_uint8
class Reg_0(ctypes.LittleEndianStructure):
    _fields_ = [("Reserved", c_short, 5),
                ("Unidirectional_enable", c_short, 1),
                ("Speed_Selection_MSB", c_short, 1),
                ("Collision_Test", c_short, 1),
                ("Duplex_Mode", c_short, 1),
                ("Restart_Auto_Negotiation", c_short, 1),
                ("Isolate", c_short, 1),
                ("Power_Down", c_short, 1),
                ("Auto_Negotiation_Enable", c_short, 1),
                ("Speed_Selection_LSB", c_short, 1),
                ("Loopback", c_short, 1),
                ("Reset", c_short, 1)]

class Reg_1(ctypes.LittleEndianStructure):
    _fields_ = [("Extended_Capability", c_short, 1),
                ("Jabber_Detect", c_short, 1),
                ("Link_Status", c_short, 1),
                ("Auto_Negotiation_Ability", c_short, 1),
                ("Remote Fault", c_short, 1),
                ("Auto_Negotiation_Complete", c_short, 1),
                ("MF_Preamble_Suppression", c_short, 1),
                ("Unidirectional_ability", c_short, 1),
                ("Extended_Status", c_short, 1),
                ("100BASE_T2_Half_Duplex", c_short, 1),
                ("100BASE_T2_Full_Duplex", c_short, 1),
                ("10_Mb_Half_Duplex", c_short, 1),
                ("10_Mb_Full_Duplex", c_short, 1),
                ("100BASE_X_Half_Duplex", c_short, 1),
                ("100BASE_X_Full_Duplex", c_short, 1),
                ("100BASE_T4", c_short, 1)]


class Reg_9(ctypes.LittleEndianStructure):
    _fields_ = [("Reserved", c_short, 8),
                ("1000BASE_T_half_Duplex", c_short, 1),
                ("1000BASE_T_Full_Duplex", c_short, 1),
                ("Port_type", c_short, 1),
                ("MASTER_SLAVE_Config_Value", c_short, 1),
                ("MASTER_SLAVE_Manual_Config_Enable", c_short, 1),
                ("Test_mode_bits", c_short, 3)]


class MAC_Reg_0x0(ctypes.LittleEndianStructure):
    _fields_ = [("Reserved", c_short, 5),
                ("Unidirectional_enable", c_short, 1),
                ("Speed_Selection_MSB", c_short, 1),
                ("Collision_Test", c_short, 1),
                ("Duplex_Mode", c_short, 1),
                ("Restart_Auto_Negotiation", c_short, 1),
                ("Isolate", c_short, 1),
                ("Power_Down", c_short, 1),
                ("Auto_Negotiation_Enable", c_short, 1),
                ("Speed_Selection_LSB", c_short, 1),
                ("Loopback", c_short, 1),
                ("Reset", c_short, 1)]


class MAC_Reg_0x14(ctypes.LittleEndianStructure):
    _fields_ = [("SGMII_ENA", c_short, 1),
                ("USE_SGMII_AN", c_short, 1),
                ("SGMII_SPEED", c_short, 2),
                ("SGMII_DUPLEX", c_short, 1),
                ("SGMII_AN_MODE", c_short, 1),
                ("Reserved_a", c_short, 2),
                ("Reserved_b", c_short, 8)]

register_struct_t_list=[Reg_0,Reg_1]
print "sizeof(Reg_0)",sizeof(Reg_1)

def setup0x20_reg(module,MDIO_ACCESS,addr):
    module.set_custom_params(0x6,[MDIO_ACCESS,addr])


def setup0x21_reg(module,MDIO_DEVAD,MDIO_PRTAD,MDIO_REGAD):
    mdio_ad=MDIO_AD()
    mdio_ad.DEVAD=MDIO_DEVAD
    mdio_ad.PRTAD=MDIO_PRTAD
    mdio_ad.REGAD=MDIO_REGAD
    s=c_uint32()
    ctypes.memmove(ctypes.pointer(s),ctypes.pointer(mdio_ad),4)
    module.set_custom_params(0x7,[s.value,])
    
def get0x20_reg(module,addr):

    err,i =Cycl(10)
    while err and i.incr():
        c,err=module.get_custom_params(0x10,[0,addr])
    if err :sys.exit()


    #print str(c)[0:4]
    mdio=uint32_t.from_buffer_copy(c[0:4])
    ret=hex(mdio.value)[2:-1]
    if (addr<len(register_struct_t_list)):
        reg0=register_struct_t_list[addr]()
        ctypes.memmove(ctypes.pointer(reg0), ctypes.pointer(uint16_t(mdio.value)), 2)
        print struct2txt(reg0)
    elif(addr==9):
        reg0=Reg_9()
        ctypes.memmove(ctypes.pointer(reg0), ctypes.pointer(uint16_t(mdio.value)), 2)
        print struct2txt(reg0)
    else:
        print   "0"*(8-len(ret))+ret




def get0x21_reg(module):
    err,i =Cycl(10)
    while err and i.incr():
        c,err = module.get_custom_params(0x11)
    if err :sys.exit()

    mdio=MDIO_AD.from_buffer_copy(c[0:4])
    print struct2txt(mdio)

def setup_eth_reg(module,MDIO_ACCESS,addr):
    module.set_custom_params(0x14,[MDIO_ACCESS,addr])

def get_eth_reg(module,addr):
    c=module.get_custom_params(0x015,[0,addr])[0]
    #print str(c)[0:4]
    mdio=uint32_t.from_buffer_copy(c[0:4])
    ret=hex(mdio.value)[2:-1]
    if (addr==0x14):
        reg=MAC_Reg_0x14()
        ctypes.memmove(ctypes.pointer(reg), ctypes.pointer(uint16_t(mdio.value)), 2)
        print struct2txt(reg)
    else:
        print   "0"*(8-len(ret))+ret


def wait(N=3):
    print "-----------------------------------"
    ind = N*2
    while ind > 0:
        ind -= 1
        if ind%2==0:
            print "time",ind/2.0
        time.sleep(0.5)
        print "-----------------------------------"




def reg2value(reg_s):
    reg = uint16_t()
    ctypes.memmove(ctypes.pointer(reg), ctypes.pointer(reg_s), 2)
    return reg.value


#
# clause 22.2.4.5
# clause 22.2.4.5
#
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

        #tsk=module.get_module_task()

        #print struct2txt(tsk)
        wait(0)
        setup0x21_reg(module, 0, 0, 0)


        setup0x20_reg(module, 2, 22)
        reg_0 = Reg_0(0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1)
        setup0x20_reg(module, reg2value(reg_0), 0)
        get0x20_reg(module,0)
        setup0x20_reg(module, 0, 22)
        get0x20_reg(module,0)
        wait(0)
        #reg_0 = Reg_0(0x0, 0x0, 0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1)
        #setup0x20_reg(module, reg2value(reg_0), 0)
        get0x20_reg(module,16)
        wait(0)
        get0x20_reg(module,1)
        wait(0)
        get0x20_reg(module,9)
        wait(0)
        reg_9=Reg_9(0x0,0x0,0x0,0x1,0x1,0x0,0x0)
        #setup0x20_reg(module, reg2value(reg_9), 9) |
        reg_0=Reg_0(0x0,0x0,0x1,0x0,0x1, 0x0, 0x0, 0x0, 0x1, 0x0, 0x0, 0x1)
        #setup0x20_reg(module, reg2value(reg_0), 0)
        wait(0)
        get0x20_reg(module, 0)
        wait(0)
        #get_eth_reg(module, 0x14)
        """
        for i in xrange(0x15):
            wait(0)
            get_eth_reg(module, i)
        #setup_eth_reg(module,1|(1<<5),0x14)
        wait(2)
        for i in xrange(0x15):
            wait(0)
            get_eth_reg(module, i)
        """
  


#Register 1 (Continued) Page 2, Register 16



"""
0x00 control RW PCS control register. Use this register to control and
configure the PCS function. For the bit description, see
Control Register (Word Offset 0x00) on page 95.
0x1140

0x01 status RO Status register. Provides information on the operation of the
PCS function.
0x0089

0x02 phy_identifier RO 32-bit PHY identification register. This register is set to the
value of the PHY ID parameter. Bits 31:16 are written to
word offset 0x02. Bits 15:0 are written to word offset 0x03.
0x0101

0x03 0x0101

0x04 dev_ability RW Use this register to advertise the device abilities to a link
partner during auto-negotiation. In SGMII MAC mode, the
PHY does not use this register during auto-negotiation. For
the register bits description in 1000BASE-X and SGMII
mode, see 1000BASE-X on page 97 and SGMII PHY Mode
Auto Negotiation on page 99.
0x01A0
cont
"""
