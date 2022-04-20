from pathlib import Path

WIDTH = 1280
HEIGHT = 800
TILE_SIZE = 64 * 3

GRID_SIZE = 3
WIDTH = TILE_SIZE * GRID_SIZE
HEIGHT = TILE_SIZE * GRID_SIZE


class Color:
    GREEN = (50, 86, 72)
    BLUE = (0, 145, 247)


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
