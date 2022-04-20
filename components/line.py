from pygame import Surface
from pygame.sprite import Sprite

from settings import TILE_SIZE


class Line(Sprite):
    def __init__(self, x: int, y: int, width: int, height: int, *args: any) -> None:
        super().__init__(*args)

        self.image = Surface((width, height))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
