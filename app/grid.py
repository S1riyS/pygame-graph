from pygame.math import Vector2

from config import Config


class Grid:
    def __init__(self):
        self.rows = Config.ROWS
        self.columns = Config.COLUMNS
        self.graph_width = (Config.WINDOW_WIDTH - (self.columns + 1) * Config.GRAPHS_PADDING) // self.columns
        self.graph_height = (Config.WINDOW_HEIGHT - (self.rows + 1) * Config.GRAPHS_PADDING) // self.rows

    def get_position(self, row: int, column: int) -> Vector2:
        x = row * Config.GRAPHS_PADDING + (row - 1) * self.graph_width
        y = column * Config.GRAPHS_PADDING + (column - 1) * self.graph_height

        return Vector2(x, y)
