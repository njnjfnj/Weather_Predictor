# This Python file uses the following encoding: utf-8
#from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtCore import qDebug
from PySide6 import QtCore
import pyqtgraph as pg
from PySide6 import QtGui

#class Widget(QWidget):
#    def __init__(self, parent=None):
#        super().__init__(parent)

class Main_window(QtWidgets.QWidget):
    def __init__(self, screen, parent=None):
        super().__init__(parent)

        self._buttonCountry = QtWidgets.QLabel()
        self._textLine = QtWidgets.QLineEdit()
        self._buttonPredict = QtWidgets.QPushButton()


        self._labelShowWeather1 = QtWidgets.QLabel("Show weather from")
        self._dateEdit1 = QtWidgets.QDateEdit(calendarPopup=True)
        self._labelShowWeather2 = QtWidgets.QLabel("to")
        self._dateEdit2 = QtWidgets.QDateEdit(calendarPopup=True)
        self._buttonSettings = QtWidgets.QPushButton()

        self._buttonArrowLeft = QtWidgets.QPushButton()
        self._plot_graph = pg.PlotWidget()
        self._buttonArrowRight = QtWidgets.QPushButton()

        self._labelPickedDate = QtWidgets.QLabel("00:00:00")


        #self._textLine.setPlaceholderText("type a city here")
        self._dateEdit1.setDateTime(QtCore.QDateTime.currentDateTime())
        self._dateEdit2.setDateTime(QtCore.QDateTime.currentDateTime())

        pm1 = QtGui.QPixmap("icons/icoEarth.png")
        w1 = self._buttonCountry.contentsRect().width()
        #pm1 = pm1.scaledToWidth(pm1.width()/w1, QtCore.Qt.SmoothTransformation)
        self._buttonCountry.setPixmap(pm1)

        self._mainVbl = QtWidgets.QVBoxLayout()

        self._hbl1 = QtWidgets.QHBoxLayout()
        self._hbl1.addWidget(self._buttonCountry)
        self._hbl1.addWidget(self._textLine)
        self._hbl1.addWidget(self._buttonPredict)
        self._mainVbl.addLayout(self._hbl1)

        h = self._hbl1.geometry().height()
        qDebug(str(h))
        self._mainVbl.addSpacing(h)

        self._hbl2 = QtWidgets.QHBoxLayout()
        self._hbl2.addWidget(self._labelShowWeather1)
        self._hbl2.addWidget(self._dateEdit1)
        self._hbl2.addWidget(self._labelShowWeather2)
        self._hbl2.addWidget(self._dateEdit2)
        self._hbl2.addWidget(self._buttonSettings)
        self._mainVbl.addLayout(self._hbl2)
        #self._mainVbl.addSpacing(100)

        self._hbl3 = QtWidgets.QHBoxLayout()
        self._hbl3.addWidget(self._buttonArrowLeft)
        self._hbl3.addWidget(self._plot_graph)
        self._hbl3.addWidget(self._buttonArrowRight)
        self._mainVbl.addLayout(self._hbl3)

        self._mainVbl.addWidget(self._labelPickedDate)

        self.setLayout(self._mainVbl)




    def paintEvent(self, event: QtGui.QPaintEvent):
            with QtGui.QPainter(self) as p:
                rect1 = self._hbl1.geometry()
                rect2 = self._hbl2.geometry()
                temp = rect1.height()+rect1.height()*0.75

                p.setPen(QtGui.QColor("#FFC700"))
                p.setBrush(QtGui.QBrush(QtGui.QColor("#FFC700"), QtCore.Qt.SolidPattern))
                p.drawRect(0, 0, self.width(), temp)

                p.setPen(QtGui.QColor("#FFD53F"))
                p.setBrush(QtGui.QBrush(QtGui.QColor("#FFD53F"), QtCore.Qt.SolidPattern))
                p.drawRect(0, temp, self.width(), rect2.height()+rect2.height()*0.75)


