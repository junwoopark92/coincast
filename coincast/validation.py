import numpy as np


class IsNotPositiveNumberException(Exception):
    pass


class VariableTypeException(Exception):
    pass


def is_positive_number(number):
    if type(number) is not int:
        raise VariableTypeException('Variable type expected int, but got '+type(number).__name__)

    if number > 0:
        return number

    raise IsNotPositiveNumberException('Number is not Positive')
