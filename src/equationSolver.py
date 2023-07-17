import re
from typing import List, Tuple, Union
import numpy as np
import sys
import os




class EquationSolver:
    """
    A class for validating and solving equation over a specific domain.
    """

    def __init__(self, equation: str, min_boundary: str, max_boundary: str):
        """
        Constructor for EquationSolver class.

        :param equation: the equation to be validated and solved.
        :param min_boundary: the lower limit value.
        :param max_boundary: the upper limit value.
        Raises:
        ValueError: If the equation or boundaries are invalid.
        """
        # validate the equation.
        valid_equation, error_messages = EquationSolver.__validate_equation(equation)
        if not valid_equation:
            raised_message="\n".join(error_messages)
            raise ValueError( f"Invalid equation:\n{raised_message}")
        #  validate the boundaries.
        valid_boundaries, error_message = EquationSolver.__validate_boundaries(min_boundary, max_boundary)
        if not valid_boundaries:
            raised_message="\n".join(error_messages)
            raise ValueError(f"Invalid boundaries:\n{error_message}")
        # Store the equation and boundaries as private attributes
        self.__equation = equation
        self.__min_boundary = float(min_boundary)
        self.__max_boundary = float(max_boundary)

    @staticmethod
    def __validate_boundaries(min_value: str, max_value: str) -> Tuple[bool, Union[None, str]]:
        """
        Static method to validate the boundaries of the range to be solved over.

        :param min_value: The minimum value of the range to be solved over.
        :param max_value:The maximum value of the range to be solved over.
        :return: A tuple containing a boolean indicating whether the boundaries are valid and an error message if applicable.
        """

        def is_number(value: str) -> bool:
            """
             An inner function to check if a given value is a number.

            :param value: The value to be checked.
            :return: True if the value is a number, False otherwise.
            """
            try:
                float(value)
                return True
            except ValueError:
                return False

        # Check if both boundaries are numeric values
        if is_number(min_value) and is_number(max_value):
            # Check if the maximum value is greater than the minimum value
            if float(max_value) > float(min_value):
                return True, None
            else:
                return False, ' -> Minimum value must be less than Maximum value'
        else:
            return False, ' -> Boundaries must be numeric values'

    @staticmethod
    def __validate_equation(equation: str) -> Tuple[bool, List[str]]:
        """
        Static method to validate the equation to be solved.

        :param equation:The equation to be solved.
        :return: A tuple containing a boolean indicating whether the equation is valid and a list of error messages if applicable.
        """
        errors = []
        equation = equation.lower().replace(' ', '')

        # Check whether the equation is empty or not.
        if len(equation) == 0:
            errors.append(' -> Equation is empty')
            return False, errors
        # Define a list of regular expression patterns and error messages
        pattern_checks = [
            (r'[a-wy-z]', ' -> Invalid variable'),
            (r'[^0-9a-z*^+-/]', ' -> Unsupported operator'),
            (r'[0-9]+x', ' -> Missing operator before variable x'),
            (r'x[0-9]', ' -> Missing operator after variable x'),
            (r'[*^+-/][*^+-/]', ' -> Two consecutive operators'),
            (r'/0', ' -> Division by zero')
        ]
        # Iterate through the list of patterns and check for matches in the equation string
        for pattern, error_msg in pattern_checks:
            pattern = re.compile(pattern)
            matches = pattern.findall(equation)
            # creating new list to drop duplicated mathces.
            clean_matches=list()
            [clean_matches.append(match) for match in matches if match not in clean_matches]
            if len(matches) > 0:
                errors.append(f'{error_msg}: {clean_matches}')

        return len(errors) == 0, errors

    def calc_range(self, x: np.ndarray) -> np.ndarray:
        """
        Calculates the range of the equation over the given domain.

        :param x: A numpy array representing the domain of the equation.
        :return: A numpy array representing the range of the equation over the given domain.
        """
        # Replace whitespace and '^' character with '**' the equivalent power operator in python.
        # Then, evaluate the equation
        equation = self.__equation.lower().replace(' ', '').replace('^', '**')
        # Return resultant range as numpy array.
        return np.array(eval(equation))

    def get_domain(self, num_elements: int = 100) -> np.ndarray:
        """
        Generates a numpy array representing the domain of the equation.

        :param num_elements: The number of elements in the domain array.
        :return: A numpy array representing the domain of the equation.
        """
        # Create a numpy array using the minimum and maximum boundaries and number of steps
        return np.linspace(float(self.__min_boundary), float(self.__max_boundary), num_elements)


