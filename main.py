import time
from dataclasses import dataclass, field
from pprint import pprint

import pygame

from pygame.sprite import Sprite, Group
from pygame.surface import Surface
from settings import *

from components import Grid, Tile

pygame.init()


@dataclass
class Game:
    width: int = WIDTH
    height: int = HEIGHT

    running: bool = True
    screen: Surface | None = None

    player_move: Tile | None = None
    current_player: bool = True
    winner: bool | None = None
    clock: pygame.time.Clock = pygame.time.Clock()
    font: pygame.font.SysFont = pygame.font.SysFont('arial', 14)
    board_size: int = GRID_SIZE
    player_icons: dict[bool, Path] = field(default_factory=lambda: {
        True: ASSETS_DIR / 'letter-o.png',
        False: ASSETS_DIR / 'letter-x.png'
    })

    board: list[list[bool, None]] = None

    def get_initial_board(self) -> list[list[bool, None]]:
        return [[None for __ in range(self.board_size)] for _ in range(self.board_size)]

    def __post_init__(self) -> None:
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.board = self.get_initial_board()
        self.grid = Grid(self.board_size, self.board_size)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))
            self.update()

            pygame.display.update()
            self.clock.tick(60)

    def __check_group(self, group: list[bool | None]) -> None:
        if all(group):
            self.winner = True
        if None not in group and not any(group):
            self.winner = False

    def check_win(self) -> None:
        for i, col in enumerate(self.board):
            self.__check_group(col)

            row = [self.board[j][i] for j in range(self.board_size)]

            self.__check_group(row)

        diagonal = [self.board[i][i] for i in range(self.board_size)]
        self.__check_group(diagonal)

        reverse_diagonal = [self.board[i][j] for i, j in
                            zip(range(self.board_size), range(self.board_size - 1, -1, -1))]
        self.__check_group(reverse_diagonal)

    def draw_winner(self) -> None:
        self.screen.fill(Color.BLUE)
        text = self.font.render(f'Winner is Player: {1 if self.winner else 2 if self.winner is not None else None}',
                                True, (0, 0, 0))
        rect = text.get_rect()
        rect.center = self.width // 2, self.height // 2
        self.screen.blit(text, rect)

        button = self.font.render(f'Restart', True, (255, 255, 255), (0, 0, 0))
        button_rect = button.get_rect()
        button_rect.center = self.width // 2, (self.height // 2) + 150

        self.screen.blit(button, button_rect)

        if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
            self.restart()

    def restart(self) -> None:
        self.player_move = None
        self.current_player = True
        self.board = self.get_initial_board()
        self.grid.clicked_item = None
        for tile in self.grid.sprites():
            if type(tile) == Tile:
                tile.selected = False
        self.winner = None
        self.player_move = None
        time.sleep(0.1)

    def update(self) -> None:
        if all(
                [
                    all(
                        [cell is not None for cell in row]
                    )
                    for row in self.board
                ]
        ):
            self.draw_winner()
            return
        self.grid.draw(self.screen)

        if self.winner is not None:
            self.draw_winner()
            return

        self.grid.update()

        if self.player_move != self.grid.clicked_item:
            item_pos = self.grid.clicked_item.rect
            row, col = item_pos.x // TILE_SIZE, item_pos.y // TILE_SIZE

            current_cell = self.board[row][col]
            if current_cell is not None:
                return
            # print(row, col, self.current_player, current_cell)

            self.board[row][col] = self.current_player

            self.current_player = not self.current_player

            self.player_move = self.grid.clicked_item

            self.player_move.set_image(self.player_icons[self.current_player])
            self.player_move.selected = True
            self.check_win()


def main() -> None:
    game: Game = Game()
    game.run()


if __name__ == '__main__':
    main()
