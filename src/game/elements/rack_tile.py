from functools import cached_property
from pygame.math import Vector3
from pygame.locals import *
import pygame

from src.common.constants import VEC, Color, LETTER_POINTS, RACK_TILE_FONT, RACK_TILE_SUBFONT
from src.game.elements.interactable import Interactable
from src.game.held_tile import HeldTile
from src.management.scene import Scene

class RackTile(Interactable):
    def __init__(self, scene: Scene, rect: tuple[float, float, float, float], letter: str) -> None:
        super().__init__(scene, rect)
        self.text = letter
        self.bg_color = Color.RACK_TILE.value
        self.edge_color = Color.RACK_TILE_EDGE.value
        self.fg_color = (0, 0, 0)
        self.font = RACK_TILE_FONT
        self.subfont = RACK_TILE_SUBFONT
        self.border_radius = 9

        self.scale = 1

    @cached_property
    def image(self) -> pygame.SurfaceType:
        image = pygame.Surface(self.rect.size, SRCALPHA)
        pygame.draw.rect(image, self.bg_color, ((0, 0), self.rect.size), 0, self.border_radius)
        for i in range(5):
            edge_color = Vector3(self.edge_color) + (Vector3(self.bg_color) - self.edge_color) / 5 * i
            pygame.draw.rect(image, edge_color, ((i, i), VEC(self.rect.size) - (i * 2, i * 2)), 2, self.border_radius)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        image.blit(text_surf, (VEC(self.rect.size) - text_surf.get_size()) // 2 + (1, 1))
        text_surf = self.font.render(self.text, True, self.fg_color)
        image.blit(text_surf, (VEC(self.rect.size) - text_surf.get_size()) // 2)

        text_surf = self.subfont.render(str(LETTER_POINTS[self.text]), True, self.fg_color)
        image.blit(text_surf, VEC(image.get_size()) - VEC(text_surf.get_size()) - (5, 5))

        return image

    def draw(self) -> None:
        transformed = pygame.transform.scale_by(self.image, self.scale)
        self.manager.screen.blit(transformed, VEC(self.rect.topleft) + (VEC(self.rect.size) - transformed.get_size()) // 2)

    def on_click(self) -> None:
        HeldTile(self.scene, self.rect.topleft, self).scale = 1
        self.hide()

    def hovering(self) -> None:
        self.scale += 0.8 * self.manager.dt
        self.scale = min(self.scale, 1.1)

    def idle(self) -> None:
        self.scale -= 0.8 * self.manager.dt
        self.scale = max(self.scale, 1)

    def hide(self) -> None:
        super().kill()

    def unhide(self) -> None:
        self.scene.sprite_manager.add(self)

    def kill(self) -> None:
        self.parent.children.remove(self)
        try:
            super().kill()
        except ValueError: # It has already been removed from the sprite manager via self.hide
            pass