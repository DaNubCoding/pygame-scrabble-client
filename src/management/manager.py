from pygame.locals import *
from enum import Enum
import pygame
import sys

from src.common.constants import VEC, FPS, SIZE
from src.game.main_game import MainGame
from src.management.scene import Scene
from src.client.client import Client

class AbortScene(Exception):
    def __str__(self):
        return "Scene aborted but not caught with a try/except block."

class AbortGame(Exception):
    def __str__(self):
        return "Game aborted but not caught with a try/except block."

class GameManager:
    def __init__(self) -> None:
        pygame.init()

        self.flags = DOUBLEBUF | SCALED
        self.screen = pygame.display.set_mode(SIZE, self.flags)
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick_busy_loop(FPS) * 0.05
        self.window_changing = False
        self.events = {}

        self.scene = MainGame(self, None)
        self.scene.setup()

        self.client = Client(self)

    def run(self) -> None:
        running = True

        while running:
            try:
                self.update()
                self.scene.update()
                self.scene.draw()
            except AbortScene:
                continue
            except AbortGame:
                running = False

            pygame.display.flip()

        self.quit()

    def update(self) -> None:
        self.dt = self.clock.tick_busy_loop(FPS) * 0.001
        # Window changing events only register to the DT the frame after the event
        # Thus the window changing variable is sustained to the next frame, and handled here
        if self.window_changing:
            self.dt = 0
            self.window_changing = False

        pygame.display.set_caption(f"Pygame Scrabble | FPS: {round(self.clock.get_fps())} | Score: {self.scene.score}")

        self.events = {event.type: event for event in pygame.event.get()}
        self.mouse_state = pygame.mouse.get_pressed()
        self.mouse_pos = VEC(pygame.mouse.get_pos())

        if QUIT in self.events:
            raise AbortGame
        if WINDOWRESIZED in self.events or WINDOWMOVED in self.events:
            self.window_changing = True
            self.dt = 0

        if not self.client.alive:
            raise AbortGame

    def quit(self) -> None:
        self.client.disconnect()
        pygame.quit()
        sys.exit()

    def new_scene(self, scene_class: str) -> None:
        self.scene = self.Scenes[scene_class].value(self, self.scene)
        self.scene.setup()
        raise AbortScene

    def switch_scene(self, scene: Scene) -> None:
        self.scene = scene
        raise AbortScene

    class Scenes(Enum):
        MainGame = MainGame