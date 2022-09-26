import typing as t

import pygame
from pygame.math import Vector2

from config import Config


class Function(t.NamedTuple):
    function: t.Callable
    left_x: t.Optional[float] = None
    right_x: t.Optional[float] = None


class PygameGraph:
    def __init__(self, functions: t.Iterable[Function], initial_scale: int):
        pygame.init()
        self.functions = functions
        self.graph_scale = initial_scale

        self.WIDTH = Config.WINDOW_WIDTH
        self.HEIGHT = Config.WINDOW_HEIGHT
        self.GRAPH_CENTER = Vector2(self.WIDTH // 2, self.HEIGHT // 2)
        self.COLORS = (
            pygame.Color(255, 0, 0),
            pygame.Color(0, 255, 0),
            pygame.Color(0, 0, 255),
            pygame.Color(25, 25, 25),
            pygame.Color(255, 0, 255),
            pygame.Color(0, 255, 255),
            pygame.Color(236, 123, 45),
            pygame.Color(35, 35, 35),
            pygame.Color(123, 123, 123),
        )

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True

        pygame.display.set_caption('Pygame graph')

    def run(self) -> None:
        while self.running:
            self.screen.fill(Config.WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.graph_scale += Config.ZOOM_VALUE
                    elif event.button == 5:
                        self.graph_scale -= Config.ZOOM_VALUE

            self.__normalize_graph_scale()
            self.__draw_coordinate_plane()
            for function, color in zip(self.functions, self.COLORS):
                self.__draw_function(function, color)

            pygame.display.flip()

        pygame.quit()

    def __normalize_graph_scale(self) -> None:
        self.graph_scale = min(max(self.graph_scale, Config.MIN_ZOOM), Config.MAX_ZOOM)

    def __draw_coordinate_plane(self) -> None:
        # Drawing horizontal and vertical lines
        pygame.draw.line(
            self.screen,
            Config.BLACK,
            (Config.DIVIDING_STRIPES_OFFSET, self.GRAPH_CENTER.y),
            (self.WIDTH - Config.DIVIDING_STRIPES_OFFSET, self.GRAPH_CENTER.y)
        )
        pygame.draw.line(
            self.screen,
            Config.BLACK,
            (self.GRAPH_CENTER.x, Config.DIVIDING_STRIPES_OFFSET),
            (self.GRAPH_CENTER.x, self.HEIGHT - Config.DIVIDING_STRIPES_OFFSET)
        )

        # Drawing dividing strips on X axis
        for strip_x in range(-1, (self.WIDTH - 2 * Config.DIVIDING_STRIPES_OFFSET) // self.graph_scale):
            half_width = (self.WIDTH - 2 * Config.DIVIDING_STRIPES_OFFSET) // 2
            strip_x_offset = half_width - self.graph_scale * (half_width // self.graph_scale - 1)
            strip_x_coordinate = Config.DIVIDING_STRIPES_OFFSET + strip_x * self.graph_scale + strip_x_offset

            pygame.draw.line(
                self.screen,
                Config.BLACK,
                (strip_x_coordinate, self.GRAPH_CENTER.y - Config.DIVIDING_STRIPES_WIDTH),
                (strip_x_coordinate, self.GRAPH_CENTER.y + Config.DIVIDING_STRIPES_WIDTH)
            )

        # Drawing dividing strips on Y axis
        for strip_y in range(-1, (self.HEIGHT - 2 * Config.DIVIDING_STRIPES_OFFSET) // self.graph_scale):
            half_height = (self.HEIGHT - 2 * Config.DIVIDING_STRIPES_OFFSET) // 2
            strip_y_offset = half_height - self.graph_scale * (half_height // self.graph_scale - 1)
            strip_y_coordinate = Config.DIVIDING_STRIPES_OFFSET + strip_y * self.graph_scale + strip_y_offset

            pygame.draw.line(
                self.screen,
                Config.BLACK,
                (self.GRAPH_CENTER.x - Config.DIVIDING_STRIPES_WIDTH, strip_y_coordinate),
                (self.GRAPH_CENTER.x + Config.DIVIDING_STRIPES_WIDTH, strip_y_coordinate),
            )

    def __draw_function(self, function: Function, color: pygame.Color) -> None:
        """Draws graph of given function"""
        previous_dot_position = None
        if function.left_x and function.right_x:
            left_border = round(function.left_x * self.graph_scale)
            right_border = round(function.right_x * self.graph_scale)
        else:
            half_width = ((self.WIDTH - 2 * Config.DIVIDING_STRIPES_OFFSET) // 2)
            left_border = -self.graph_scale * (half_width // self.graph_scale)
            right_border = self.graph_scale * (half_width // self.graph_scale)

        for x in range(left_border, right_border):
            try:
                graph_dot_offset = Vector2(x, -function.function(x / self.graph_scale) * self.graph_scale)
                current_dot_position = self.GRAPH_CENTER + graph_dot_offset

                if previous_dot_position:
                    if abs(previous_dot_position.y - current_dot_position.y) < self.HEIGHT:
                        pygame.draw.line(self.screen, color, previous_dot_position, current_dot_position, 1)

                previous_dot_position = current_dot_position
            except (ValueError, ZeroDivisionError):
                pass
