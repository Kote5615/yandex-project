import sys
import sqlite3
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
            'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'э', 'ю', 'я', 'ё']


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('start menu.ui', self)  # Загружаем дизайн
        # self.pushButton_add.clicked.connect(self.run)
        self.database()

    def database(self):
        letter = 'х'
        con = sqlite3.connect("sorts_db.sqlite")
        # Создание курсора
        cur = con.cursor()
        # Выполнение запроса и получение всех результатов
        result = cur.execute(f"""SELECT * FROM sorts WHERE Sort like '{letter}%'""").fetchall()
        # Вывод результатов на экран
        for elem in result:
            print(*elem)



        con.close()

    # def run(self):
    #     print("OK")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
