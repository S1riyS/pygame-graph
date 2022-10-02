import typing as t

import pygame
from pygame.math import Vector2

from config import Config
from app.types import Function, GraphType


class Graph:
    def __init__(
            self,
            surface: pygame.Surface,
            function: Function,
            color: pygame.Color,
            graph_type: GraphType = GraphType.CARTESIAN,
            initial_scale: int = 30
    ):

        self.surface = surface
        self.rect = self.surface.get_rect()

        self.function = function
        self.color = color
        self.graph_type = graph_type
        self.graph_scale = initial_scale

        self.WIDTH = self.rect.width
        self.HEIGHT = self.rect.height
        self.GRAPH_CENTER = Vector2(self.WIDTH // 2, self.HEIGHT // 2)

    def __normalize_graph_scale(self) -> None:
        self.graph_scale = min(max(self.graph_scale, Config.MIN_ZOOM), Config.MAX_ZOOM)

    def __draw_coordinate_plane(self) -> None:
        # Drawing horizontal and vertical lines
        pygame.draw.line(
            self.surface,
            Config.BLACK,
            (0, self.GRAPH_CENTER.y),
            (self.WIDTH, self.GRAPH_CENTER.y)
        )
        pygame.draw.line(
            self.surface,
            Config.BLACK,
            (self.GRAPH_CENTER.x, 0),
            (self.GRAPH_CENTER.x, self.HEIGHT)
        )

        # Drawing dividing strips on X axis
        for strip_x in range(-1, self.WIDTH // self.graph_scale):
            half_width = self.WIDTH // 2
            strip_x_offset = half_width - self.graph_scale * (half_width // self.graph_scale - 1)
            strip_x_coordinate = strip_x * self.graph_scale + strip_x_offset

            pygame.draw.line(
                self.surface,
                Config.BLACK,
                (strip_x_coordinate, self.GRAPH_CENTER.y - Config.DIVIDING_STRIPE_WIDTH),
                (strip_x_coordinate, self.GRAPH_CENTER.y + Config.DIVIDING_STRIPE_WIDTH)
            )

        # Drawing dividing strips on Y axis
        for strip_y in range(-1, self.HEIGHT // self.graph_scale):
            half_height = self.HEIGHT // 2
            strip_y_offset = half_height - self.graph_scale * (half_height // self.graph_scale - 1)
            strip_y_coordinate = strip_y * self.graph_scale + strip_y_offset

            pygame.draw.line(
                self.surface,
                Config.BLACK,
                (self.GRAPH_CENTER.x - Config.DIVIDING_STRIPE_WIDTH, strip_y_coordinate),
                (self.GRAPH_CENTER.x + Config.DIVIDING_STRIPE_WIDTH, strip_y_coordinate),
            )

    def __draw_function(self) -> None:
        """Draws graph of given function"""
        previous_dot_position = None

        if self.graph_type == GraphType.CARTESIAN:
            if self.function.left_x and self.function.right_x:
                left_border = round(self.function.left_x * self.graph_scale)
                right_border = round(self.function.right_x * self.graph_scale)
            else:
                half_width = self.WIDTH // 2
                left_border = -self.graph_scale * (half_width // self.graph_scale)
                right_border = self.graph_scale * (half_width // self.graph_scale)

            for x in range(left_border, right_border):
                try:
                    graph_dot_offset = Vector2(x, -self.function.function(x / self.graph_scale) * self.graph_scale)
                    current_dot_position = self.GRAPH_CENTER + graph_dot_offset

                    if previous_dot_position:
                        pygame.draw.line(self.surface, self.color, previous_dot_position, current_dot_position, 1)

                    previous_dot_position = current_dot_position

                except (ValueError, ZeroDivisionError):
                    pass

    def render(self):
        self.__normalize_graph_scale()
        self.__draw_coordinate_plane()
        self.__draw_function()
