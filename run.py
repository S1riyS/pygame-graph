import math

from main import PygameGraph


def func(x: float) -> float:
    return math.sin(x)


if __name__ == '__main__':
    app = PygameGraph(function=func, scale=40)
    app.run()
