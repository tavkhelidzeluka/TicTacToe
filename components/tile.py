from pathlib import Path

import pygame
from pygame import Surface
from pygame.sprite import Sprite
from settings import TILE_SIZE


class Tile(Sprite):
    def __init__(self, x: int, y: int, *args: any) -> None:
        super().__init__(*args)
        self.selected: bool = False

        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

    def set_image(self, image_path: Path) -> None:
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, self.rect.size)

    def update(self) -> None:
        if self.selected:
            return
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill((0, 125, 175))
        else:
            self.image.fill((255, 255, 255))