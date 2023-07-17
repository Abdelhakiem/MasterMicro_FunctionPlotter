import numpy as np
import pytest
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from equationSolver import EquationSolver
from function_plotter_gui import FunctionPlotter


@pytest.fixture
def window(qtbot):
    """
    Fixture to create and return the main window of the application.
    """
    win = FunctionPlotter()
    qtbot.addWidget(win)
    win.show()
    qtbot.wait_for_window_shown(win)
    return win




def test_initial_state(window):
    """
    Test the initial state of the GUI elements.
    """
    assert window.equation_editor.text() == ""
    assert window.equation_label.text() == "Enter the equation"
    assert window.plot_button.text() == "Plot"
    assert window.plot_button.isEnabled()
    assert window.min_value_editor.text() == ""
    assert window.min_value_label.text() == "Minimum Value"
    assert window.max_value_editor.text() == ""
    assert window.max_value_label.text() == "Maximum Value"


def test_valid_equation_and_boundaries(window, qtbot):
    """
    Test that a valid equation and boundaries result in a correct plot.
    """
    # Enter a valid equation, minimum value, and maximum value
    equation = "x^3-10*x^2+11"
    min_value = "-11"
    max_value = "10"
    window.equation_editor.setText(equation)
    window.min_value_editor.setText(min_value)
    window.max_value_editor.setText(max_value)

    # Click the plot button
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)

    # Check that the equation is displayed correctly
    X_values = np.linspace(float(min_value), float(max_value), 100)
    assert window.canvas.figure.axes[0].lines[0].get_xydata().tolist() == [[x, x ** 3 - 10 * x ** 2 + 11] for x in X_values]


def test_plot_figure(window):
    """
    Test that the plot_figure method displays the plot correctly.
    """
    # Create test data for x and y arrays
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])

    # Call the plot_figure method with the test data
    window.plot_figure(x, y)

    # Check that the plot is displayed correctly
    assert window.figure.axes[0].lines[0].get_xdata().tolist() == x.tolist()
    assert window.figure.axes[0].lines[0].get_ydata().tolist() == y.tolist()
    assert window.figure.axes[0].get_xlabel() == 'X-Axis'
    assert window.figure.axes[0].get_ylabel() == f"F(X) = {window.equation_editor.text()}"