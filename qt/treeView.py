# -*- coding: utf-8 -*-

import sys, os, pprint, time
from PySide.QtCore import *
from PySide.QtGui import *
#import numpy as np

listOfValuesNames = u"""
частота по положительному фронту
частота по отрицательному фронту
период по положительному фронту
период по отрицательному фронту
длительности положительного импульса
длительности отрицательного импульса""".split("\n")[1:]



class TreeView(QTreeView):
    def __init__(self,listOfValuesNames=listOfValuesNames,numOfChannels=16):
        QTreeView.__init__(self)
        self.setStyleSheet("QTreeView::item:hover{background-color:#999966;}")
        self.setAnimated(False)
        self.setUniformRowHeights(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.numOfChannels=numOfChannels
        self.listOfValuesNames=listOfValuesNames
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([u"канал", u"среднее"])
        self.setModel(self.model)


        self.maxColumnNum=1
        self.listOfChannels = list()
        self.listOfValues = list()

        self.create()



    def create(self):
        for i in range(self.numOfChannels):
            parent = QStandardItem('{}'.format(i))
            for j in self.listOfValuesNames:
                mainColumn = QStandardItem(j)
                meanValueColumn = QStandardItem('{}'.format(3))
                self.listOfValues.append(meanValueColumn)
                parent.appendRow([mainColumn, meanValueColumn])
            self.model.appendRow(parent)
            self.setFirstColumnSpanned(i, self.rootIndex(), True)

        #print self.model.takeColumn(0)
        print self.model.item(0, 0).child(0,1).text()
        print self.model#.item(0, 0).takeColumn(1)

        for i in self.listOfValues: i.setText("NoData")


    def update(self,data):
        for i in xrange(len(self.listOfValues)):
            if len(data[i])==0:
                txt="NoData"
            else :
                txt=str(float(sum(data[i]))/len(data[i]))
            self.listOfValues[i].setText(txt)

        print len(data[0])




if __name__ == "__main__":
    app = QApplication(sys.argv)
    view=TreeView()
    view.show()
    app.setStyle("windows")
    sys.exit(app.exec_())



