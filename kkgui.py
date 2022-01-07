from typing import Union
from inspect import getmembers
import pygame as pg
pg.font.init()


class Display:
    """This class contains settings for the display window."""
    WIDTH, HEIGHT = 1200, 800
    WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
    BACKGROUND = pg.image.load('Images/grey-hills-1280×800.jpg')
    BACK_POS = (WIDTH//2 - BACKGROUND.get_width()//2, HEIGHT//2 - BACKGROUND.get_height()//2)
    WIN_COLOR = (20, 70, 180)  # ROYAL BLUE
    pg.display.set_caption('Project Koi-Koi')
    pg.display.set_icon(pg.image.load('Images/imgbin_hanafuda-playing-card-card-game-flowers-game-emoji-png.png'))

    RGB_YELLOW = (255, 255, 0)
    RGB_RED = (225, 25, 0)
    RGB_WHITE = (255, 255, 255)
    RGB_BLACK = (0, 0, 0)

    FONT_NAME = 'Fonts/Nau Sea.otf'
    FONT = pg.font.Font(FONT_NAME, 20)
    FONT_COLOR = RGB_WHITE

    FPS = 30
    FRAME = 0
    EXPAND_ROW = False
    EXPAND_COL = False

    @staticmethod
    def draw_images(images: list, positions: Union[list | tuple]):
        Display.WINDOW.blits(zip(images, positions))

    @classmethod
    def draw_window(cls):
        # cls.WINDOW.blit(cls.BACKGROUND, cls.BACK_POS)
        cls.WINDOW.fill(cls.WIN_COLOR)
        cls.FRAME = (cls.FRAME + 1) % cls.FPS


class MessageBox:
    """This class controls settings for displayed messages."""
    def __init__(self,
                 position=(0.0, 0.0),
                 text='',
                 font=Display.FONT_NAME,
                 size=20,
                 color=Display.FONT_COLOR,
                 background=None
                 ):
        self.position = position
        self.text = text
        self._font = font
        self._size = size
        self.color = color
        self.background = background

    def draw(self):
        message = self.font.render(self.text, True, self.color, self.background)
        Display.WINDOW.blit(message, self.position)

    def center(self, horiz=True, vert=True):
        x, y = self.position
        msg_width, msg_height = self.font.size(self.text)
        win_width, win_height = Display.WIDTH, Display.HEIGHT

        new_x, new_y = x, y
        if horiz:
            new_x = win_width/2 - msg_width/2
        if vert:
            new_y = win_height/2 - msg_height

        self.position = (new_x, new_y)

    def change_font(self, name='', size=0):
        if name:
            self._font = name
        if size > 0:
            self._size = size

    @property
    def font(self) -> pg.font.Font:
        return pg.font.Font(self._font, self._size)

    @property
    def size(self) -> int:
        return self._size


class Box(pg.Rect):
    """This object is the bridge between the interface and the main loop."""
    def __init__(self, dimensions: tuple[float, float, float, float], box_name):
        super().__init__(*dimensions)
        self.name = box_name
        self.flash = False
        self.active = False
        self.color1 = Display.RGB_RED
        self.color2 = None
        self.color3 = None

    def __repr__(self):
        return f'{self.__class__.__name__} {self.name}'

    @staticmethod
    def highlight(box_list, color=Display.RGB_YELLOW):
        interval = Display.FPS // 2
        for box in box_list:
            if Display.FRAME >= interval and box.active:
                pg.draw.rect(Display.WINDOW, color, box,
                             width=5,
                             border_radius=10)


class DisplayData:
    """This class draws the images and text to the window."""
    TITLE = pg.display.get_caption()
    TITLE_POS = (50, 10)
    TITLE_MSG = MessageBox(TITLE_POS, text=TITLE[1], color=Display.RGB_WHITE)

    START_BUTTON = Box((400, 600, 400, 50), 'Start Button')
    START_BUTTON.color1, START_BUTTON.color2 = Display.RGB_BLACK, Display.RGB_YELLOW
    START_BTN_TEXT = MessageBox((0, START_BUTTON.y), text='PLAY GAME', size=48, color=Display.RGB_BLACK)
    START_BTN_TEXT.center(vert=False)

    IMAGES = []
    POSITIONS = []

    MSG_FONT = 'Fonts/LLPIXEL3.ttf'
    MSG_SIZE = 24

    @classmethod
    def get_messages(cls) -> list[MessageBox]:
        # Center messages after text is set.
        cls.TITLE_MSG.position = DisplayData.TITLE_POS
        cls.TITLE_MSG.change_font(size=36)
        for msg in []:
            msg.center(vert=False)

        return [getattr(cls, attr[0]) for attr in getmembers(cls) if attr[0].endswith('_MSG')]

    @classmethod
    def draw_msg(cls):
        Display.WINDOW.blits(zip(cls.IMAGES, cls.POSITIONS))
        for msg in cls.get_messages():
            msg.draw()

    @classmethod
    def draw_start(cls):
        """Draws the start screen displayed upon loading."""
        Display.WINDOW.blit(Display.BACKGROUND, Display.BACK_POS)
        # Display.WINDOW.fill(Display.WIN_COLOR)

        cls.TITLE_MSG.change_font(size=64)
        cls.TITLE_MSG.center()
        cls.TITLE_MSG.draw()

        if mouse_over(cls.START_BUTTON):
            cls.START_BUTTON.color1 = Display.RGB_YELLOW
            cls.START_BTN_TEXT.color = Display.RGB_BLACK
        else:
            cls.START_BUTTON.color1 = Display.RGB_BLACK
            cls.START_BTN_TEXT.color = Display.RGB_YELLOW
        pg.draw.rect(Display.WINDOW, cls.START_BUTTON.color1, cls.START_BUTTON, 0, 10, 10, 10, 10)
        cls.START_BTN_TEXT.draw()


def mouse_over(surface: pg.Rect | pg.Surface) -> bool:
    mouse_pos = pg.mouse.get_pos()
    if type(surface) is pg.Surface:
        surf_rect = surface.get_rect()
    else:
        surf_rect = surface
    return surf_rect.collidepoint(mouse_pos)


def get_mouse_over(rect_list: list[pg.Rect]) -> pg.Rect:
    for rect in rect_list:
        if mouse_over(rect):
            return rect


def draw_table():
    pass
