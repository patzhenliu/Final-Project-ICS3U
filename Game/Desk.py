import pygame
import Helpers


class Desk:

    def __init__(self, screen):
        """
        creating the bottom left portion of the game showing the office with desk and calendar
        :param screen:
            screen for blitting things
        """
        # loading images
        self.screen = screen
        self.image = Helpers.load_image("images/officething.png")
        self.background = Helpers.load_image("images/officeBack.png")
        self.calendar = Helpers.load_image("images/calendar.png")

        self.day1Date = Helpers.load_image("images/calendarDay1.png")
        self.day2Date = Helpers.load_image("images/calendarDay2.png")
        self.day3Date = Helpers.load_image("images/calendarDay3.png")
        self.day4Date = Helpers.load_image("images/calendarDay4.png")
        self.dateList = [self.day1Date, self.day2Date, self.day3Date, self.day4Date]

        # position:
        self.top_left = (20, 150)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.top_left)  # since we need rect for collision, move where it is drawn
        self.get_desk_ticket_position = 160, 380

    def draw(self, levelNum):
        # draw desk and calendar (bottom left)
        self.screen.blit(self.image, self.top_left)
        self.draw_calendar(levelNum)

    def draw_background(self):
        # draw gray wall background
        self.screen.blit(self.background, self.top_left)

    def draw_calendar(self, levelNum):
        # blitting calendar image with corresponding date
        self.screen.blit(self.calendar, (20, 310))
        self.screen.blit(self.dateList[levelNum - 1], (39, 327))