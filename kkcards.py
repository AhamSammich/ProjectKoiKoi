from abc import ABC, abstractmethod


class Collection:
    __slots__ = ('_cards', '_value', 'yaku_list')

    def __init__(self):
        self._cards = []
        self._value = 0
        self.yaku_list = [MoonViewing(),
                          FlowerViewing(),
                          BoarDeerButterfly(),
                          PoetryRibbons(),
                          BlueRibbons(),
                          ThreeBrights(),
                          FourBrightsWithRainman(),
                          FourBrights(),
                          FiveBrights(),
                          Ribbons(),
                          Animals(),
                          Plains()
                          ]

    def add_cards(self, new_cards: list[str]):
        self._cards += new_cards
        for yaku in self.yaku_list:
            yaku.collect(new_cards)

    def calculate_value(self):
        self._value = 0
        for yaku in self.completed_yaku:
            self._value += yaku.tally_points()

    @property
    def completed_yaku(self):
        return [yaku for yaku in self.yaku_list if yaku.complete]

    @property
    def value(self):
        return self._value


class Yaku(ABC):
    __slots__ = ('name', 'value', 'required', 'collected', 'remaining')

    def __repr__(self):
        return f'{self.name} ({self.__class__.__name__})'

    def collect(self, card_list):
        for name in card_list:
            if all([name in self.required, (name in self.remaining or name not in self.collected)]):
                self.collected.append(name)
                self.remaining.remove(name)

    @abstractmethod
    def tally_points(self) -> int:
        pass

    @property
    @abstractmethod
    def complete(self) -> bool:
        pass

    @property
    def count(self) -> int:
        return len(self.collected)


class MoonViewing(Yaku):

    def __init__(self):
        self.required = ['Susuki ni Tsuki', 'Kiku ni Sakazuki']
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Tsukimizake'
        self.value = 5

    def tally_points(self) -> int:
        return self.value if self.complete else 0

    @property
    def complete(self) -> bool:
        return not (set(self.collected) - set(self.required))


class FlowerViewing(Yaku):

    def __init__(self):
        self.required = ('Sakura ni Maku', 'Kiku ni Sakazuki')
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Hanamizake'
        self.value = 5

    def tally_points(self) -> int:
        return self.value if self.complete else 0

    @property
    def complete(self):
        return not (set(self.collected) - set(self.required))


class BoarDeerButterfly(Yaku):

    def __init__(self):
        self.required = ['Hagi ni Inoshishi', 'Momiji ni Shika', 'Botan ni Chou']
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Ino-Shika-Chou'
        self.value = 5

    def tally_points(self) -> int:
        return self.value if self.complete else 0

    @property
    def complete(self):
        return not (set(self.collected) - set(self.required))


class PoetryRibbons(Yaku):

    def __init__(self):
        self.required = ['Matsu no Tan', 'Ume no Tan', 'Sakura no Tan']
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Aka-tan'
        self.value = 5

    def tally_points(self) -> int:
        return self.value if self.complete else 0

    @property
    def complete(self):
        return not (set(self.collected) - set(self.required))


class BlueRibbons(Yaku):

    def __init__(self):
        self.required = ['Botan no Tan', 'Kiku no Tan', 'Momiji no Tan']
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Ao-tan'
        self.value = 5

    def tally_points(self) -> int:
        return self.value if self.complete else 0

    @property
    def complete(self):
        return not (set(self.collected) - set(self.required))


class ThreeBrights(Yaku):
    """Any three brights excluding Yanagi ni Ono no Toufuu"""

    def __init__(self):
        self.required = ['Matsu ni Tsuru', 'Sakura ni Maku', 'Susuki ni Tsuki', 'Kiri ni Ho-oh']
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Sankou'
        self.value = 5

    def tally_points(self) -> int:
        return self.value if self.complete else 0

    @property
    def complete(self):
        return set(self.required).intersection(set(self.collected)) == 3


class FourBrightsWithRainman(Yaku):
    """Yanagi ni Ono no Toufuu and any three brights"""

    def __init__(self):
        self.required = [
            'Matsu ni Tsuru', 'Sakura ni Maku', 'Susuki ni Tsuki', 'Kiri ni Ho-oh', 'Yanagi ni Ono no Toufuu']
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Ame-Shikou'
        self.value = 7

    def tally_points(self) -> int:
        return self.value if self.complete else 0

    @property
    def complete(self):
        return all(['Yanagi ni Ono no Toufuu' in self.collected, self.count == 4])


class FourBrights(Yaku):
    """Four brights excluding Yanagi ni Ono no Toufuu"""

    def __init__(self):
        self.required = ['Matsu ni Tsuru', 'Sakura ni Maku', 'Susuki ni Tsuki', 'Kiri ni Ho-oh']
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Shikou'
        self.value = 8

    def tally_points(self) -> int:
        return self.value if self.complete else 0

    @property
    def complete(self):
        return not (set(self.collected) - set(self.required))


class FiveBrights(Yaku):
    """All five brights"""

    def __init__(self):
        self.required = [
            'Matsu ni Tsuru', 'Sakura ni Maku', 'Susuki ni Tsuki', 'Yanagi ni Ono no Toufuu', 'Kiri ni Ho-oh']
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Gokou'
        self.value = 10

    def tally_points(self) -> int:
        return self.value if self.complete else 0

    @property
    def complete(self):
        return not (set(self.collected) - set(self.required))


class Animals(Yaku):
    """Any five animal(tane) cards"""

    def __init__(self):
        self.required = [
            'Ume ni Uguisu', 'Fuji ni Kakku', 'Ayame ni Yatsuhashi', 'Botan ni Chou', 'Hagi ni Inoshishi',
            'Susuki ni Kari', 'Kiku ni Sakazuki', 'Momiji ni Shika', 'Yanagi ni Tsubame'
        ]
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Tanezaku'
        self.value = 5  # plus

    def tally_points(self) -> int:
        if self.complete:
            xtra_pts = self.count - self.value
            if xtra_pts > 0:
                return self.value + xtra_pts
            else:
                return self.value
        else:
            return 0

    @property
    def complete(self):
        return self.count >= 5


class Ribbons(Yaku):
    """Any five red and/or blue ribbon(tan) cards"""

    def __init__(self):
        self.required = [
            'Matsu no Tan', 'Ume no Tan', 'Sakura no Tan', 'Fuji no Tan', 'Ayame no Tan', 'Botan no Tan',
            'Hagi no Tan', 'Kiku no Tan', 'Momiji no Tan', 'Yanagi no Tan'
        ]
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Tanzaku'
        self.value = 5

    def tally_points(self) -> int:
        if self.complete:
            xtra_pts = self.count - self.value
            if xtra_pts > 0:
                return self.value + xtra_pts
            else:
                return self.value
        else:
            return 0

    @property
    def complete(self):
        return self.count >= 5


class Plains(Yaku):
    """Any ten plain(kasu) cards"""

    def __init__(self):
        self.required = [
            'Matsu no Kasu', 'Matsu no Kasu',
            'Ume no Kasu', 'Ume no Kasu',
            'Sakura no Kasu', 'Sakura no Kasu',
            'Fuji no Kasu', 'Fuji no Kasu',
            'Ayame no Kasu', 'Ayame no Kasu',
            'Botan no Kasu', 'Botan no Kasu',
            'Hagi no Kasu', 'Hagi no Kasu',
            'Susuki no Kasu', 'Susuki no Kasu',
            'Kiku no Kasu', 'Kiku no Kasu',
            'Momiji no Kasu', 'Momiji no Kasu',
            'Yanagi no Kasu',
            'Kiri no Kasu', 'Kiri no Kasu', 'Kiri no Kasu'
        ]
        self.remaining = list(self.required)
        self.collected = []
        self.name = 'Kasu'
        self.value = 1

    def tally_points(self) -> int:
        if self.complete:
            xtra_pts = self.count - self.value
            if xtra_pts > 0:
                return self.value + xtra_pts
            else:
                return self.value
        else:
            return 0

    @property
    def complete(self):
        return self.count >= 10
