# -*- coding: utf-8 -*-

import sys

#from PyQt4.QtGui import *
#from PySide.QtCore import *
from PySide.QtGui import *
from tnstruct import *
from tncommon import *
#import matplotlib.pyplot as plt
from ctypes import memmove
from data_recive.d01__recive import *
from treeView import TreeView

listOfValuesNames = u"""
частота по положительному фронту
частота по отрицательному фронту
период по положительному фронту
период по отрицательному фронту
длительности положительного импульса
длительности отрицательного импульса""".split("\n")[1:]

listOfStr = u"""
F_рег частоты сигнала по положительному фронту
F_рег частоты сигнала по отрицательному фронту
F_рег периода сигнала по положительному фронту
F_рег периода сигнала по отрицательному фронту
F_рег длительности положительного импульса
F_рег длительности отрицательного импульса""".split("\n")[1:]


def d01_createIndexArray( task, valuesCount=6, channelsCount=16):
    class channelSt(Structure):
        _fields_ = [('values', uint16_t * valuesCount)]
        _pack_ = 1

    class dataCountSt(Structure):
        _fields_ = [('channels', channelSt * channelsCount)]
        _pack_ = 1

        def copy(self, struct): memmove(addressof(self), addressof(struct), sizeof(self))

    dataCount = dataCountSt()

    def frCode2fr(code):
        return 0 if code == 0xFF else 2 ** code

    def frDivision(max_val, code):
        return 0 if code == 0 else max_val / code

    maxArr = []
    pointsNum = 0
    for i in xrange(channelsCount):
        dataCount.channels[i].values[0] = frCode2fr(task.data.cnl[i].frequencyFp)
        dataCount.channels[i].values[1] = frCode2fr(task.data.cnl[i].frequencyFn)
        dataCount.channels[i].values[2] = frCode2fr(task.data.cnl[i].frequencyTp)
        dataCount.channels[i].values[3] = frCode2fr(task.data.cnl[i].frequencyTn)
        dataCount.channels[i].values[4] = frCode2fr(task.data.cnl[i].frequencyDp)
        dataCount.channels[i].values[5] = frCode2fr(task.data.cnl[i].frequencyDn)
        maxArr.append(max(dataCount.channels[i].values))
        pointsNum += sum(dataCount.channels[i].values)
    maxVal = max(maxArr)

    dataCountBase = []
    for i in xrange(channelsCount):
        for j in xrange(valuesCount):
            dataCountBase.append(frDivision(maxVal, dataCount.channels[i].values[j]))

    indexArray = []
    for i in xrange(maxVal):
        for j in xrange(len(dataCountBase)):
            k = dataCountBase[j]
            if 0 == (1 if k == 0 else i % k): indexArray.append(j)

    print indexArray
    # print struct2txt(dataCount, format=DEC_fr)  # print task for N-channel
    return indexArray


class UpdateButton(QPushButton):
    def __init__(self,txt,listOfFrComboBox,voltageP,voltageN,param,module,ether):
        QPushButton.__init__(self,txt)
        self.listOfFrComboBox=listOfFrComboBox
        self.param=param
        self.voltageP=voltageP
        self.voltageN=voltageN
        self.clicked.connect(self.keyPressEvent)
        self.module=module
        self.ether =ether

    def keyPressEvent(self):
        ChNum=self.param.currentIndex()
        factor=10000*100
        def combo_index(n):
            index=self.listOfFrComboBox[n].currentIndex()
            if index==0:index=0xFF
            else : index=index-1
            return index
        ch=SETTINGS_D01_()
        def ch_setup_default(N):
            ch.cnl[N].frequencyFp =0xff
            ch.cnl[N].frequencyFn =0xff
            ch.cnl[N].frequencyTp =0xff
            ch.cnl[N].frequencyTn =0xff
            ch.cnl[N].frequencyDp =0xff
            ch.cnl[N].frequencyDn =0xff
            ch.cnl[N].reserved    =0
            ch.cnl[N].flags       =0
            ch.cnl[N].voltageP    =20000
            ch.cnl[N].voltageN    =-20000
            ch.cnl[N].filter      =0

        def ch_setup(N):
            ch.cnl[N].frequencyFp =combo_index(0)
            ch.cnl[N].frequencyFn =combo_index(1)
            ch.cnl[N].frequencyTp =combo_index(2)
            ch.cnl[N].frequencyTn =combo_index(3)
            ch.cnl[N].frequencyDp =combo_index(4)
            ch.cnl[N].frequencyDn =combo_index(5)
            ch.cnl[N].reserved    =0
            ch.cnl[N].flags       =0
            ch.cnl[N].voltageP    =int(factor*float(self.voltageP.text()))
            ch.cnl[N].voltageN    =int(factor*float(self.voltageN.text()))
            ch.cnl[N].filter      =0

        if ChNum==0:
            for i in xrange(16): ch_setup(i)
        else:
            for i in xrange(16): ch_setup_default(i)
            ch_setup(ChNum-1)

        #print struct2txt(ch,format=DEC_fr)
        if __name__ == "__main__":
            return

        self.ether.pause=True
        while False==self.ether.waitSecondPoint: pass
        tsk = self.module.get_module_task()            # get task
        tsk.data=ch
        tsk.setCheckSumm()
        self.module.set_module_task(tsk)  # send  task
        tsk = self.module.get_module_task()  # get task

        self.ether.indexArray=d01_createIndexArray(tsk)
        self.ether.pause = False
        #print struct2txt(tsk, format=DEC_fr)  # print task for N-channel




class MainW(QWidget):
    def __init__(self,module,src,D01__module_num,activModuleCount):
        QWidget.__init__(self)

        topLayaut  = QHBoxLayout()
        vertLayaut =  QVBoxLayout()
        formLayout = QFormLayout()
        chNLayout  = QFormLayout()
        paramGroup = QGroupBox(u"параметры")



        param = QComboBox()
        param.addItem(u"все каналы")
        for i in range(16):  param.addItem(str(i))
        chNLayout.addRow(u"выбор канала",  param);

        def genFrComboBox(max_range):
            combo = QComboBox()
            combo.addItem(u"не регистрируется")
            for i in range(max_range) :  combo.addItem(str(2**i))
            return combo

        voltageP = QLineEdit("0.02")
        voltageN = QLineEdit("-0.02")
        voltageP.setValidator(QDoubleValidator(0.2, 30.0,2))
        voltageN.setValidator(QDoubleValidator(-30,  0,2))
        formLayout.addRow(u"положительный",  voltageP);
        formLayout.addRow(u"отрицательный",  voltageN);
        #print int(100*float(voltageP.text()))
        listOfFrComboBox=[]

        for i in listOfStr:
            cb=genFrComboBox(11)
            listOfFrComboBox.append(cb)
            formLayout.addRow(QLabel(i), cb );


        self.ether = Ethernet(d01_createIndexArray(module.get_module_task()),src, D01__module_num, activModuleCount,parent=self)
        self.ether.start()


        uButton=UpdateButton(u"обновить",listOfFrComboBox,voltageP,voltageN,param,module,self.ether)

        self.treeView=TreeView(listOfValuesNames,numOfChannels=16)

        paramGroup.setLayout(formLayout)
        vertLayaut.addLayout(chNLayout)
        vertLayaut.addWidget(paramGroup)
        vertLayaut.addWidget(uButton)
        topLayaut.addLayout(vertLayaut)
        topLayaut.addWidget(self.treeView)
        self.setLayout(topLayaut)

    def update(self,data):
        self.treeView.update(data)


    def close(self):
        self.ether.pause =False
        self.ether.enable=False
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        udp_socket.bind( (self.ether.so.getsockname()[0],777))
        udp_socket.sendto(b'exit', self.ether.so.getsockname())
        udp_socket.close()
        self.ether.join()

        QWidget.close(self)




# ------------------------------------------
# -- Create window
# ------------------------------------------
def create_widget(module,src,D01__module_num,activModuleCount):
    myApp = QApplication(sys.argv)                   # Create an PyQT4 application object.
    topWidget = MainW(module,src,D01__module_num,activModuleCount,)                                    # The QWidget widget is the base class
    topWidget.setWindowTitle('D01_')
    topWidget.resize(400, 200)
    topWidget.show()
    myApp.setStyle("windows")
    myApp.exec_()
    topWidget.close()
    print "terminalend"


if __name__ == "__main__":
    create_widget(0)