import pygame
import Helpers


class Story:

    def __init__(self, screen):
        """
            it shows set of images in sequence
            Used for tutorials or for story
        :param screen:
            blitting stuff
        """

        self.screen = screen

        #level 1 tutorial intro
        self.slide1 = Helpers.load_image("images/intro/Intro0.png")
        self.slide2 = Helpers.load_image("images/intro/Intro2.png")
        self.slide3 = Helpers.load_image("images/intro/Intro3.png")
        self.slide4 = Helpers.load_image("images/intro/DeskIntro.png")
        self.slide5 = Helpers.load_image("images/intro/TableTopIntro.png")
        self.slide6 = Helpers.load_image("images/intro/DocumentIntro.png")
        self.slide7 = Helpers.load_image("images/intro/StampIntro.png")
        self.slide7a = Helpers.load_image("images/intro/returnIntro.png")
        self.slide8 = Helpers.load_image("images/intro/IntercomIntro.png")
        self.slide8a = Helpers.load_image("images/intro/escapeIntro.png")
        #lev 2  tutorial intro
        self.slide9 = Helpers.load_image("images/intro/badgeIntro.png")
        #lev 3 tutorial intro
        self.slide10 = Helpers.load_image("images/intro/SpeechIntro.png")
        #lev 4 tutorial intro
        self.slide11 = Helpers.load_image("images/intro/lastIntro.png")
        #endings
        self.slide12 = Helpers.load_image("images/intro/FamilyDead.png")
        self.slide13 = Helpers.load_image("images/intro/arrestedEnding1.png")
        self.slide14 = Helpers.load_image("images/intro/arrestedEnding2.png")
        self.slide15 = Helpers.load_image("images/intro/arrestedEnding3.png")
        self.slide16 = Helpers.load_image("images/intro/fullEnding1.png")
        self.slide17 = Helpers.load_image("images/intro/fullEnding2.png")
        self.slide18 = Helpers.load_image("images/intro/happyEnding1.png")
        self.slide19 = Helpers.load_image("images/intro/happyEnding2.png")

        self.slides = []
        self.currentSlide = 0

    def reset_slides(self):
        # make sure slide counter reset after each slideshow
        self.currentSlide = -1

    def process(self, mb, event, story_number):
        # shows set of slides depending on story number
        if mb[0] == 1 and event.type == pygame.MOUSEBUTTONUP:
            self.currentSlide += 1

        if story_number == 1:
            self.slides = [self.slide1, self.slide2, self.slide3, self.slide4, self.slide5,
                           self.slide6, self.slide7, self.slide7a, self.slide8, self.slide8a]
        elif story_number == 2:
            self.slides = [self.slide9]
        elif story_number == 3:
            self.slides = [self.slide10]
        elif story_number == 4:
            self.slides = [self.slide11]

        elif story_number == 5:  # family dead - 2 feeding or 2 heating in a row
            self.slides = [self.slide12]
        elif story_number == 6:  # jail - you are in debt
            self.slides = [self.slide13, self.slide14, self.slide15]
        elif story_number == 7:  # full ending with citations
            self.slides = [self.slide16, self.slide17]
        elif story_number == 8:  # full ending without citations
            self.slides = [self.slide18, self.slide19]
        elif story_number == 9:
            return True # nothig to show here

        if self.currentSlide >= len(self.slides):
            return True
        else:
            if self.currentSlide < 0:
                self.currentSlide = 0
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.slides[self.currentSlide], (0, 0))
        return False
