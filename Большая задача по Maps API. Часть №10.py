import math
import os
import sys
import requests
import geospn

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
        self.zoom = 12

        self.spisok = []

        self.flag_metka = False
        self.metka_coord = []

        self.show_map()

        self.pixmap = QPixmap(self.map_file)
        self.label.setPixmap(self.pixmap)

        self.pushButton.clicked.connect(self.search_coord)
        self.pushButton_2.clicked.connect(self.type)
        self.pushButton_3.clicked.connect(self.search_adress)
        self.pushButton_4.clicked.connect(self.reset_map)
        self.checkBox.stateChanged.connect(self.search_adress)

        self.setFocus()
        self.label.installEventFilter(self)

    def setFocus(self):
        self.setFocusPolicy(Qt.StrongFocus)

    def eventFilter(self, object, event):
        if object == self.label and event.type() == 2:
            mouse = list(map(float, str(event.pos()).split('(')[1][:-1].split(',')))
            self.clickMouse(mouse)
        return super(QMainWindow, self).eventFilter(object, event)

    def clickMouse(self, coords_mouse):
        self.delta_x = coords_mouse[0] - 300
        self.delta_y = 225 - coords_mouse[1]
        self.lot_temp = self.coords[0] + self.delta_x * 0.0000428 * math.pow(2, 15 - self.zoom)
        self.lan_temp = self.coords[1] + self.delta_y * 0.0000428 * math.cos(math.radians(self.coords[1])) * math.pow(2, 15 - self.zoom)

        self.spisok.clear()
        self.spisok.append(str(self.lot_temp))
        self.spisok.append(str(self.lan_temp))

        self.doubleSpinBox.setValue(float(self.spisok[0]))
        self.doubleSpinBox_2.setValue(float(self.spisok[1]))

        self.zapros = ','.join(self.spisok)
        self.lineEdit.setText(str(self.zapros))

        self.coords.clear()
        self.coords.append(self.lot_temp)
        self.coords.append(self.lan_temp)
        self.draw_map_2()

        self.search_adress()

    def draw_map(self):
        self.metka_coord = self.coords
        self.show_map()
        self.pixmap.load('map.png')
        self.label.setPixmap(self.pixmap)

    def draw_map_2(self):
        self.metka_coord = self.coords
        self.show_map_2()
        self.pixmap.load('map.png')
        self.label.setPixmap(self.pixmap)

    def reset_map(self):
        self.coords = [40.403477, 56.144662]
        self.zoom = 12
        self.lineEdit.clear()
        self.flag_metka = False
        self.label_2.setText('')
        self.draw_map()

    def type(self):
       if self.type_map == "map":
           self.type_map = "sat"
       elif self.type_map == "sat":
           self.type_map = "skl"
       elif self.type_map == "skl":
           self.type_map = "map"
       self.draw_map()

    def search_coord(self):
        self.lot = self.doubleSpinBox.value()
        self.lan = self.doubleSpinBox_2.value()
        self.coords.clear()
        self.coords.append(self.lot)
        self.coords.append(self.lan)
        self.draw_map()

    def search_adress(self):
        self.adress = self.lineEdit.text()
        if self.adress:
            self.coords[0], self.coords[1] = geospn.llspan(self.adress)
            if self.checkBox.isChecked():
                self.adres = geospn.post(self.adress)
            else:
                self.adres = geospn.adres(self.adress)
            self.label_2.setText(self.adres)
        else:
            self.lot = str(self.doubleSpinBox.value())
            self.lan = str(self.doubleSpinBox_2.value())
            self.spisok.clear()
            self.spisok.append(self.lot)
            self.spisok.append(self.lan)
            self.zapros2 = ','.join(self.spisok)
            if self.checkBox.isChecked():
                self.zapros2 = geospn.post(str(self.zapros2))
            else:
                self.zapros2 = geospn.adres(str(self.zapros2))
            self.label_2.setText(self.zapros2)

        self.metka_coord = self.coords
        self.flag_metka = True
        self.draw_map_2()

    def show_map(self):
        maps_server = 'http://static-maps.yandex.ru/1.x/'

        map_params = {
            'll': str(self.coords[0]) + ',' + str(self.coords[1]),
            'z': self.zoom,
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

        self.lineEdit.clear()
        self.doubleSpinBox.setValue(float(self.coords[0]))
        self.doubleSpinBox_2.setValue(float(self.coords[1]))

    def show_map_2(self):
        maps_server = 'http://static-maps.yandex.ru/1.x/'

        ll = str(self.coords[0]) + ',' + str(self.coords[1])
        metka = str(self.metka_coord[0]) + ',' + str(self.metka_coord[1])

        map_params = {
            'll': f"{ll}",
            'z': self.zoom,
            'l': self.type_map,
            "pt": f"{metka},pm2dgl"}

        response = requests.get(maps_server, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.lineEdit.clear()
        self.doubleSpinBox.setValue(float(self.coords[0]))
        self.doubleSpinBox_2.setValue(float(self.coords[1]))

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.zoom < 18:
            self.zoom += 1
            if self.flag_metka:
                self.draw_map_2()
            else:
                self.draw_map()

        elif event.key() == Qt.Key_PageDown and self.zoom > 2:
            self.zoom -= 1
            if self.flag_metka:
                self.draw_map_2()
            else:
                self.draw_map()

        elif event.key() == Qt.Key_W:
            self.coords = [self.coords[0], self.coords[1] + 0.05]
            if self.flag_metka:
                self.draw_map_2()
            else:
                self.draw_map()

        elif event.key() == Qt.Key_S:
            self.coords = [self.coords[0], self.coords[1] - 0.05]
            if self.flag_metka:
                self.draw_map_2()
            else:
                self.draw_map()

        elif event.key() == Qt.Key_A:
            self.coords = [self.coords[0] - 0.05, self.coords[1]]
            if self.flag_metka:
                self.draw_map_2()
            else:
                self.draw_map()

        elif event.key() == Qt.Key_D:
            self.coords = [self.coords[0] + 0.05, self.coords[1]]
            if self.flag_metka:
                self.draw_map_2()
            else:
                self.draw_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())