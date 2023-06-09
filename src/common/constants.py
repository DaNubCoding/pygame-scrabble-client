from enum import Enum
import pygame

VEC = pygame.math.Vector2

IP = "localhost" # "10.242.101.221" # "192.168.0.90"
PORT = 1200
ADDRESS = (IP, PORT)

FPS = 60
WIDTH, HEIGHT = SIZE = 800, 1000
HSIZE = (WIDTH // 2, HEIGHT // 2)
TILE_SIZE = 44
TILE_MARGIN = 4
NUM_TILES = 15
BOARD_SIZE = (TILE_SIZE + TILE_MARGIN) * NUM_TILES - TILE_MARGIN

class Color(Enum):
    BG = (230, 230, 241)
    TILE_BG = (196, 196, 209)
    DL = (104, 162, 195)
    TL = (12, 103, 156)
    DW = (228, 162, 163)
    TW = (191, 78, 78)
    AXIS_TEXT = (145, 145, 165)
    RACK_BUTTON_IDLE = (244, 244, 250)
    RACK_BUTTON_HOVER = (230, 230, 241)
    RACK_BUTTON_CLICK = (210, 210, 220)
    SUBMIT_BUTTON_IDLE = (61, 182, 194)
    SUBMIT_BUTTON_HOVER = (98, 160, 170)
    SUBMIT_BUTTON_CLICK = (78, 140, 155)
    SUBMIT_BUTTON_LOCKED_BG = (70, 70, 87)
    SUBMIT_BUTTON_LOCKED_FG = (145, 146, 160)
    RACK_TILE = (255, 218, 158)
    RACK_TILE_EDGE = (229, 181, 104)
    DROPPED_TILE = (241, 197, 84)
    DROPPED_TILE_EDGE = (237, 184, 96)
    PLACED_TILE = (255, 241, 220)
    PLACED_TILE_EDGE = (237, 206, 160)

BONUS_LOCATIONS = {
    (4, 1): Color.DL,
    (12, 1): Color.DL,
    (7, 3): Color.DL,
    (9, 3): Color.DL,
    (1, 4): Color.DL,
    (8, 4): Color.DL,
    (15, 4): Color.DL,
    (3, 7): Color.DL,
    (7, 7): Color.DL,
    (9, 7): Color.DL,
    (13, 7): Color.DL,
    (4, 8): Color.DL,
    (12, 8): Color.DL,
    (3, 9): Color.DL,
    (7, 9): Color.DL,
    (9, 9): Color.DL,
    (13, 9): Color.DL,
    (1, 12): Color.DL,
    (8, 12): Color.DL,
    (15, 12): Color.DL,
    (7, 13): Color.DL,
    (9, 13): Color.DL,
    (4, 15): Color.DL,
    (12, 15): Color.DL,

    (6, 2): Color.TL,
    (10, 2): Color.TL,
    (2, 6): Color.TL,
    (6, 6): Color.TL,
    (10, 6): Color.TL,
    (14, 6): Color.TL,
    (2, 10): Color.TL,
    (6, 10): Color.TL,
    (10, 10): Color.TL,
    (14, 10): Color.TL,
    (6, 14): Color.TL,
    (10, 14): Color.TL,

    (2, 2): Color.DW,
    (3, 3): Color.DW,
    (4, 4): Color.DW,
    (5, 5): Color.DW,
    (14, 2): Color.DW,
    (13, 3): Color.DW,
    (12, 4): Color.DW,
    (11, 5): Color.DW,
    (14, 14): Color.DW,
    (13, 13): Color.DW,
    (12, 12): Color.DW,
    (11, 11): Color.DW,
    (2, 14): Color.DW,
    (3, 13): Color.DW,
    (4, 12): Color.DW,
    (5, 11): Color.DW,
    (8, 8): Color.DW,

    (1, 1): Color.TW,
    (15, 1): Color.TW,
    (15, 15): Color.TW,
    (1, 15): Color.TW,
    (8, 1): Color.TW,
    (15, 8): Color.TW,
    (8, 15): Color.TW,
    (1, 8): Color.TW,
}

LETTER_POINTS = {
    "A": 1, "E": 1, "I": 1, "O": 1, "U": 1, "L": 1, "N": 1, "S": 1, "T": 1, "R": 1,
    "D": 2, "G": 2,
    "B": 3, "C": 3, "M": 3, "P": 3,
    "F": 4, "H": 4, "V": 4, "W": 4, "Y": 4,
    "K": 5,
    "J": 8, "X": 8,
    "Q": 10, "Z": 10,
}

# interextralight inter intermedium interregular intersemibold interthin interblack interextrabold
pygame.font.init()
BONUS_FONT = pygame.font.SysFont("interextrabold", 15)
AXIS_FONT = pygame.font.SysFont("intersemibold", 11)
OPTIONS_BUTTON_FONT = pygame.font.SysFont("intersemibold", 18)
RACK_TILE_FONT = pygame.font.SysFont("interextrabold", 35)
RACK_TILE_SUBFONT = pygame.font.SysFont("interextrabold", 12)
DROPPED_TILE_FONT = PLACED_TILE_FONT = pygame.font.SysFont("interextrabold", 30)
DROPPED_TILE_SUBFONT = PLACED_TILE_SUBFONT = pygame.font.SysFont("interextrabold", 10)