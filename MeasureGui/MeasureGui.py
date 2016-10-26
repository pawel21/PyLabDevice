import sys
sys.path.insert(0, "/home/pawel1/Pulpit/PyLabDevice/Device")
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QLineEdit, QLabel, QPlainTextEdit, QAction, QFileDialog
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging
import numpy as np
import time
import thread
import shutil

from Device import Device


class BaseMeasureInfo:
    _DEFAULT_FMT = "%(asctime)s - %(levelname)s - %(message)s"
    logger = logging.getLogger(__name__)
    OUT_MSG = ""
    CURRENT_WAVELENGTH = ""

    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG,
            stream=sys.stdout,
            format=self._DEFAULT_FMT)


class MeasureDeviceConnect(BaseMeasureInfo):

    try:
        dev = Device()
        ldc = dev.get_ldc4005_instance()
        pm100 = dev.get_pm100_instance()
        BaseMeasureInfo.OUT_MSG += "Connections with device successful"
        BaseMeasureInfo.CURRENT_WAVELENGTH = str(pm100.get_current_wavelength_in_nm())
    except Exception as err:
        BaseMeasureInfo.logger.error(err)
        BaseMeasureInfo.OUT_MSG += ("Error %s" % err)


class Measure:

    @staticmethod
    def do_measure(start_current, stop_current, numbers_of_points):
        try:
            MeasureDeviceConnect.ldc.ld_current_in_A_setpoint(0)
            time.sleep(1)
            MeasureDeviceConnect.ldc.on()
            time.sleep(3)

            current = list()
            voltage = list()
            power = list()
            set_current_array = np.linspace(start_current, stop_current, numbers_of_points)

            for i in range(0, len(set_current_array)):
                MeasureDeviceConnect.ldc.ld_current_in_A_setpoint(str(set_current_array[i]))
                current.append(MeasureDeviceConnect.ldc.ld_current_reading())
                voltage.append(MeasureDeviceConnect.ldc.ld_voltage_reading())
                power.append(MeasureDeviceConnect.pm100.get_power())
                J = np.array(current, dtype=float)
                V = np.array(voltage, dtype=float)
                L = np.array(power, dtype=float)
                np.savetxt('data.txt', zip(J, V, L), fmt='%1.12e', header=' J [A] \t V \t L [w] ')
                time.sleep(0.1)
        except Exception as err:
                print(err)
        finally:
            MeasureDeviceConnect.ldc.off()


class App(QMainWindow, MeasureDeviceConnect):
    START_CURRENT = 0
    STOP_CURRENT = 0
    POINTS_TO_MEASURE = 0

    def __init__(self):
        super(App, self).__init__()
        self.left = 10
        self.top = 10
        self.title = 'Measure Laser'
        self.width = 1340
        self.height = 900
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.plot_canvas = PlotCanvas(self, width=10, height=6)
        self.plot_canvas.move(0, 0)
        self.matplotlib_toolbar = NavigationToolbar(self.plot_canvas, self)
        self.matplotlib_toolbar.move(300, 0)
        self.matplotlib_toolbar.resize(500, 50)

        buton_to_save_data = QPushButton("Save data", self)
        buton_to_save_data.clicked.connect(self.save_data)
        buton_to_save_data.move(1020, 100)
        buton_to_save_data.resize(140, 50)

        label_with_current_wavelength = QLabel('Current wavelength: ' + str(self.CURRENT_WAVELENGTH ) + " nm", self)
        label_with_current_wavelength.move(1020, 150)
        label_with_current_wavelength.resize(200, 80)

        button_to_start_measure = QPushButton('Start', self)
        button_to_start_measure.move(1020, 10)
        button_to_start_measure.resize(140, 50)
        button_to_start_measure.clicked.connect(self.click_to_start_measure)

        button_to_stop_measure = QPushButton('Stop', self)
        button_to_stop_measure.move(1180, 10)
        button_to_stop_measure.resize(140, 50)
        button_to_stop_measure.clicked.connect(self.click_to_stop_measure)

        button_to_set_start_current = QPushButton('Set start current [mA]', self)
        button_to_set_start_current.move(30, 650)
        button_to_set_start_current.resize(150, 30)
        button_to_set_start_current.clicked.connect(self.set_start_current)
        self.line_to_enter_start_current = QLineEdit(self)
        self.line_to_enter_start_current.setText("0")
        self.line_to_enter_start_current.move(200, 650)

        button_to_set_stop_current = QPushButton('Set stop current [mA]', self)
        button_to_set_stop_current.move(30, 700)
        button_to_set_stop_current.resize(150, 30)
        button_to_set_stop_current.clicked.connect(self.set_stop_current)
        self.line_to_enter_stop_current = QLineEdit(self)
        self.line_to_enter_stop_current.setText("0")
        self.line_to_enter_stop_current.move(200, 700)

        button_to_set_numer_of_points_to_measure = QPushButton('Set numer of points to measure', self)
        button_to_set_numer_of_points_to_measure.move(350, 650)
        button_to_set_numer_of_points_to_measure.resize(220, 30)
        button_to_set_numer_of_points_to_measure.clicked.connect(self.set_points_to_measure)
        self.POINTS_TO_MEASURE = 0
        self.line_to_enter_points_to_measure = QLineEdit(self)
        self.line_to_enter_points_to_measure.setText("0")
        self.line_to_enter_points_to_measure.move(600, 650)

        self.label_info = QPlainTextEdit(self)
        self.label_info.setReadOnly(True)
        self.label_info.move(100, 750)
        self.label_info.resize(500, 100)
        self.OUT_MSG += "\nPlease set parameters to measure"
        self.label_info.setPlainText(self.OUT_MSG)
        self.show()

    def click_to_start_measure(self):
        try:
            thread.start_new_thread(Measure.do_measure, (float(self.START_CURRENT)*1e-3, float(self.STOP_CURRENT)*1e-3,
                                                         float(self.POINTS_TO_MEASURE), ))
            self.OUT_MSG += "\nstart new measure"
            self.label_info.setPlainText(self.OUT_MSG)
        except Exception as err:
            print(err)
            print("Error, unable to start thread")

        time.sleep(4)
        self.plot_canvas.real_time_plot()

    def click_to_stop_measure(self):
        MeasureDeviceConnect.ldc.off()

    def set_start_current(self):
        self.START_CURRENT = self.line_to_enter_start_current.text()
        self.OUT_MSG = self.OUT_MSG + "\nstart current set to " + str(self.START_CURRENT) + " mA"
        self.label_info.setPlainText(self.OUT_MSG)

    def set_stop_current(self):
        self.STOP_CURRENT = self.line_to_enter_stop_current.text()
        self.OUT_MSG = self.OUT_MSG + "\nstop current set to " + str(self.STOP_CURRENT) + " mA"
        self.label_info.setPlainText(self.OUT_MSG)

    def set_points_to_measure(self):
        self.POINTS_TO_MEASURE = self.line_to_enter_points_to_measure.text()
        self.OUT_MSG = self.OUT_MSG + "\nnumbers of points to measure set to " + self.POINTS_TO_MEASURE
        self.label_info.setPlainText(self.OUT_MSG)

    def save_data(self):
        file_name_to_save = QFileDialog.getSaveFileName(self, 'Open file',
                                                        '', "Image files (*.txt )")
        shutil.copy("/home/pawel1/Pulpit/PyLabDevice/MeasureGui/data.txt", str(file_name_to_save[0]))


class PlotCanvas(FigureCanvas, BaseMeasureInfo):
    def __init__(self, parent=None, width=60, height=50, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def real_time_plot(self):
        ax1 = self.figure.add_subplot(1, 1, 1)
        ax2 = ax1.twinx()

        def animate(*args):
            try:
                current, voltage, power = np.loadtxt("data.txt", unpack=True, skiprows=1)
                ax1.clear()
                ax2.clear()
                ax1.plot(current, power, 'ro')
                ax2.plot(current, voltage, 'bo')
                ax1.set_xlabel("J [A]")
                ax1.set_ylabel('L [W]', color='r')
                ax2.set_ylabel('U [V]', color='b')
                plt.grid(True)
            except Exception as msg_error:
                self.OUT_MSG = self.OUT_MSG + "\n" + str(msg_error)
        ani = animation.FuncAnimation(self.figure, animate, interval=100)
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
