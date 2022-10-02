import math

from app import Application
from app.types import Function

FUNCTIONS = (
    Function(function=lambda x: -x ** 2, left_x=-2, right_x=2),
    Function(function=lambda x: (x + 5) ** 2, left_x=-8, right_x=2),
    Function(function=lambda x: -(x - 3) ** 2 + 4, left_x=0.5, right_x=5.5),
    Function(function=lambda x: (x + 4) ** 2 - 4, left_x=-6.5, right_x=-1.5),
    Function(function=lambda x: -(x + 2) ** 2 + 3, left_x=-4.5, right_x=0.5),
    Function(function=lambda x: -(x - 6) ** 2, left_x=3.5, right_x=8.5),
    Function(function=lambda x: math.cos(x))
)

if __name__ == '__main__':
    app = Application(functions=FUNCTIONS, initial_scale=40)
    app.run()
