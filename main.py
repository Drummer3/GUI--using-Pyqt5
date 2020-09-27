import sys
import sqlite3
from PySyde2 import QtWidgets, QtCore, QtGui
from PySyde2.QtCore import QDate
from PySide2.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QGridLayout, QGroupBox, QVBoxLayout, QLineEdit, QLabel, QComboBox, QDateEdit)


names = ["თარიღი", "დასახელება", "რაოდენობა", "ზომის ერთეული", "ერთ.ფასი", "ჯამური ფასი"]

# მთავარი ფანჯარა
# მთავარი ფანჯარა
# მთავარი ფანჯარა

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Georgian Flowers - ქართული ყვავილები"
        self.setWindowIcon(QtGui.QIcon('ico.png'))
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.CreateLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)
        self.showMaximized()

    def CreateLayout(self):
        self.groupBox = QGroupBox()
        gridLayout = QGridLayout()
        self.table = self.createTable()
        gridLayout.addWidget(self.table, 0, 0, 1, 2)
        sum = 0
        for i in range(len(self.arr)-1):
            sum += int(self.arr[i][5])
        self.sum = QLabel(f"ჯამი: {sum}")
        self.sum.setAlignment(QtCore.Qt.AlignRight)
        self.sum.setFont(QtGui.QFont("", 14, QtGui.QFont.Bold))
        gridLayout.addWidget(self.sum, 1,0,1,2)
        self.button = QPushButton("დამატება", self)
        self.button.setMinimumHeight(50)
        self.button.clicked.connect(self.addingProduct)
        gridLayout.addWidget(self.button, 2, 0)
        self.button2 = QPushButton("რეალიზაცია", self)
        self.button2.setMinimumHeight(50)
        self.button2.clicked.connect(self.subtractingProduct)
        gridLayout.addWidget(self.button2, 2, 1)
        self.groupBox.setLayout(gridLayout)

    def createTable(self):
        self.tableWidget = QTableWidget()
        
        self.tableWidget.setColumnCount(len(names))
        self.open_db()
        self.tableWidget.setRowCount( len(self.arr) + 2 )
        self.setData()
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(names)
        return self.tableWidget

    
    def read_table(self,con):
        self.arr = []
        cur = con.cursor()
        cur.execute("SELECT * FROM List")
        rows = cur.fetchall()
        for row in rows:
            self.arr.append(row)
        cur.close()
    def open_db(self):
        try:
            con = sqlite3.connect("database.db")
            self.read_table(con)
        except sqlite3.Error as e:
            e = 1
    
    def setData(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                newitem = QTableWidgetItem(str(self.arr[i][j]))
                self.tableWidget.setItem(i, j, newitem)

    # დამატების ფუნქცია
    # დამატების ფუნქცია
    # დამატების ფუნქცია

    def addingProduct(self):
        self.adding = QWidget()
        self.adding.setWindowTitle('პროდუქტის დამატება')
        self.apCreateLayout()
        apvbox = QVBoxLayout()
        apvbox.addWidget(self.apGroupBox)
        self.adding.setLayout(apvbox)
        self.adding.show()

    def apCreateLayout(self):
        self.apGroupBox = QGroupBox()
        apGridLayout = QGridLayout()
        #apGridLayout.setSpacing(10)
        self.apDateLabel = QLabel("თარიღი")
        apGridLayout.addWidget(self.apDateLabel, 0, 0)
        self.apDateEdit = QDateEdit()
        self.apDateEdit.setDate(QDate.currentDate())
        self.apDateEdit.setDisplayFormat("yyyy-MM-dd")
        apGridLayout.addWidget(self.apDateEdit, 0, 1)
        self.apNameLabel = QLabel("დასახელება")
        apGridLayout.addWidget(self.apNameLabel, 1, 0)
        self.apNameLine = QLineEdit()
        apGridLayout.addWidget(self.apNameLine, 1, 1, 1, 2)
        self.apQuantityLabel = QLabel("რაოდენობა")
        apGridLayout.addWidget(self.apQuantityLabel, 2, 0)
        self.apQuantityLine = QLineEdit()
        self.apQuantityLine.setAlignment(QtCore.Qt.AlignRight)
        apGridLayout.addWidget(self.apQuantityLine, 2, 1)
        self.apTypeCombo = QComboBox()
        self.apTypeCombo.addItem("ცალი")
        self.apTypeCombo.addItem("კილოგრამი")
        self.apTypeCombo.addItem("გრამი")
        apGridLayout.addWidget(self.apTypeCombo, 2, 2)
        self.apOnePriceLabel = QLabel("ცალ. ფასი")
        apGridLayout.addWidget(self.apOnePriceLabel, 3, 0)
        self.apOnePriceLine = QLineEdit()
        self.apOnePriceLine.setAlignment(QtCore.Qt.AlignRight)
        apGridLayout.addWidget(self.apOnePriceLine, 3, 1, 1, 2)
        self.apPriceLabel = QLabel("ჯამ. ფასი")
        apGridLayout.addWidget(self.apPriceLabel, 4, 0)
        self.apPriceLine = QLineEdit()
        self.apPriceLine.setAlignment(QtCore.Qt.AlignRight)
        apGridLayout.addWidget(self.apPriceLine, 4, 1, 1, 2)
        self.apButton = QPushButton("დამატება", self)
        apGridLayout.addWidget(self.apButton, 5, 0, 1, 3)
        self.apButton.clicked.connect(self.addingData)
        self.apGroupBox.setLayout(apGridLayout)

    def addingData(self):
        date = self.apDateEdit.date().toPyDate()
        name = self.apNameLine.text()
        quantity = int(self.apQuantityLine.text())
        unit = self.apTypeCombo.currentText()
        eachprice = self.apOnePriceLine.text()
        sumprice = self.apPriceLine.text()
        
        try:
            sqliteConnection = sqlite3.connect('database.db')
            cursor = sqliteConnection.cursor()
            sqlite_insert_query =   f"""INSERT INTO List
                                    (Date, Name, Quantity, Unit, PricePer, PriceSum)
                                    VALUES
                                    ('{date}','{name}','{quantity}','{unit}','{eachprice}','{sumprice}')"""
            cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
            cursor.close()
        except sqlite3.Error as error:
            error = 1
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
        self.updateTableData()
        self.adding.close()
    def updateTableData(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount( len(self.arr) + 2 )
        self.open_db()
        self.setData()

    # რეალიზაციის ფუნქცია
    # რეალიზაციის ფუნქცია
    # რეალიზაციის ფუნქცია

    def subtractingProduct(self):
        self.subing = QWidget()
        self.subing.setWindowTitle('პროდუქტის რეალიზაცია')
        self.spCreateLayout()
        self.spvbox = QVBoxLayout()
        self.spvbox.addWidget(self.spGroupBox)
        self.subing.setLayout(self.spvbox)
        self.subing.show()

    def spCreateLayout(self):
        self.spGroupBox = QGroupBox()
        self.spGridLayout = QGridLayout()
        #spGridLayout.setSpacing(10)
        self.spButton = QPushButton("რეალიზაცია",self)
        self.spGridLayout.addWidget(self.spButton,0,0)
        self.spGroupBox.setLayout(self.spGridLayout)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
