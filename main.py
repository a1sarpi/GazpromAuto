import random
import sys

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow, QTableView, QHBoxLayout, QPushButton
from matplotlib.backends.backend_qtagg import (FigureCanvasQTAgg as FigureCanvas,
                                               NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class PlotWidget(QWidget):
    functions = {
        1 : np.sin,
        2 : np.cos,
    }

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.initUi()

    def initUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.navToolbar = NavigationToolbar(self.canvas, self)

        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addWidget(self.navToolbar)

    def plot(self):
        function_index = random.randint(1, 2)
        function = PlotWidget.functions[function_index]
        x = np.linspace(-10, 10, 2000)
        y = function(x)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#DCDCDC")

        ax.axhline(y=0, xmin=-10.25, xmax=10.25, color="#000000")
        ax.axvline(x=0, ymin=-2, ymax=2, color="#000000")

        ax.set_ylim([-2, 2])
        ax.set_xlim([-10.25, 10.25])

        if function == np.sin or function == np.cos:
            ax.axhline(y=1, xmin=-10.25, xmax=10.25, color='b', linestyle='--')
            ax.axhline(y=-1, xmin=-10.25, xmax=10.25, color='b', linestyle='--')

        ax.plot(x, y, linestyle='-.', color='#008000', label=function.__name__)
        ax.legend(loc="upper right")
        self.canvas.draw()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.connectUi()

    def initUi(self):
        self.centralWidget = QWidget(self)

        self.main_layout = QHBoxLayout(self.centralWidget)
        self.plot_layout = QVBoxLayout(self.centralWidget)
        self.button_layout = QHBoxLayout(self.centralWidget)

        self.table = QTableView()

        data = [
            [4, 9],
            [1, 0],
            [3, 5],
            [3, 3],
            [7, 8]
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.plotWidget = PlotWidget()

        self.plotButton = QPushButton("Plot")
        self.clearButton = QPushButton("Clear")

        self.plotButton.setStyleSheet("font-size: 12pt; font-weight: 530")
        self.clearButton.setStyleSheet("font-size: 12pt; font-weight: 530")

        self.button_layout.addWidget(self.plotButton)
        self.button_layout.addWidget(self.clearButton)

        self.plot_layout.addLayout(self.button_layout)
        self.plot_layout.addWidget(self.plotWidget)

        self.main_layout.addWidget(self.table)
        self.main_layout.addLayout(self.plot_layout)

        self.setCentralWidget(self.centralWidget)

    def connectUi(self):
        self.plotButton.clicked.connect(self.plotWidget.plot)
        self.clearButton.clicked.connect(self.clear)

    def clear(self):
        self.plotWidget.figure.clear()
        self.plotWidget.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
