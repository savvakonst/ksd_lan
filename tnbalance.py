# -*- coding: utf-8 -*-
"""
This example module shows various types of documentation available for use
with pydoc.  To generate HTML documentation for this module issue the
command:

    pydoc -w foo

"""
__docformat__ = "restructuredtext"




from tnbalancelib import *
from pof2bin import *






CD=CONNECTED_DEVICE()
d,error_code= CONNECTED_DEVICE().send_request(PING)


devices=[CONNECTED_DEVICE(csw=csw,address=k) for k,csw in d.items() ]

kk=0



from functools import partial
from PyQt4.QtCore import Qt ,QObject
from PyQt4.QtGui import QApplication  ,QTreeView ,QStandardItemModel ,QProgressDialog,QStandardItem ,QPushButton ,QComboBox
import sys
import cmd_run

app = QApplication(sys.argv)

tree = QTreeView()


tree._datamodel = QStandardItemModel(0, 2)
tree.setModel(tree._datamodel)

tree.model().setHorizontalHeaderLabels(['', '',"","","",""])
def prints(sd,eve):
    print "sadaws"

List_of_dirs= [x[0].split("\\")[-1] for x in os.walk("POFS")]

class module_gui(QObject):
    def __init__(self,progress,mod,list ):
        QObject.__init__(self)
        ID, VER, SER = list
        self.mod=mod
        self.ID=ID
        self.VER=VER
        self.SER=SER
        self.Name=None

    def update(self):
        lun= self.mod.device.wLun
        addr= self.mod.device.saCtl[0]
        N= self.mod.number

        cmd_run.cmd_run(addr,lun,N,self.ID.text(),self.VER.text(),self.SER.text())

    def update_sofwhere(self):
        print "--------------------------------------------------------------------",self.Name.currentText()
        data=read_pof(self.Name.currentText(),"pofs\\"+self.ID.text()+"\\")
        #print self.ID.text()
        self.progress.setValue(100)
        self.progress.open()
        self.write_sofwhere(data)
        #self.write_ID_VER(str(self.ID.text()),readk(self.VER.text()),readk(self.SER.text()))




progress_dlg = QProgressDialog(tree)
id_=0
count=0
for i in devices:
    m=i.get_modules()
    Dev_ =QStandardItem( u"устройство  "+i.saCtl[0])
    Dev_.setFlags(Qt.NoItemFlags)
    tree.model().appendRow(Dev_)

    id2_=0
    for j in i.modules:
        try:
            module=i.modules[j]
            Slot=QStandardItem( u"слот "+str(j+1)+":")


            s, error = module.status_command_eeprom()
            print "error",hex(error)
            if error==0:
                sa = Flash_HEADER.from_buffer_copy(s[4:16])
                if sa.page_size==0:
                    error=1
                    print "sdfsf"
                else :
                    try:
                        f = open(struct2string_(uint32_t(module.dwID)) + "_" + str(uint16_t(module.wSerialNumber).value)+".txt",'wb')
                    except:
                        f = open(str(count)+"N.txt", 'wb')
                        count += 1
                    data = ''

                    for b in xrange(0,(sa.prog_addr >> 10)):
                        g, err = module.read_eeprom(b * 1024)
                        data += g
                    f.write(data)
                    f.close()


            if error==0 :
                col0_flags=Qt.NoItemFlags | Qt.ItemIsEnabled
                col1_flags = Qt.ItemIsEnabled |Qt.ItemIsEditable | ~ Qt.ItemIsSelectable
            else :
                col0_flags=Qt.NoItemFlags
                col1_flags = Qt.NoItemFlags

            def gen_row(var1,var2):
                ID_= QStandardItem(var1 +var2)
                ID_copy = QStandardItem(var2)
                ID_.setFlags(col0_flags)
                ID_copy.setFlags(col1_flags)
                return[ID_,ID_copy]

            def int2ver(var):
                return str(var>>8)+"."+str(var&255)

            hp=lambda x : reduce(lambda y,z:y&z ,[(0x29<ord(ij))&(ord(ij)<0x80) for ij in x])
            hr=lambda x : "F"*((not hp(x))*4)+x*(hp(x)*1)


            Slot.appendRow(gen_row( u"ID :",hr(struct2string_(uint32_t(module.dwID)))))
            Slot.appendRow(gen_row( u"Версия :", int2ver(uint16_t(module.wVersion).value)))
            Slot.appendRow(gen_row( u"Серия  :", str(uint16_t(module.wSerialNumber).value)))
            Slot.setFlags(col0_flags)
            Dev_.setFlags(Dev_.flags() | col0_flags)

            if error == 0:

                mh = module_gui(progress_dlg, module, [Slot.child(g, 1) for g in xrange(3)] )
                if mh.ID.text() in List_of_dirs :

                    listOfFiles = os.listdir("pofs\\"+mh.ID.text())
                    if len(listOfFiles)>0:
                        Slot_b = QStandardItem(u"")
                        Slot_c = QStandardItem(u"")
                        Slot_d = QStandardItem(u"")
                        Dev_.appendRow([Slot,Slot_b,Slot_c,Slot_d])
                        combobox = QComboBox()
                        combobox.addItems(listOfFiles)

                        mh.Name=combobox
                        qindex_widget = Slot_c.index()
                        tree.setIndexWidget(qindex_widget, combobox)

                        button = QPushButton(u'записать')
                        button.clicked.connect(partial(module_gui.update_sofwhere, mh))

                        qindex_widget = Slot_d.index()
                        tree.setIndexWidget(qindex_widget, button)
                    else:
                        Slot_b = QStandardItem(u"")
                        Dev_.appendRow([Slot, Slot_b])
                else :
                    Slot_b = QStandardItem(u"")
                    Dev_.appendRow([Slot, Slot_b])
                button=QPushButton(u'записать')

                button.clicked.connect(partial(module_gui.update,mh))
                qindex_widget = Slot_b.index()
                tree.setIndexWidget(qindex_widget, button)


                qindex_widget =Dev_.index()
                tree.expand(qindex_widget)
            else :
                Dev_.appendRow([Slot])


        except module_error:
            print module_error.txt
    id_ += 1


    print "\n\n"

tree.keyPressEvent =prints
tree.show()

sys.exit(app.exec_())




