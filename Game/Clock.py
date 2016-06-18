import pygame
import math


class Clock:

    def __init__(self, screen, pos):
        """
        creating clock referring to the in game time in top right corner of level
        :param screen:
            blitting stuff
        :param pos:
            position of blitting clock text
        """
        self.screen = screen
        self.pos = pos
        self.clock_font = pygame.font.SysFont("Arial", 30, True)
        self.time_counter = 0
        self.times = ["9:00", "9:30",
                 "10:00", "10:30",
                 "11:00", "11:30",
                 "12:00", "12:30",
                 "1:00", "1:30",
                 "2:00", "2:30",
                 "3:00", "3:30",
                 "4:00", "4:30",
                 "5:00"
                 ]
        self.can_start = False

    def start(self):
        # start clock (when intercom is first clicked in level -> will call this function)
        self.can_start = True

    def draw_time(self, text):
        # drawing the clock text
        clock_text = self.clock_font.render(text, 0, (0,255,0))
        self.screen.blit(clock_text, (725 - clock_text.get_width()//2, self.pos[1],350, 70))

    def draw(self, ticks):
        """
        controls the speed at which the clock changes time
        :param ticks:
            speed at which clock ticks
        :return:
            True - when it reaches 5 pm
            False - otherwise
        """
        if self.can_start:
            self.time_counter += 1
            if self.time_counter // ticks > len(self.times) - 1:
                self.draw_time(self.times[len(self.times) - 1])
            else:
                self.draw_time(self.times[self.time_counter // ticks])
            return self.time_counter > ticks * len(self.times)
        else:
            self.draw_time(self.times[0])
            return False