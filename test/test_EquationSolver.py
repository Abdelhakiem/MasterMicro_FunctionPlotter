import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from equationSolver import EquationSolver

class TestEquationSolver:
    def test_init_valid(self):
        # Test object instantiation with valid parameters
        solver = EquationSolver("2*x + 3", "0", "10")

    def test_init_invalid_equation(self):
        # Test object instantiation with invalid equation parameter
        with pytest.raises(ValueError):
            solver = EquationSolver("", "0", "10")

        with pytest.raises(ValueError):
            solver = EquationSolver("2x + 3", "0", "10")

        with pytest.raises(ValueError):
            solver = EquationSolver("2*x + / 3", "0", "10")

    def test_init_invalid_boundaries(self):
        # Test object instantiation with invalid boundaries parameter
        with pytest.raises(ValueError):
            solver = EquationSolver("2*x + 3", "", "10")

        with pytest.raises(ValueError):
            solver = EquationSolver("2*x + 3", "0", "-10")

        with pytest.raises(ValueError):
            solver = EquationSolver("2*x + 3", "a", "b")

    def test_validate_boundaries(self):
        # Test validate_boundaries method with valid parameters
        assert EquationSolver._EquationSolver__validate_boundaries("0", "10") == (True, None)

        # Test validate_boundaries method with invalid parameters
        assert EquationSolver._EquationSolver__validate_boundaries("", "") == (False, " -> Boundaries must be numeric values")
        assert EquationSolver._EquationSolver__validate_boundaries("a", "b") == (False, " -> Boundaries must be numeric values")
        assert EquationSolver._EquationSolver__validate_boundaries("10", "0") == (False, " -> Minimum value must be less than Maximum value")

    def test_validate_equation(self):
        # Test empty equation
        assert EquationSolver._EquationSolver__validate_equation("") == (False, [" -> Equation is empty"])

        # Test equation with invalid variable
        assert EquationSolver._EquationSolver__validate_equation("y^2 + 2*y + 1") == (False, [" -> Invalid variable: ['y']"])

        # Test equation with unsupported operator
        assert EquationSolver._EquationSolver__validate_equation("x^2 % 2*x & 1") == (False, [" -> Unsupported operator: ['%', '&']"])

        # Test equation with missing operator
        assert EquationSolver._EquationSolver__validate_equation("2x 3") == (
        False, [" -> Missing operator before variable x: ['2x']", " -> Missing operator after variable x: ['x3']"])
        # Test equation with consecutive operators
        assert EquationSolver._EquationSolver__validate_equation("x^2 ++ 2*x + 1") == (False, [" -> Two consecutive operators: ['++']"])

        # Test equation with division by zero
        assert EquationSolver._EquationSolver__validate_equation("x / 0") == (False, [" -> Division by zero: ['/0']"])
    def test_calc_range(self):
        # Test calc_range method with valid parameters
        solver = EquationSolver("2*x + 3", "0", "10")
        x = np.array([0, 1, 2])
        assert (solver.calc_range(x) == np.array([3, 5, 7])).all()

    def test_get_domain(self):
        # Test get_domain method with valid parameters
        solver = EquationSolver("2*x + 3", "0", "10")
        assert (solver.get_domain(num_elements=3) == np.array([0., 5., 10.])).all()





if __name__ == '__main__':
    pytest.main()