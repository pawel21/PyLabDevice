from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QLineEdit, QLabel, QPlainTextEdit, QAction, QFileDialog, QLCDNumber, QSlider, QDialog
from PyQt5.QtCore import Qt, QObject, pyqtSlot

from MeasureDeviceConnect import MeasureDeviceConnect


class LdcSettingsWindow(QDialog, MeasureDeviceConnect):
    def __init__(self, parent=None):
        super(LdcSettingsWindow, self).__init__(parent)

        label_current_limit_info = QLabel("Laser current limit in mA", self)
        label_current_limit_info.move(80, 15)

        display_current_limit = QLCDNumber(self)
        display_current_limit.move(50, 40)
        display_current_limit.resize(180, 50)

        self.slider_to_change_current_limit = QSlider(Qt.Horizontal, self)
        self.slider_to_change_current_limit.move(250, 60)
        self.slider_to_change_current_limit.setMaximum(200)
        self.slider_to_change_current_limit.valueChanged.connect(display_current_limit.display)

        button_to_set_current_limit = QPushButton(self)
        button_to_set_current_limit.setText("Set current limit")
        button_to_set_current_limit.move(380, 40)
        button_to_set_current_limit.resize(150, 50)
        button_to_set_current_limit.clicked.connect(self.set_current_limit)

        try:
            display_current_limit.display(MeasureDeviceConnect.ldc.get_current_limit_in_amper()*1000)
        except Exception:
            pass

        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('Ldc settings')

    def set_current_limit(self):
        new_current_limit = self.slider_to_change_current_limit.value()
        MeasureDeviceConnect.ldc.set_current_limit_in_amper(float(new_current_limit/1000.0))
        print(str(new_current_limit))

    def slider_changed(self):
        print("Current dial value: %i" % (self.dial.value()))