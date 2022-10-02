import typing as t

import pygame
from pygame.math import Vector2

from config import Config
from app.graph import Graph
from app.grid import Grid


class Function(t.NamedTuple):
    function: t.Callable
    left_x: t.Optional[float] = None
    right_x: t.Optional[float] = None


class Application:
    def __init__(self, functions: t.Iterable[Function], initial_scale: int):
        pygame.init()
        self.functions = functions
        self.graph_scale = initial_scale

        self.WIDTH = Config.WINDOW_WIDTH
        self.HEIGHT = Config.WINDOW_HEIGHT
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

        self.grid = Grid()

    def run(self) -> None:
        while self.running:
            self.screen.fill(Config.WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if event.button == 4:
                #         self.graph_scale += Config.ZOOM_VALUE
                #     elif event.button == 5:
                #         self.graph_scale -= Config.ZOOM_VALUE

            for index, (function, color) in enumerate(zip(self.functions, self.COLORS)):
                # print(function.left_x, function.right_x, color)
                surface = pygame.Surface((self.grid.graph_width, self.grid.graph_height), pygame.SRCALPHA)
                graph = Graph(surface=surface, function=function, color=color)
                graph.render()

                row = (index + 1) // Config.ROWS
                column = Config.COLUMNS - (Config.COLUMNS - (index + 1) % Config.COLUMNS) % Config.COLUMNS
                print(row, column)
                self.screen.blit(graph.surface, self.grid.get_position(row, column))

            pygame.display.flip()

        pygame.quit()
