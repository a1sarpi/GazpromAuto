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
    dataChangedSignal = QtCore.pyqtSignal()

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = float(value)
            self.dataChangedSignal.emit()
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class ExtendedTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(ExtendedTableModel, self).__init__()
        self._data = data
        self._sum_data = self.calculate_sums()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._sum_data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._sum_data)

    def columnCount(self, index):
        return 2

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "X"
                elif section == 1:
                    return "Sum(Y)"
            elif orientation == Qt.Vertical:
                return str(section + 1)

    def calculate_sums(self):
        unique_x = np.unique([row[0] for row in self._data])
        sums = []
        for x in unique_x:
            y_sum = sum([row[1] for row in self._data if row[0] == x])
            sums.append([x, y_sum])
        return sums


class PlotWidget(QWidget):
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

    def plot(self, data):
        data = np.transpose(data)
        x = data[0]
        y = data[1]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#DCDCDC")

        ax.plot(x, y, linestyle='-.', color='#008000', label="Function")
        ax.legend(loc="upper right")
        self.canvas.draw()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = [
            [1, 2],
            [2, 1],
            [3, 2],
            [4, 1],
            [5, 2]
        ]

        self.initUi()
        self.connectUi()
        self.update_plot()

    def initUi(self):
        self.centralWidget = QWidget(self)

        self.main_layout = QHBoxLayout(self.centralWidget)
        self.tables_layout = QVBoxLayout(self.centralWidget)
        self.plot_layout = QVBoxLayout(self.centralWidget)
        self.button_layout = QHBoxLayout(self.centralWidget)

        self.table = QTableView()
        self.sumTable = QTableView()

        self.create_models()
        self.set_table_settings()

        self.model = TableModel(self.data)
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

        self.tables_layout.addWidget(self.table)
        self.tables_layout.addWidget(self.sumTable)

        self.main_layout.addLayout(self.tables_layout)
        self.main_layout.addLayout(self.plot_layout)

        self.setCentralWidget(self.centralWidget)

    def create_models(self):
        self.model = TableModel(self.data)
        self.sum_model = ExtendedTableModel(self.data)

    def set_table_settings(self):
        self.table.setModel(self.model)
        self.sumTable.setModel(self.sum_model)

    def connectUi(self):
        # ... (existing connections)
        self.model.dataChangedSignal.connect(self.update_data)

    def update_plot(self):
        self.plotWidget.plot(self.model._data)

    def update_data(self):
        self.sum_model = ExtendedTableModel(self.model._data)
        self.sumTable.setModel(self.sum_model)

    def connectUi(self):
        self.plotButton.clicked.connect(self.update_plot)
        self.clearButton.clicked.connect(self.clear)
        self.model.dataChanged.connect(self.update_plot)
        self.model.dataChangedSignal.connect(self.update_data)

    def clear(self):
        self.plotWidget.figure.clear()
        self.plotWidget.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
