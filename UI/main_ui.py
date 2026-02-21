from PyQt5 import QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(800, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(10, 10, 780, 300)
        self.tableWidget.setColumnCount(7)

        self.addButton = QtWidgets.QPushButton(
            "Добавить", self.centralwidget
        )
        self.addButton.setGeometry(220, 330, 120, 40)

        self.editButton = QtWidgets.QPushButton(
            "Редактировать", self.centralwidget
        )
        self.editButton.setGeometry(360, 330, 120, 40)

        MainWindow.setCentralWidget(self.centralwidget)