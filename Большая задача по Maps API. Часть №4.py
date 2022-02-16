import os
import sys
import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow

from YandexMap import Ui_MainWindow

SCREEN_SIZE = [800, 800]


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.coords = [40.403477, 56.144662]
        self.lot = self.doubleSpinBox.value()
        self.lan = self.doubleSpinBox_2.value()
        self.coords.clear()
        self.coords.append(self.lot)
        self.coords.append(self.lan)
        self.type_map = 'map'
        self.spn = [0.05, 0.05]

        self.show_map()

        self.pixmap = QPixmap(self.map_file)
        self.label.setPixmap(self.pixmap)

      #  self.lineEdit.hide()
        self.label.focusWidget()

        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.type)

    def type(self):
       if self.type_map == "map":
           self.type_map = "sat"
       elif self.type_map == "sat":
           self.type_map = "skl"
       elif self.type_map == "skl":
           self.type_map = "map"

       self.show_map()
       self.pixmap.load('map.png')
       self.label.setPixmap(self.pixmap)

    def search(self):
        self.lot = self.doubleSpinBox.value()
        self.lan = self.doubleSpinBox_2.value()
        self.coords.clear()
        self.coords.append(self.lot)
        self.coords.append(self.lan)
        self.show_map()
        self.pixmap.load('map.png')
        self.label.setPixmap(self.pixmap)

    def show_map(self):
        maps_server = 'http://static-maps.yandex.ru/1.x/'

        map_params = {
            'll': str(self.coords[0]) + ',' + str(self.coords[1]),
            'spn': str(self.spn[0]) + ',' + str(self.spn[1]),
            'l': self.type_map}

        response = requests.get(maps_server, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def change_zoom(self, flag, coeff):
        spn2 = coeff
        if flag:
            spn2 = [spn2[0] * 2, spn2[1] * 2]
        else:
            spn2 = [spn2[0] / 2, spn2[1] / 2]
        return spn2

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn = self.change_zoom(True, self.spn)
            self.show_map()
            self.pixmap.load('map.png')
            self.label.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_PageDown:
            self.spn = self.change_zoom(False, self.spn)
            self.show_map()
            self.pixmap.load('map.png')
            self.label.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_W:
            self.coords = [self.coords[0], self.coords[1] + 0.05]
            self.show_map()
            self.pixmap.load('map.png')
            self.label.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_S:
            self.coords = [self.coords[0], self.coords[1] - 0.05]
            self.show_map()
            self.pixmap.load('map.png')
            self.label.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_A:
            self.coords = [self.coords[0] - 0.05, self.coords[1]]
            self.show_map()
            self.pixmap.load('map.png')
            self.label.setPixmap(self.pixmap)
        elif event.key() == Qt.Key_D:
            self.coords = [self.coords[0] + 0.05, self.coords[1]]
            self.show_map()
            self.pixmap.load('map.png')
            self.label.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())