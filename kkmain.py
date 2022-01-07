import os

import kkcards as crd
import kkgui as ui
import pygame as pg
import random as rd
import concurrent.futures
from kkbase import Player, Comp, Log, GameFlow, GameState as State
from dataclasses import dataclass
from enum import Enum


class CardType(Enum):
    BRIGHT = 3
    ANIMAL = 2
    RIBBON = 1
    PLAIN = 0

    def __repr__(self):
        return self.name


@dataclass
class Card:
    BRIGHTS = ('Matsu ni Tsuru', 'Sakura ni Maku', 'Susuki ni Tsuki', 'Yanagi ni Ono no Toufuu', 'Kiri ni Ho-oh')
    FLOWERS = ('Matsu', 'Ume', 'Sakura', 'Fuji', 'Ayame', 'Botan', 'Hagi', 'Susuki', 'Kiku', 'Momiji', 'Yanagi', 'Kiri')
    WIDTH = 75
    HEIGHT = 113

    name: str = ''
    image: pg.Surface = None
    value: int = 0
    type: CardType = None

    def __post_init__(self):
        # Assign value
        for index, flower in enumerate(self.FLOWERS):
            if self.name.startswith(flower):
                self.value = index + 1

        # Assign type
        if self.name.endswith('no Tan'):
            self.type = CardType.RIBBON
        elif self.name.endswith('no Kasu'):
            self.type = CardType.PLAIN
        elif self.name in self.BRIGHTS:
            self.type = CardType.BRIGHT
        else:
            self.type = CardType.ANIMAL

    def __repr__(self):
        return self.name

    def resize(self, size=(WIDTH, HEIGHT)):
        self.image = pg.transform.scale(self.image, size)

    @property
    def get_width(self):
        return self.image.get_width()

    @property
    def get_height(self):
        return self.image.get_height()


class Deck:
    """Creates Card instances."""
    __slots__ = ('cards', 'position')

    def __init__(self):
        self.cards: list = self.build()
        self.position = ui.Box((25, ui.Display.HEIGHT//2, Card.WIDTH, Card.HEIGHT), 'Deck')

    @staticmethod
    def build() -> list[Card]:
        """Gathers the images and names to create the cards."""
        # Create list of names
        with open('Images/Cards/card_names.txt') as txt:
            name_list = txt.read()
            card_names = [name for name in name_list.split('\n')]

        # Create list of images
        img_path = os.path.join('Images', 'Cards')
        img_list = os.listdir(os.path.join('Images', 'Cards'))
        card_images = [pg.image.load(os.path.join(img_path, img)) for img in img_list if img.endswith('.png')]

        # Create list of instances with the zipped lists as parameters
        cards = [Card(name=name, image=img) for name, img in zip(card_names, card_images)]
        return cards

    def draw_cards(self, num_cards=1) -> list[Card]:
        drawn_cards = []
        for _ in range(num_cards):
            if not self.empty:
                card = rd.choice(self.cards)  # Pick a card
                drawn_cards.append(card)  # Add card to list
                self.cards.remove(card)  # Remove card from deck
        return drawn_cards

    @property
    def remaining(self) -> int:
        return len(self.cards)

    @property
    def empty(self) -> bool:
        return not self.cards


class Hand:
    """Control Card positioning."""
    __slots__ = ('player', 'cards', '_selected', 'positions', '_hidden', 'collection')

    def __init__(self, deck: Deck, player_num=0):
        self.player = player_num
        self.cards = deck.draw_cards(8)
        self._selected = None
        self._hidden = False
        self.positions = self.set_positions(deck.position)
        self.collection = crd.Collection if player_num else None

    def __repr__(self):
        return f'Player{self.player}: {self.cards}'

    @Log.call_log
    def set_positions(self, deck_pos: ui.Box) -> tuple:
        positions = []
        match self.player:
            case 0:  # Table card positions
                for n in range(self.count):
                    # x = (left start pos) + (card width offset) + (gap offset)
                    x = (deck_pos.x + 50 + Card.WIDTH) + (n * Card.WIDTH // 2) + n
                    # split cards into 2 rows
                    y = deck_pos.y + ((1 + Card.HEIGHT // 2) * (1 if n % 2 else -1))
                    rect_dim = (x, y, Card.WIDTH, Card.HEIGHT)
                    positions.append(ui.Box(rect_dim, f'Table Card {n + 1}'))

            case 1:  # Player1 card positions
                start = deck_pos.x
                positions = (
                    ui.Box((start + x * Card.WIDTH + x, ui.Display.HEIGHT - 150, Card.WIDTH, Card.HEIGHT),
                           f'P1 Card {x + 1}')
                    for x in range(self.count)
                )
            case 2:  # Player2/Comp card positions
                self._hidden = True
                start = deck_pos.x
                positions = (
                    ui.Box((start + x * Card.WIDTH + x, 100, Card.WIDTH, Card.HEIGHT),
                           f'P2 Card {x + 1}')
                    for x in range(self.count)
                )
        return tuple(positions)

    @Log.call_log
    def select_card(self, card_found=None) -> Card:
        if card_found:
            self._selected = card_found
        else:
            for card, box in zip(self.cards, self.positions):
                if ui.mouse_over(box):
                    box.active = True
                    self._selected = card
        self.cards.remove(self.selected)
        return self.selected

    def reset_selection(self):
        for box in self.positions:
            box.active = False
        self.cards.append(self._selected)
        self._selected = None

    def hide(self):
        self._hidden = True
        for box in self.positions:
            pg.draw.rect(ui.Display.WINDOW, ui.Display.RGB_RED, box)

    def reveal(self):
        self._hidden = False

    @property
    def selected(self) -> Card:
        return self._selected

    @property
    def empty(self) -> bool:
        return not self.cards

    @property
    def count(self) -> int:
        return len(self.cards)

    @property
    def hidden(self) -> bool:
        return self._hidden

    @property
    def images(self) -> list:
        return [card.image for card in self.cards]


class Table(Hand):
    """
    This class provides the bridge between the main loop and player input.
    """
    __slots__ = ('_matched',)

    def __init__(self, deck: Deck):
        super().__init__(deck)
        self._matched = []

    def match_pool(self, comp_hand: Hand) -> list[tuple[Card, Card]]:
        matches = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self.find_match, card) for card in comp_hand.cards]
            for f in concurrent.futures.as_completed(results):
                if f.result():
                    matches += f.result()
        return matches

    def add_card(self, new_card: Card):
        self.cards.append(new_card)

    def find_match(self, selected_card: Card) -> list[tuple[Card, Card]]:
        """Returns a card for comp selection."""
        matches_found = [(selected_card, card) for card in self.cards if card.value == selected_card.value]
        return matches_found

    def match_card(self, selected_card):
        pass

    def update(self, p1_cards: Hand, p2_cards: Hand, deck: Deck, deck_draw=None):
        if deck_draw:
            ui.Display.draw_images([deck_draw.image], [(deck.position.x + 10, deck.position.y + 10)])
        elif not deck.empty:
            pg.draw.rect(ui.Display.WINDOW, ui.Display.RGB_RED, deck.position)

        for hand in [self, p1_cards, p2_cards]:
            # Append extra positions
            if len(hand.cards) > len(hand.positions):
                hand.set_positions(deck.position)

            if not hand.hidden:
                ui.Display.draw_images(hand.images, hand.positions)
                ui.Box.highlight(hand.positions)
            else:
                hand.hide()


def initialize() -> tuple:
    player = Player()
    player.set_opponent(Comp())
    comp = player.opp
    comp.set_opponent(player)

    player.__setattr__('collection', crd.Collection())
    comp.__setattr__('collection', crd.Collection())
    return player, comp


def start_screen(game):
    while game.state is State.START:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.end_flow()

            if event.type == pg.KEYDOWN:
                keys_pressed = pg.key.get_pressed()
                if keys_pressed[pg.K_RETURN]:
                    game.break_flow(State.SETUP)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and ui.mouse_over(ui.DisplayData.START_BUTTON):
                    game.break_flow(State.SETUP)

        ui.DisplayData.draw_start()
        pg.display.flip()


def switch_players(game, table):
    pass


def main():
    game = GameFlow(state_order=(
        State.PLAY, State.MATCH, State.WAIT, State.MATCH, State.END,
        State.COMP, State.MATCH, State.WAIT, State.MATCH, State.END
    ))

    start_screen(game)  # State.START -> SETUP | QUIT

    player, comp = initialize()
    deck = Deck()
    player.__setattr__('hand', Hand(deck, player_num=1))
    comp.__setattr__('hand', Hand(deck, player_num=2))
    table = Table(deck)
    game.progress_flow(start=State.PLAY)

    clock = pg.time.Clock()
    while game.state is not State.QUIT:
        clock.tick(ui.Display.FPS)

        match game.state:
            case State.COMP:
                active_player, hand = comp, comp.hand
                active_cards = []

                matches = table.match_pool(comp.hand)
                if matches:
                    found_card, matched_card = rd.choice(matches)
                    comp.hand.select_card(found_card)
                else:
                    discard = comp.hand.select_card(rd.choice(comp.hand.cards))
                    table.add_card(discard)

            case State.PLAY:
                active_player, hand = player, player.hand
                active_cards = []

                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pass

        ui.Display.draw_window()
        table.update(player.hand, comp.hand, deck)
        pg.display.flip()


if __name__ == '__main__':
    main()
