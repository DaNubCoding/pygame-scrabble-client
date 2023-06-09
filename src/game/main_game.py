from random import shuffle
from typing import Literal

from src.common.constants import VEC, Color, TILE_SIZE, TILE_MARGIN, OPTIONS_BUTTON_FONT
from src.game.elements.button import ButtonType1, ShuffleButton, ResetButton
from src.game.elements.container import Container, Spacer
from src.game.elements.dropped_tile import DroppedTile
from src.game.elements.placed_tile import PlacedTile
from src.game.elements.rack_tile import RackTile
from src.client.client import MessageType
from src.management.element import Style
from src.management.scene import Scene
from src.common.utils import inttup
from src.game.board import Board

class MainGame(Scene):
    def setup(self) -> None:
        super().setup()

        self.board = Board(self)
        self.turn = False
        self.score = 0

        self.rack_button_style = Style(
            idle_color = Color.RACK_BUTTON_IDLE.value,
            hover_color = Color.RACK_BUTTON_HOVER.value,
            click_color = Color.RACK_BUTTON_CLICK.value,
            idle_fg_color = (0, 0, 0),
            locked_bg_color = Color.RACK_BUTTON_HOVER.value,
            font = OPTIONS_BUTTON_FONT,
        )

        self.__build_rack_container()
        self.rack.add_children(Spacer(self, (0, 0, 2, 0)))

        self.__build_options_container()

    def __build_rack_container(self) -> None:
        self.rack_cont = Container(self, (40, 780, (TILE_SIZE + TILE_MARGIN) * 15 - TILE_MARGIN, 110))
        self.rack_cont.setup(
            bg_color = (255, 255, 255),
            border_radius = 12,
        )

        self.shuffle_button = ShuffleButton(self, (15, 15, ..., "100% - 30p"))
        self.shuffle_button.setup(**self.rack_button_style)
        self.rack_cont.add_children(self.shuffle_button)

        self.rack = Container(self, ("$ + 15p", 15, "100% - $ - $ - 30p - 30p", "100% - 30p"))
        self.rack.setup(
            bg_color = Color.BG.value,
            border_radius = 12,
        )
        self.rack_cont.add_children(self.rack)

        self.reset_button = ResetButton(self, ("$ + 15p", 15, ..., "100% - 30p"))
        self.reset_button.setup(**self.rack_button_style)
        self.rack_cont.add_children(self.reset_button)

    def __build_options_container(self) -> None:
        cont = Container(self, (VEC(self.rack_cont.rect.topleft) + (0, 125), VEC(self.rack_cont.rect.size) - (0, 40)))

        cont.add_children(ele := ButtonType1(self, (0, 0, "(100% - 15p * 3) / 4", "100%"), lambda: print("resign")))
        ele.setup(
            **self.rack_button_style,
            text = "Resign",
            border_radius = 9,
        )

        self.skip_button = ButtonType1(self, ("$ + 15p", 0, "$", "100%"), lambda: print("skip"))
        cont.add_children(self.skip_button)
        self.skip_button.setup(
            **self.rack_button_style,
            text = "Skip",
            border_radius = 9,
        )

        self.swap_button = ButtonType1(self, ("$ + 15p", 0, "$", "100%"), lambda: print("swap"))
        cont.add_children(self.swap_button)
        self.swap_button.setup(
            **self.rack_button_style,
            text = "Swap",
            border_radius = 9,
        )

        self.submit_button = ButtonType1(self, ("$ + 15p", 0, "$", "100%"), self.submit)
        cont.add_children(self.submit_button)
        self.submit_button.setup(
            text = "Submit",
            font = OPTIONS_BUTTON_FONT,
            idle_fg_color = (255, 255, 255),
            idle_color = Color.SUBMIT_BUTTON_IDLE.value,
            hover_color = Color.SUBMIT_BUTTON_HOVER.value,
            click_color = Color.SUBMIT_BUTTON_CLICK.value,
            locked_bg_color = Color.SUBMIT_BUTTON_LOCKED_BG.value,
            locked_fg_color = Color.SUBMIT_BUTTON_LOCKED_FG.value,
            border_radius = 9,
        )

    def shuffle(self) -> None:
        children = self.rack.children[1:]
        shuffle(children)
        self.reorder_rack(children)

    def reset(self) -> None:
        children = self.rack.children[1:]
        children.sort(key=lambda child: child.text)
        self.reorder_rack(children)

    def clear(self) -> None:
        for dropped_tile in DroppedTile._registry.copy():
            dropped_tile.rack_tile.unhide()
            dropped_tile.kill()

    def reorder_rack(self, children: list[RackTile] = None) -> None:
        if children:
            self.rack.children = [self.rack.children[0]] + children

        for child in self.rack.children:
            child.parse_rect()

    def submit(self) -> None:
        if not self.turn: return

        tiles = {inttup(dropped_tile.board_pos): dropped_tile.text for dropped_tile in DroppedTile._registry}

        if not tiles: return
        self.manager.client.send({"type": MessageType.PLACE.name, "message": tiles})

    def update(self) -> None:
        super().update()

        self.skip_button.locked = self.swap_button.locked = self.submit_button.locked = not self.turn

        if not self.manager.client.has_messages: return
        message = self.manager.client.get_message()
        message_handler = getattr(self, f"message_type_{message['type'].lower()}")
        print(f"Processing message of type {message['type']}.")
        message_handler(message["message"])

    # The following methods with the prefix "message_type_" are called based on the name of the type of message received

    def message_type_place(self, tiles: dict[tuple[int, int], str]) -> None:
        for board_pos, letter in tiles.items():
            PlacedTile(self, VEC(board_pos), letter)

    def message_type_replenish(self, new_tiles: list[str]) -> None:
        # Settle tiles since a replenish message = valid move
        tiles = {}
        for dropped_tile in DroppedTile._registry.copy():
            tiles[inttup(dropped_tile.board_pos)] = dropped_tile.text
            PlacedTile(self, dropped_tile.board_pos, dropped_tile.text)
            dropped_tile.rack_tile.kill()
            dropped_tile.kill()

        self.turn = False

        self.reorder_rack()
        for letter in new_tiles:
            self.rack.add_children(RackTile(self, ("$ + 9p", 10, ..., "100% - 20p"), letter))

    def message_type_turn(self, _: Literal[None]) -> None:
        print("MY TURN!")
        self.turn = True

    def message_type_invalid(self, reason: str) -> None:
        print(f"Invalid! {reason}")
        self.clear()

    def message_type_points(self, points: int) -> None:
        self.score += points
        print(f"{points} points received! Score now: {self.score}")

    def draw(self) -> None:
        self.manager.screen.fill(Color.BG.value)

        super().draw()