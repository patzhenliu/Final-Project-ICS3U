import pygame
import Helpers


class Background:

    def __init__(self, screen):
        """
        creating the top portion of the game showing the workplace
        :param screen:
            screen for blitting things
        """
        # loading images
        self.image = Helpers.load_image("images/office.png")
        self.intercom = Helpers.load_image("images/intercom.png")
        self.screen = screen

        # setting positions
        self.top_left = (20, 20)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.top_left)

    def draw(self):
        # draw the office area at the top of the level
        self.screen.blit(self.image, self.top_left)

    def get_intercom_area(self):
        """
        :return:
            area for intercom (little white box)
        """
        return pygame.Rect(82,46,202,20)

    def highlight_intercom(self, mx, my):
        """
        blits circle around intercom when mouse is in contact w/ area
        :param mx:
            mouse pos x
        :param my:
            mouse pos y
        """
        if pygame.Rect(78, 45, 29, 27).collidepoint(mx,my):
            self.screen.blit(self.intercom, (78, 45))


