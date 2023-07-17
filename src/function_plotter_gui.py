import sys
import numpy as np
from PySide2.QtWidgets import (
    QApplication, QWidget, QDesktopWidget, QPushButton, QMessageBox, QLabel, QVBoxLayout, QGroupBox, QGridLayout,
    QLineEdit
)
from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from equationSolver import EquationSolver

class FunctionPlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI of the window
        """
        def center_window():
            # Center the window on the screen
            q_rect = self.frameGeometry()
            center_point = QDesktopWidget().availableGeometry().center()
            q_rect.moveCenter(center_point)
            self.move(q_rect.topLeft())

        def set_icon():
            # Set the window icon
            app_icon = QIcon('../images/appIcon.png')
            self.setWindowIcon(app_icon)

        self.setWindowTitle("Function Plotter Window")
        self.setGeometry(300, 300, 800, 700)
        self.setMinimumWidth(700)
        self.setMaximumWidth(800)
        self.setMinimumHeight(650)
        self.setMaximumHeight(750)

        center_window()
        set_icon()
        self.create_widgets()
        self.create_box_layout()

    def create_widgets(self):
        """
        Create all the widgets for the UI
        """
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)

        self.equation_label = QLabel("Enter the equation", self)
        self.equation_label.setFont(QFont("Times New Roman", 13))
        self.equation_label.setStyleSheet("color:blue")

        self.plot_button = QPushButton("Plot", self)
        self.plot_button.setIcon(QIcon('../images/buttonIcon.jpg'))
        self.plot_button.setFont(QFont("Times New Roman", 13))
        self.plot_button.setStyleSheet("color:blue")
        self.plot_button.setIconSize(QSize(50, 60))
        self.plot_button.clicked.connect(self.plot_button_clicked)

        self.equation_editor = QLineEdit(self)
        self.equation_editor.setFont(QFont("Times New Roman", 14))
        self.equation_editor.setStyleSheet("color:black")

        self.min_value_editor = QLineEdit(self)
        self.min_value_editor.setFont(QFont("Times New Roman", 14))
        self.min_value_editor.setStyleSheet("color:black")

        self.max_value_editor = QLineEdit(self)
        self.max_value_editor.setFont(QFont("Times New Roman", 14))
        self.max_value_editor.setStyleSheet("color:black")

        self.min_value_label = QLabel("Minimum Value", self)
        self.min_value_label.setFont(QFont("Times New Roman", 14))
        self.min_value_label.setStyleSheet("color:blue")

        self.max_value_label = QLabel("Maximum Value", self)
        self.max_value_label.setFont(QFont("Times New Roman", 14))
        self.max_value_label.setStyleSheet("color:blue")

    def create_box_layout(self):
        """
        Create the box layout for organizing the widgets
        """
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)

        groupbox1 = QGroupBox("Enter required inputs: ")
        groupbox1.setFont(QFont("Times New Roman", 15))
        groupbox1.setStyleSheet("color:red")

        grid1 = QGridLayout()
        grid1.addWidget(self.equation_label, 0, 0)
        grid1.addWidget(self.equation_editor, 0, 1)
        grid1.addWidget(self.plot_button, 0, 2)
        groupbox1.setLayout(grid1)
        vbox.addWidget(groupbox1)

        groupbox2 = QGroupBox("")
        grid2 = QGridLayout()
        grid2.addWidget(self.min_value_label, 0, 0)
        grid2.addWidget(self.min_value_editor, 0, 1)
        grid2.addWidget(self.max_value_label, 0, 2)
        grid2.addWidget(self.max_value_editor, 0, 3)
        groupbox2.setLayout(grid2)
        vbox.addWidget(groupbox2)

        self.setLayout(vbox)

    def plot_button_clicked(self):
        """
        Handle the click event of the plot button
        """
        try:
            solver = EquationSolver(
                self.equation_editor.text(),
                self.min_value_editor.text(),
                self.max_value_editor.text()
            )
            x = solver.get_domain()
            y = solver.calc_range(x)
            self.plot_figure(x, y)
        except ValueError as e:
            self.show_error_message(str(e))
        except Exception as e:
            self.show_error_message(str(e))

    def plot_figure(self, x: np.ndarray, y: np.ndarray):
        """
        Plot the figure using the provided x and y values
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel('X-Axis')
        ax.set_ylabel('F(X) = '+self.equation_editor.text())
        ax.plot(x, y)
        self.canvas.draw()

    @staticmethod
    def show_error_message( message: str):
        """
        Show an error message box with the provided message
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle("Input Error")
        msg_box.exec_()


if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(myApp.exec_())

