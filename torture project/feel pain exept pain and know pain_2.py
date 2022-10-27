import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QMessageBox

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
            'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'э', 'ю', 'я', 'ё']


def database(letter):
    con = sqlite3.connect("sorts_db.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM sorts WHERE name_of_sort like '{letter}'""").fetchall()
    return result

class StartMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        window = uic.loadUi('start menu.ui', self)
        window.setWindowTitle("органайзер садовода")
        self.pushButton_add.clicked.connect(self.openAddItem)
        for i in self.buttonGroup.buttons():
            i.clicked.connect(self.run)

    def database(self, letter):
        con = sqlite3.connect("sorts_db.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM sorts WHERE name_of_sort like '{letter}%'""").fetchall()

        result.sort()
        for elem in result:
            print(*elem)
        con.close()

    def run(self):
        letter = self.sender().text()
        print(letter)
        self.database(letter)

    def openAddItem(self):
        print('Ok')
        self.open = AddItem()
        self.open.show()
        self.hide()


class AddItem(QWidget):
    def __init__(self):
        super().__init__()
        window = uic.loadUi('asd.ui', self)
        window.setWindowTitle("органайзер садовода")
        self.addButton.clicked.connect(self.add)

    def add(self):
        name_of_sort = self.name_of_sort.text().strip().capitalize()
        note = self.note.toPlainText().strip()
        description = self.description.toPlainText().strip()
        con = sqlite3.connect("sorts_db.sqlite")
        cur = con.cursor()

        if name_of_sort != '' and description != '':
            if name_of_sort[0].lower() in alphabet and database(name_of_sort) == []:
                print(name_of_sort, note, description)
                cur.execute(
                    f"INSERT INTO sorts(name_of_sort, description, note) VALUES('{name_of_sort}','{description}', '{note}')").fetchall()
                con.commit()
                con.close()
                self.openStartMenu()
            else:
                self.show_info_messagebox()
        else:
            print('hm')
            self.show_info_messagebox()

    def show_info_messagebox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Введите корректное значение названия и описания сорта")
        msg.setWindowTitle("ВНИМАНИЕ")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()



    def openStartMenu(self):
        print('Ok')
        self.open = StartMenu()
        self.open.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartMenu()
    ex.show()
    sys.exit(app.exec())