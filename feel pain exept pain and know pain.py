import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
            'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'э', 'ю', 'я', 'ё']


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('start menu.ui', self)  # Загружаем дизайн
        self.pushButton_add.clicked.connect(self.add_item)
        for i in self.buttonGroup.buttons():
            i.clicked.connect(self.run)

    def database(self, letter):
        con = sqlite3.connect("sorts_db.sqlite")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute(f"""SELECT * FROM sorts WHERE Sort like '{letter}%'""").fetchall()
        result.sort()
        for elem in result:
            print(*elem)
        con.close()

    def run(self):
        letter = self.sender().text()
        print(letter)
        self.database(letter)

    def add_item(self):
        # INSERT INTO sorts(Sort) VALUES('Балерина')
        print('Ok')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
