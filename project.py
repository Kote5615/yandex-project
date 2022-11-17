import sys
import sqlite3
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QMessageBox, QScrollArea, QVBoxLayout, \
    QPushButton, QLineEdit, QButtonGroup, QAbstractButton
from PyQt5.QtGui import QPixmap
# from PyQt5.QtWinExtras import QWinTaskbarButton, QWinTaskbarProgress

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
            'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'э', 'ю', 'я', 'ё']


def database(word):
    con = sqlite3.connect("sorts_db.sqlite")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM sorts WHERE name_of_sort like '{word}'""").fetchall()
    return result


class StartMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        window = uic.loadUi('start menu.ui', self)
        window.setFixedSize(951, 248)

        window.setWindowTitle("органайзер садовода")
        self.pushButton_add.clicked.connect(self.openAddItem)
        self.search.clicked.connect(self.openSearch)
        self.info.clicked.connect(self.information)
        enabled_buttons = []
        con = sqlite3.connect("sorts_db.sqlite")
        cur = con.cursor()
        for i in alphabet:
            result = cur.execute(f"""SELECT name_of_sort FROM sorts WHERE name_of_sort like '{i}%'""").fetchall()
            if result == []:
                enabled_buttons.append(i)

        for i in self.buttonGroup.buttons():
            if i.text().lower() in enabled_buttons:
                i.setEnabled(False)
            i.clicked.connect(self.run)



    def information(self):
        AddItem.main = Info()
        AddItem.main.show()
        self.hide()

    def run(self):
        letter = self.sender().text().lower()
        print(letter)
        self.openSearch_letter(letter)

    def openAddItem(self):
        self.open = AddItem()
        self.open.show()
        self.hide()

    def openSearch(self):
        self.open = Search()
        self.open.show()
        self.hide()

    def openSearch_letter(self, letter):
        self.open = Search(letter)
        self.open.show()
        self.hide()


class AddItem(QWidget):
    def __init__(self, *sort, original=True):
        super().__init__()
        window = uic.loadUi('add.ui', self)
        window.setFixedSize(405, 295)
        window.setWindowTitle("органайзер садовода")
        self.original = original
        self.addButton.clicked.connect(self.add)
        self.cancel.clicked.connect(self.close)
        self.sort = str(*sort)
        if original is False:
            print('hm')
            data = database(*sort)
            self.name_of_sort.setText(str(*sort).capitalize())
            self.description.appendPlainText(data[0][1])
            self.note.appendPlainText(data[0][2])

    def add(self):
        name_of_sort = self.name_of_sort.text().strip().lower()
        note = self.note.toPlainText().strip()
        description = self.description.toPlainText().strip()
        con = sqlite3.connect("sorts_db.sqlite")
        cur = con.cursor()
        if name_of_sort != '' and description != '':
            if name_of_sort[0].lower() in alphabet and len(name_of_sort) <= 20:
                if self.original is True:
                    if database(name_of_sort) == []:
                        print(name_of_sort, note, description)
                        if note != '':
                            cur.execute(
                                f"INSERT INTO sorts(name_of_sort, description, note) VALUES('{name_of_sort}','{description}', '{note}')").fetchall()
                            con.commit()
                            con.close()
                            self.close()
                        else:
                            cur.execute(
                                f"INSERT INTO sorts(name_of_sort, description) VALUES('{name_of_sort}','{description}')").fetchall()
                            con.commit()
                            con.close()
                            self.close()
                    else:
                        self.show_info_messagebox('Такой сорт уже есть')
                else:
                    if note == '':
                        cur.execute(
                            f"UPDATE sorts SET description = '{description}' WHERE name_of_sort = '{self.sort}'").fetchall()
                        cur.execute(
                            f"UPDATE sorts SET note = '{note}' WHERE name_of_sort = '{self.sort}'").fetchall()
                        cur.execute(
                            f"UPDATE sorts SET name_of_sort = '{name_of_sort}' WHERE name_of_sort = '{self.sort}'").fetchall()
                        con.commit()
                        con.close()
                        self.close()
                    else:
                        cur.execute(
                            f"UPDATE sorts SET description = '{description}' WHERE name_of_sort = '{self.sort}'").fetchall()
                        cur.execute(
                            f"UPDATE sorts SET note = '{note}' WHERE name_of_sort = '{self.sort}'").fetchall()
                        cur.execute(
                            f"UPDATE sorts SET name_of_sort = '{name_of_sort}' WHERE name_of_sort = '{self.sort}'").fetchall()
                        con.commit()
                        con.close()
                        self.close()
            else:
                self.show_info_messagebox(
                    'Название сорта должно начинаться с буквы на кириллице и быть не больше 20 символов')
        else:
            self.show_info_messagebox('Поля название и описание не могут оставаться пустыми')

    def show_info_messagebox(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("ВНИМАНИЕ")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()

    def close(self):
        AddItem.main = StartMenu()
        AddItem.main.show()
        self.hide()


class Search(QScrollArea):
    def __init__(self, *letter):
        super(Search, self).__init__()

        if letter != ():
            self.databasebyletter(*letter)
        else:
            self.initUISearch()

    def databasebyletter(self, letter):
        sp = []
        con = sqlite3.connect("sorts_db.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT name_of_sort FROM sorts WHERE name_of_sort like '{letter}%'""").fetchall()
        result.sort()
        for elem in result:
            sp.append(*elem)
            print(*elem)
        con.close()
        self.initUIAlfabet(sp, letter)

    def initUIAlfabet(self, sp, letter):
        self.setGeometry(500, 300, 400, 300)
        self.setFixedSize(400, 300)
        self.setWindowTitle(f"все сорта на букву {letter}")
        widget = QWidget()
        # self.btn_sp.clear()
        self.btn = []
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(50, 30, 50, 25)
        # for i in sp:
        #     layout.addWidget(QPushButton(i.capitalize()))
        for i in sp:
            print(i)
            btn = QPushButton(i, self)
            self.btn.append(btn)

            for j in self.btn:
                layout.addWidget(j)

        for i in self.btn:
            i.clicked.connect(self.open)

        cancelbtn = QPushButton(self)
        cancelbtn.setFont(QtGui.QFont("Times", 9))
        cancelbtn.setText('Вернуться')
        cancelbtn.move(10, 20)
        cancelbtn.clicked.connect(self.close)
        self.setWidget(widget)
        self.setWidgetResizable(True)

    def initUISearch(self):
        self.widget = QWidget()
        self.cs_group = QButtonGroup(self.widget)
        self.layout = QVBoxLayout(self.widget)
        self.layout.setContentsMargins(50, 90, 50, 10)
        self.setGeometry(500, 300, 400, 300)
        self.setFixedSize(400, 300)
        self.setWindowTitle('Поиск')
        self.setWidget(self.widget)
        self.setWidgetResizable(True)

        self.SearchWindow = QLineEdit(self)
        self.SearchWindow.resize(150, 25)
        self.SearchWindow.move(120, 50)

        self.label = QLabel(self)
        self.label.setFont(QtGui.QFont("Times", 9))
        self.label.setText('Введите поисковой запрос')
        self.label.move(120, 30)

        cancelbtn = QPushButton(self)
        cancelbtn.setFont(QtGui.QFont("Times", 9))
        cancelbtn.setText('Вернуться')
        cancelbtn.move(10, 30)
        cancelbtn.clicked.connect(self.close)
        self.btn_sp = []
        self.SearchWindow.textChanged.connect(self.databaseforsearching)
        self.SearchWindow.textChanged.connect(self.showResult)

    def databaseforsearching(self):
        data = self.SearchWindow.text().strip().lower()
        con = sqlite3.connect("sorts_db.sqlite")
        cur = con.cursor()
        self.result = cur.execute(f"""SELECT name_of_sort FROM sorts WHERE name_of_sort like '%{data}%'""").fetchall()
        self.result.sort()
        # print(self.result)

    def close(self):
        Search.main = StartMenu()
        Search.main.show()
        self.hide()

    def showResult(self):
        for i in reversed(range(self.layout.count())):
            widgetToRemove = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
            self.btn_sp.clear()
        self.buttons = self.widget.findChildren(QAbstractButton)
        print(self.buttons)
        for i in self.result:
            a = i[0]
            btn = QPushButton(a, self)
            self.btn_sp.append(btn)

            for j in self.btn_sp:
                self.layout.addWidget(j)

        for i in self.btn_sp:
            i.clicked.connect(self.open)

    def open(self):
        sort = self.sender().text()
        AddItem.main = SearchResult(sort)
        AddItem.main.show()
        self.hide()


class SearchResult(QWidget):
    def __init__(self, *sort):
        super().__init__()
        self.sort = str(*sort)
        window = uic.loadUi('sort.ui', self)
        window.setFixedSize(563, 414)
        window.setWindowTitle('Органайзер садовода')
        self.label = QLabel(self)
        self.label.setFont(QtGui.QFont("Times", 9))
        self.label.setText(self.sort.capitalize())
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.resize(250, 20)
        self.label.setStyleSheet("background-color:#d8d8d8")
        self.label.move(160, 20)

        info = database(str(*sort))

        self.description.setText(info[0][1])
        if info[0][2] != [(None,)]:
            self.note.setText(info[0][2])

        self.cancel.clicked.connect(self.close)
        self.delete_2.clicked.connect(self.delete)
        self.change.clicked.connect(self.change_item)

    def delete(self):
        valid = QMessageBox.question(
            self, '', "удалить сорт?",
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            con = sqlite3.connect("sorts_db.sqlite")
            cur = con.cursor()
            cur.execute(f"DELETE FROM sorts WHERE name_of_sort == '{self.sort}'")
            con.commit()
            self.close()

    def close(self):
        Search.main = StartMenu()
        Search.main.show()
        self.hide()

    def change_item(self):
        Search.main = AddItem(self.sort, original=False)
        Search.main.show()
        self.hide()


class Info(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(500, 300)
        self.setWindowTitle('О программе')
        line = QVBoxLayout()
        self.setLayout(line)
        text_info = QLabel(self)
        # label = QLabel('This is label')
        file = open("info.txt", encoding='UTF-8')
        # print(file.read())
        text_info.setText(file.read())
        text_info.setFont(QtGui.QFont("Times", 11))
        text_info.setWordWrap(True)
        line.addWidget(text_info)
        file.close()

        cancelbtn = QPushButton(self)
        cancelbtn.setFont(QtGui.QFont("Times", 9))
        cancelbtn.setText('Вернуться')
        cancelbtn.move(340, 200)
        cancelbtn.clicked.connect(self.close)

        label = QLabel(self)
        label.setFixedSize(58, 60)
        label.move(10, 10)
        pixmap = QPixmap('img.jpg')
        label.setPixmap(pixmap)


    def close(self):
        Info.main = StartMenu()
        Info.main.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    ex = StartMenu()
    ex.show()
    sys.exit(app.exec())
