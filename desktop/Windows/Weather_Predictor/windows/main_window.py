from PySide6 import QtWidgets
from PySide6 import QtCore
import pyqtgraph as pg
from PySide6 import QtGui
import requests
import os
import shutil
import json
import numpy as np
from datetime import datetime
import pandas as pd


#class Widget(QWidget):
#    def __init__(self, parent=None):
#        super().__init__(parent)

class Main_window(QtWidgets.QWidget):
    def __init__(self, screen, parent=None):
        super().__init__(parent)
#Auth
        checkAuth = 0
        self._token = ""
        if os.path.isfile("token.tok"):
            checkAuth = 1
            with open('token.tok', 'r') as file:
                 self._token = file.read()
        else:
            authVbl = QtWidgets.QVBoxLayout()
            self._authLabel = QtWidgets.QLabel("Choose your token file:")
            authVbl.addWidget(self._authLabel)
            self._buttonChooseToken = QtWidgets.QPushButton("Pick a token...")
            authVbl.addWidget(self._buttonChooseToken)
            authVbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.setLayout(authVbl)

            self._buttonChooseToken.clicked.connect(self.slotChooseTokenButtonClicked)
#

#setup main vbl
        self._buttonCountry = QtWidgets.QPushButton()
        self._textLine = QtWidgets.QLineEdit()
        self._buttonPredict = QtWidgets.QPushButton()


        self._labelShowWeather1 = QtWidgets.QLabel("Show weather from")
        self._dateEdit1 = QtWidgets.QDateEdit(calendarPopup=True)
        self._labelShowWeather2 = QtWidgets.QLabel("to")
        self._dateEdit2 = QtWidgets.QDateEdit(calendarPopup=True)
        self._buttonSettings = QtWidgets.QPushButton()

        self._buttonArrowLeft = QtWidgets.QPushButton()
        pen = pg.mkPen(color=("#356ACE"),width=14)
        self._scatter = pg.ScatterPlotItem(pen=pen, symbol="o", symbolSize=20)
        self._plot_graph = pg.PlotWidget()
        self._buttonArrowRight = QtWidgets.QPushButton()

        self._labelPickedDate = QtWidgets.QLabel("Write something into text line")

        #self._textLine.setPlaceholderText("type a city here")
        self._dateEdit1.setDateTime(QtCore.QDateTime.currentDateTime())
        self._dateEdit2.setDateTime(QtCore.QDateTime.currentDateTime())

        self._textLine.setMinimumHeight(35)

        pm1 = QtGui.QPixmap("icons/icoEarth2.png")
        self._country = "None"
        self._buttonCountry.setIcon(QtGui.QIcon(pm1))
        self._buttonCountry.setMinimumWidth(40)
        self._buttonCountry.setMinimumHeight(40)
        pm1 = QtGui.QPixmap("icons/icoSearch.png")
        self._buttonPredict.setIcon(QtGui.QIcon(pm1))
        self._buttonPredict.setMinimumWidth(40)
        self._buttonPredict.setMinimumHeight(40)
        pm1 = QtGui.QPixmap("icons/icoSettings.png")
        self._buttonSettings.setIcon(QtGui.QIcon(pm1))
        self._buttonSettings.setMaximumWidth(35)
        pm1 = QtGui.QPixmap("icons/icoArrowRight.png")
        self._buttonArrowRight.setIcon(QtGui.QIcon(pm1))
        pm1 = QtGui.QPixmap("icons/icoArrowLeft.png")
        self._buttonArrowLeft.setIcon(QtGui.QIcon(pm1))
        self._buttonArrowRight.setMinimumHeight(70)
        self._buttonArrowLeft.setMinimumHeight(70)

        self._dateEdit1.setMinimumHeight(30)
        self._dateEdit2.setMinimumHeight(30)
        self._dateEdit1.setMinimumWidth(85)
        self._dateEdit2.setMinimumWidth(85)

        self._plot_graph.setBackground("w")




        self._mainVbl = QtWidgets.QVBoxLayout()

        self._hbl1 = QtWidgets.QHBoxLayout()
        self._hbl1.addWidget(self._buttonCountry)
        self._hbl1.addWidget(self._textLine)
        self._hbl1.addWidget(self._buttonPredict)
        self._mainVbl.addLayout(self._hbl1)

        self._hbl2 = QtWidgets.QHBoxLayout()
        self._hbl21 = QtWidgets.QHBoxLayout()
        self._hbl21.addWidget(self._labelShowWeather1)
        self._hbl21.addWidget(self._dateEdit1)
        self._hbl21.addWidget(self._labelShowWeather2)
        self._hbl21.addWidget(self._dateEdit2)
        self._hbl21.setSpacing(15)
        self._hbl2.addLayout(self._hbl21)
        self._hbl2.addWidget(self._buttonSettings)
        self._hbl21.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self._mainVbl.addLayout(self._hbl2)

        self._mainVbl.addSpacing(14)

        self._hbl3 = QtWidgets.QHBoxLayout()
        self._hbl3.addWidget(self._buttonArrowLeft)
        self._hbl3.addWidget(self._plot_graph)
        self._hbl3.addWidget(self._buttonArrowRight)
        self._mainVbl.addLayout(self._hbl3)

        self._hbl4 = QtWidgets.QHBoxLayout()
        self._hbl4.addWidget(self._labelPickedDate)
        self._hbl4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._mainVbl.addLayout(self._hbl4)

        if checkAuth == 1: self.setLayout(self._mainVbl)
#end of setup vbl

        self.setMinimumHeight(630)
        self.setObjectName("main_window")
        self.setWindowTitle("Weather Predictor")

        dateSet = QtCore.QDate.currentDate()
        self._dateEdit1.setMaximumDate(dateSet)
        self._dateEdit2.setMinimumDate(dateSet)
        dateSet = dateSet.addDays(-3)
        self._dateEdit1.setMinimumDate(dateSet)
        dateSet = dateSet.addDays(6)
        self._dateEdit2.setMaximumDate(dateSet)

        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        self._config = json.load(open("configs\dev.json"))

# setup country
        self._countryChooseDialog = QtWidgets.QDialog(self)

        self._countryChooseDialog.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        self._countryList = QtWidgets.QListWidget()
        self.setupCountryList()
        countryChooseCloseButton = QtWidgets.QPushButton("close")

        vbl1 = QtWidgets.QVBoxLayout()
        vbl1.addWidget(self._countryList)
        vbl1.addWidget(countryChooseCloseButton)

        self._countryChooseDialog.setLayout(vbl1)
# end of setup

        self._buttonPredict.clicked.connect(self.slotPredictButtonClicked)
        self._scatter.sigClicked.connect(self.slotPlotPointClicked)
        self._buttonCountry.clicked.connect(self.slotCountryButtonClicked)
        #self.mouseMoveEvent(self.slotMouseMoveEvent)
        countryChooseCloseButton.clicked.connect(self._countryChooseDialog.close)
        self._countryList.itemClicked.connect(self.slotCountryListItemClicked)
        self._plot_graph.plot(pen=pen)
        ###self._plot_graph.sigMouseReleased.connect(self.slotWeatherDialogCloseButtonClicked)


#        self._time = [0,400, 800, 1200, 1600, 2000]
#        self._timeStr = ["00:00","04:00", "08:00", "12:00", "16:00", "20:00"]
        self._time = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100,2200, 2300]
        self._timeStr = ["00:00", "01:00","02:00","03:00","04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

        self._weatherDialog = QtWidgets.QDialog(self)
        self._weatherDialogLabelTime = QtWidgets.QLabel()
        self._weatherDialogLabelTempreature = QtWidgets.QLabel()
        self._weatherDialogButtonClose = QtWidgets.QPushButton("Close")
        vbl2 = QtWidgets.QVBoxLayout(self._weatherDialog)
        vbl2.addWidget(self._weatherDialogLabelTime)#("Time: " + time)
        vbl2.addWidget(self._weatherDialogLabelTempreature)#("Tempreature: " + tempreature)
        vbl2.addWidget(self._weatherDialogButtonClose)
        self._weatherDialog.setLayout(vbl2)
        self._weatherDialog.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        self._weatherDialogButtonClose.clicked.connect(self._weatherDialog.close)

        self._temperature = []
        self._windSpeed = []
        self._humidity = []
        self._pressure  = []
        self._weatherCategory  = []

        self._maxTemperature = 0.0
        self._minTemperature = 0.0

# example of adding points
#        self._temperature  = [-1, 0, 1, 3, 5, 3, 4, 8, 3, 5, 2, 5, 1, 6, 7, 3, 5, 2, 5, 2, 5, 3, 5, 1]
#        self._scatter.addPoints(self._time, self._temperature)
#        self._plot_graph.addItem(self._scatter)
#



    def paintEvent(self, event: QtGui.QPaintEvent):
            with QtGui.QPainter(self) as p:
                rect1 = self._hbl1.geometry()
                rect2 = self._hbl2.geometry()
                temp = rect1.height()+rect1.height()*0.333

                p.setPen(QtGui.QColor("#FFC700"))
                p.setBrush(QtGui.QBrush(QtGui.QColor("#FFC700"), QtCore.Qt.SolidPattern))
                p.drawRect(0, 0, self.width(), temp)

                p.setPen(QtGui.QColor("#FFD53F"))
                p.setBrush(QtGui.QBrush(QtGui.QColor("#FFD53F"), QtCore.Qt.SolidPattern))
                p.drawRect(0, temp, self.width(), rect2.height()+rect2.height()*0.40)

    def slotChooseTokenButtonClicked(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a token", "", "token.tok")
        self._buttonChooseToken.setDisabled(1)

        if os.path.isfile(path[0]):
            shutil.copy(path[0], "token.tok")
            with open('token.tok', 'r') as file:
                self._token = file.read()
            url1 = self._config["Host"] + "/Auth"
            headers1={"Authorization": "Bearer " + self._token}
            response = safeRequest("GET", url=url1, headers=headers1)
            self._authLabel.setText("Authorization...")

            if response == None:
                self._authLabel.setText("Server is unreachable")
                os.remove("token.tok")
                self._buttonChooseToken.setDisabled(0)
                return
            if response.status_code == 401:
                self._authLabel.setText("Unauthorized: You have an incorrect/outdated token")
                os.remove("token.tok")
                self._buttonChooseToken.setDisabled(0)
                return

            QtWidgets.QWidget().setLayout(self.layout())
            self.setLayout(self._mainVbl)


    def slotPredictButtonClicked(self):
        url = self._config["Host"] + "/Predict/" + self._country + "-" + self._textLine.text().replace(" ", "")
        headers={"Authorization": "Bearer " + self._token}        

        date_list = pd.date_range(self._dateEdit1.date().toPython(), self._dateEdit2.date().toPython(), freq='D')
        dates = []
        for i in date_list: dates.append(i.date().strftime("%d.%m.%Y"))
        json= {"dates": dates}

        self._buttonPredict.setDisabled(1)
        self._labelPickedDate.setText("Predicting...")

        response = safeRequest("GET", url=url, headers=headers, json=json)
        if response == None:
            self._labelPickedDate.setText("Server is unreachable")
            self._buttonPredict.setDisabled(0)
            return

        if response.status_code == 401:
            self._labelPickedDate.setText("Unauthorized: You have an incorrect/outdated token")
            self._buttonPredict.setDisabled(0)
            return



        #some vizualization stuff
        self._labelPickedDate.setText(response.json()["Data"])
        #

        self._buttonPredict.setDisabled(0)

    def slotPlotPointClicked(self, points, point):
        item = point.item()
        index = np.where(self._scatter.points() == item)[0][0]
        self.showWeatherDataDialog(self._timeStr[index], str(self._temperature[index]))

    def showWeatherDataDialog(self, time, tempreature):
        self._weatherDialogLabelTime.setText("Time: " + time)
        self._weatherDialogLabelTempreature.setText("Tempreature: " + tempreature)

        pos = QtGui.QCursor.pos()
        self._weatherDialog.setGeometry(pos.x(), pos.y(), self._weatherDialog.width(), self._weatherDialog.height())
        self._weatherDialog.show()

#    def slotWeatherDialogCloseButtonClicked(self):
#        self._weatherDialog.close()
    def slotCountryButtonClicked(self):
        self._countryChooseDialog.setGeometry(
        self.x()+self._buttonCountry.x(),
        self.y()+ self._buttonCountry.y()+self._buttonCountry.height()+30,
        self.height()*0.4/2,
        self.height()*0.4)
        self._countryChooseDialog.show()
    def slotCountryListItemClicked(self, ev):
        self._country = ev.text()
        pm1 = QtGui.QPixmap("icons/"+ev.text()+".png")
        self._buttonCountry.setIcon(QtGui.QIcon(pm1))
        self._countryChooseDialog.close()

    def setupCountryList(self):
        self._countryList.addItem("Ukraine")
        self._countryList.addItem("USA")

#    def mouseMoveEvent(self, ev):
#        if ev.buttons() == QtCore.Qt.MouseButton.LeftButton:
#            print(ev)
#        super().mouseMoveEvent(ev)


def safeRequest(method, url, headers={}, json={}):
    try:
        response = requests.request(url=url, method=method, headers=headers, json=json)
        return response
    except Exception as e:
        return None

