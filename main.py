import typing as t

import pygame
from pygame.math import Vector2

from config import Config


class PygameGraph:
    def __init__(self, function: t.Callable, scale: int):
        pygame.init()
        self.function = function
        self.graph_scale = scale

        self.WIDTH = Config.WINDOW_WIDTH
        self.HEIGHT = Config.WINDOW_HEIGHT
        self.WINDOW_CENTER = Vector2(self.WIDTH // 2, self.HEIGHT // 2)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True

        pygame.display.set_caption('Pygame graph')

    def run(self) -> None:
        self.screen.fill(Config.WHITE)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.__draw_coordinate_plane()
            self.__draw_function()

            pygame.display.flip()

        pygame.quit()

    def __draw_coordinate_plane(self) -> None:
        # Drawing horizontal and vertical lines
        pygame.draw.line(
            self.screen,
            Config.BLACK,
            (Config.DIVIDING_STRIPES_OFFSET, self.HEIGHT // 2),
            (self.WIDTH - Config.DIVIDING_STRIPES_OFFSET, self.HEIGHT // 2)
        )
        pygame.draw.line(
            self.screen,
            Config.BLACK,
            (self.WIDTH // 2, Config.DIVIDING_STRIPES_OFFSET),
            (self.WIDTH // 2, self.HEIGHT - Config.DIVIDING_STRIPES_OFFSET)
        )

        # Drawing dividing strips on X axis
        for strip_x in range(-1, (self.WIDTH - 2 * Config.DIVIDING_STRIPES_OFFSET)):
            half_width = (self.WIDTH - 2 * Config.DIVIDING_STRIPES_OFFSET) // 2
            strip_x_offset = half_width - self.graph_scale * (half_width // self.graph_scale - 1)
            strip_x_coordinate = Config.DIVIDING_STRIPES_OFFSET + strip_x * self.graph_scale + strip_x_offset

            pygame.draw.line(
                self.screen,
                Config.BLACK,
                (strip_x_coordinate, self.HEIGHT // 2 - Config.DIVIDING_STRIPES_WIDTH),
                (strip_x_coordinate, self.HEIGHT // 2 + Config.DIVIDING_STRIPES_WIDTH)
            )

        # Drawing dividing strips on Y axis
        for strip_y in range(-1, (self.HEIGHT - 2 * Config.DIVIDING_STRIPES_OFFSET)):
            half_height = (self.HEIGHT - 2 * Config.DIVIDING_STRIPES_OFFSET) // 2
            strip_y_offset = half_height - self.graph_scale * (half_height // self.graph_scale - 1)
            strip_y_coordinate = Config.DIVIDING_STRIPES_OFFSET + strip_y * self.graph_scale + strip_y_offset

            pygame.draw.line(
                self.screen,
                Config.BLACK,
                (self.WIDTH // 2 - Config.DIVIDING_STRIPES_WIDTH, strip_y_coordinate),
                (self.WIDTH // 2 + Config.DIVIDING_STRIPES_WIDTH, strip_y_coordinate),
            )

    def __draw_function(self, left_x: int = -15, right_x: int = 15) -> None:
        """Draws graph of given function"""
        for x in range(left_x * self.graph_scale, right_x * self.graph_scale):
            try:
                graph_dot_offset = Vector2(x, -self.function(x / self.graph_scale) * self.graph_scale)
                pygame.draw.circle(self.screen, Config.BLACK, self.WINDOW_CENTER + graph_dot_offset, 1)
            except ValueError:
                print(f'Impossible to calculate value of function at point {x / self.graph_scale}')
