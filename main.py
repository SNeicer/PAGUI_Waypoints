import sys
from PyQt6.QtCore import Qt
import keyboard
from PyQt6 import QtWidgets, uic
import pyautogui as pag


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('main_v1.ui', self)
        self.last_id = 0
        self.is_capturing = False
        self.show()

        self.btn_clear.clicked.connect(self.clear_waypoints)
        self.cbox_activate.checkStateChanged.connect(self.change_capture_state)
        self.list_waypoints.itemClicked.connect(self.waypoint_data_to_clipboard)

    def clear_waypoints(self) -> None:
        info_box = QtWidgets.QMessageBox()
        u_answer = info_box.warning(self, 'Are you sure?', 'This will delete all saved waypoints!', QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if u_answer == QtWidgets.QMessageBox.StandardButton.Yes:
            self.list_waypoints.clear()
            self.last_id = 0
            self.statusBar().showMessage('Waypoints cleared!')

    def change_capture_state(self, capture_state) -> None:
        if capture_state == Qt.CheckState.Checked:
            self.is_capturing = True
        else:
            self.is_capturing = False

    def add_waypoint(self, some_bs_idk) -> None:
        if self.is_capturing:
            item_data_str = f'{self.last_id} - {pag.position().x}, {pag.position().y}'
            self.list_waypoints.addItem(item_data_str)
            self.statusBar().showMessage(f'Item {self.last_id} added!')
            self.last_id += 1
        else:
            self.statusBar().showMessage('Capturing is disabled!')

    def waypoint_data_to_clipboard(self, item: QtWidgets.QListWidgetItem) -> None:
        splitted_data = item.text().split(' - ')
        QtWidgets.QApplication.clipboard().setText(splitted_data[1])
        self.statusBar().showMessage(f'Waypoint {splitted_data[0]} with cords ({splitted_data[1]}) copied to clipboard!')

app = QtWidgets.QApplication(sys.argv)
MWindow = MainWindow()
keyboard.on_press_key('q', MWindow.add_waypoint)
app.exec()