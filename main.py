import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTableWidgetItem
)
from UI.main_ui import Ui_MainWindow
from UI.add_edit_ui import Ui_Form


DB_PATH = "data/coffee.sqlite"


class AddEditCoffeeForm(QWidget):
    def __init__(self, coffee_id=None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.coffee_id = coffee_id
        self.ui.saveButton.clicked.connect(self.save)

        if coffee_id is not None:
            self.load_data()

    def load_data(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        data = cursor.execute(
            "SELECT name, roast, ground, taste, price, volume "
            "FROM coffee WHERE id=?",
            (self.coffee_id,)
        ).fetchone()
        connection.close()

        self.ui.nameEdit.setText(data[0])
        self.ui.roastEdit.setText(data[1])
        self.ui.groundEdit.setText(data[2])
        self.ui.tasteEdit.setText(data[3])
        self.ui.priceEdit.setText(str(data[4]))
        self.ui.volumeEdit.setText(str(data[5]))

    def save(self):
        values = (
            self.ui.nameEdit.text(),
            self.ui.roastEdit.text(),
            self.ui.groundEdit.text(),
            self.ui.tasteEdit.text(),
            float(self.ui.priceEdit.text()),
            int(self.ui.volumeEdit.text())
        )

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        if self.coffee_id is None:
            cursor.execute(
                "INSERT INTO coffee "
                "(name, roast, ground, taste, price, volume) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                values
            )
        else:
            cursor.execute(
                "UPDATE coffee SET "
                "name=?, roast=?, ground=?, taste=?, price=?, volume=? "
                "WHERE id=?",
                values + (self.coffee_id,)
            )

        connection.commit()
        connection.close()
        self.close()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_table()
        self.ui.addButton.clicked.connect(self.add_coffee)
        self.ui.editButton.clicked.connect(self.edit_coffee)

    def load_table(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        data = cursor.execute("SELECT * FROM coffee").fetchall()
        connection.close()

        self.ui.tableWidget.setRowCount(len(data))

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                self.ui.tableWidget.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(str(value))
                )

    def add_coffee(self):
        self.form = AddEditCoffeeForm()
        self.form.show()
        self.form.destroyed.connect(self.load_table)

    def edit_coffee(self):
        row = self.ui.tableWidget.currentRow()
        if row < 0:
            return
        coffee_id = int(
            self.ui.tableWidget.item(row, 0).text()
        )
        self.form = AddEditCoffeeForm(coffee_id)
        self.form.show()
        self.form.destroyed.connect(self.load_table)


app = QApplication(sys.argv)
window = CoffeeApp()
window.show()
sys.exit(app.exec())