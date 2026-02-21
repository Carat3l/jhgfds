import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem
)


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.tableWidget.setEditTriggers(
            self.tableWidget.NoEditTriggers
        )
        self.load_table()

    def load_table(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        data = cursor.execute(
            "SELECT * FROM coffee"
        ).fetchall()
        connection.close()

        self.tableWidget.setRowCount(len(data))

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                self.tableWidget.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(str(value))
                )


app = QApplication(sys.argv)
window = CoffeeApp()
window.show()
sys.exit(app.exec())