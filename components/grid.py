import pygame
from pygame.sprite import Group

from settings import TILE_SIZE
from components.tile import Tile
from components.line import Line


class Grid(Group):

    def __init__(self, rows: int, cols: int, *args) -> None:
        super().__init__(*args)

        self.clicked_item: Tile | None = None
        self.interactable: bool = True

        for row in range(rows):
            for col in range(cols):
                self.add(Tile(row, col))

        for row in range(1, rows):
            self.add(Line(0, row, TILE_SIZE * rows, 2))

        for col in range(1, cols):
            self.add(Line(col, 0, 2, TILE_SIZE * cols))

    def update(self) -> None:
        for sprite in self.sprites():
            if self.interactable and pygame.mouse.get_pressed()[0] \
                    and sprite.rect and sprite.rect.collidepoint(pygame.mouse.get_pos()):
                self.clicked_item = sprite

            sprite.update()
