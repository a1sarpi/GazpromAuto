from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        canvas = FigureCanvas(fig)  # create canvas
        layout.addWidget(canvas)  # add canvas to layout


fig = Figure()
ax = fig.add_subplot()

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]
ax.plot(x, y)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())