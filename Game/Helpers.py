import pygame
import os

# global variable to turn on or off printing debug messages
DEBUG = False


class Point:
    """
    help manipulate point
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_up(self, move):
        self.y -= move

    def move_down(self, move):
        self.y += move

    def move_right(self, move):
        self.x += move

    def move_left(self, move):
        self.x -= move

    def get_xy(self):
        return self.x, self.y

    def clone(self):
        return Point(self.x, self.y)

def load_image(path, color_key=None):
    # makes it easier to load images and option of transparency with color_key
    # pass color_key as -1 to pick right top pixel as transparent color
    fullname = ""
    for name in path.split('/'):
        fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:' + fullname)
        raise SystemExit(message)
    image = image.convert()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))  # make top right pixel of the image transparent
        image.set_colorkey(color_key, pygame.RLEACCEL)
    return image
