import pygame
import Helpers


class Menu:
    # creates all menu stuff: credits, level select, pause menu
    def __init__(self, screen):
        # array for levels data from progress text file
        self.levels = []

        # load images
        self.logo = Helpers.load_image("images/menu/Logo.png")
        self.pushButton = Helpers.load_image("images/menu/PushButton.png")
        self.pushButtonClick = Helpers.load_image("images/menu/PushButtonClick.png")
        self.loadButtonNew = Helpers.load_image("images/menu/LoadButtonNew.png")
        self.loadButtonNewClick = Helpers.load_image("images/menu/LoadButtonNewClick.png")

        self.storyText = Helpers.load_image("images/menu/story.png")
        self.storyTextClicked = Helpers.load_image("images/menu/storyClicked.png")
        self.creditsText = Helpers.load_image("images/menu/credits.png")
        self.creditsTextClicked = Helpers.load_image("images/menu/creditsClicked.png")
        self.backText = Helpers.load_image("images/menu/back.png")
        self.backTextClicked = Helpers.load_image("images/menu/backClicked.png")
        self.resumeText = Helpers.load_image("images/menu/resume.png")
        self.resumeTextClicked = Helpers.load_image("images/menu/resumeClicked.png")
        self.mainMenuText = Helpers.load_image("images/menu/main_menu.png")
        self.mainMenuTextClicked = Helpers.load_image("images/menu/main_menuClicked.png")

        self.day1Text = Helpers.load_image("images/menu/day1.png")
        self.day2Text = Helpers.load_image("images/menu/day2.png")
        self.day3Text = Helpers.load_image("images/menu/day3.png")
        self.day4Text = Helpers.load_image("images/menu/day4.png")
        self.dayImages = [self.day1Text, self.day2Text, self.day3Text, self.day4Text]

        self.credits_image = Helpers.load_image("images/menu/creditPage.png")

        # loading music/sounds
        pygame.mixer.music.load("music/Paper Please Theme Ringtone.mp3")
        self.clickSound = pygame.mixer.Sound("music/button-drop.wav")
        self.clickSound.set_volume(0.5)

        #scroll credits initial y pos
        self.credit_y = 499

        self.screen = screen

        # fonts and text
        self.date_font = pygame.font.SysFont("Arial", 16)
        self.lastPlayedText = self.date_font.render("LastPlayed", 1, (255, 255, 255))
        self.font = pygame.font.SysFont("Arial", 60, True)
        self.textTop = self.font.render("DOCUMENTS", 1, (255, 255, 255))
        self.textBottom = self.font.render("DESIRED", 1, (255, 255, 255))
        self.textTopDark = self.font.render("DOCUMENTS", 1, (121, 121, 121))
        self.textBottomDark = self.font.render("DESIRED", 1, (121, 121, 121))
        self.levelSelectText = self.font.render("SELECT A LEVEL TO PLAY", 1, (255, 255, 255))
        self.pauseTop = self.font.render("PAUSE", 1, (255, 255, 255))
        self.pauseBottom = self.font.render("MENU", 1, (255, 255, 255))

        # resizing new button for level one in level select
        self.loadButtonNew = pygame.transform.scale(self.loadButtonNew, (100, 50))
        self.loadButtonNewClick = pygame.transform.scale(self.loadButtonNewClick, (100, 50))

        # rects for all levels
        self.day1Rect = pygame.Rect(100, 200, 100, 50)
        self.day2Rect = pygame.Rect(260, 200, 100, 50)
        self.day3Rect = pygame.Rect(420, 200, 100, 50)
        self.day4Rect = pygame.Rect(580, 200, 100, 50)

        # dates that levels were played
        self.playedDates = []

    def play_music(self, page):
        """
        play music according to game page
        :param page:
            game page
        """
        if page == "menu" or page == "levelSelect" or page == "credits" or page == "levelSummary":
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.set_volume(0.99)
                pygame.mixer.music.play()
        else:
            pygame.mixer.music.fadeout(10000)

    def draw_start_menu(self, mx, my, mb, event):
        """
        Draw start menu - credits and story
        :return:
            return what page game need to go next
        """
        self.screen.fill((0, 0, 0))
        for i in range(2):
            self.screen.blit(self.pushButton,(267,343 + 40 * i))
        self.screen.blit(self.storyText, (370, 347))
        self.screen.blit(self.creditsText, (367, 387))

        self.screen.blit(self.logo, (320, 100))
        self.screen.blit(self.textTopDark, (250, 135))
        self.screen.blit(self.textBottomDark, (300, 195))
        self.screen.blit(self.textTop, (250, 130))
        self.screen.blit(self.textBottom, (300, 190))

        if mb[0] == 1:
            self._highlight_story(mx, my)
            self._highlight_credits(mx, my)
        if mb[0] == 1 and event.type == pygame.MOUSEBUTTONUP:
            if self.select_story(mx, my):
                return "levelSelect"
            if self.select_credits(mx, my):
                return "credits"
        return "menu"

    def draw_credit_menu(self, mx, my, mb, event):
        """
        Draw credit scroll - exit on click
        :return:
            return what page game need to go next
        """
        if not self._credits_page_running():
            self.credits_reset()
            return "menu"
        if mb[0] == 1 and event.type == pygame.MOUSEBUTTONUP:
            self.credits_reset()
            return "menu"
        return "credits"

    # internal functions *******************

    def _credits_page_running(self):
        # show credit scolling up by changing y position
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.credits_image, (0, self.credit_y))
        self.credit_y -= 1
        return self.credit_y >= -1060

    def _highlight_story(self, mx, my):
        # highlight story button when clicked
        if pygame.Rect(267, 343, 266, 32).collidepoint(mx, my):
            self.screen.blit(self.pushButtonClick, (267, 343))
            self.screen.blit(self.storyTextClicked, (370, 347))

    def _highlight_credits(self, mx, my):
        # highlight credit button when clicked
        if pygame.Rect(267, 383, 266, 32).collidepoint(mx, my):
            self.screen.blit(self.pushButtonClick,(267, 383))
            self.screen.blit(self.creditsTextClicked, (367, 387))

    def draw_level_select_menu(self, mx, my, mb, event, progress):
        """
        draw select levels page
        :param progress:
            progress shows dates on which levels have been played
        :return:
            return what page game need to go next
        """
        for l in progress.levels:
            if l.DatePlayed != "":
                self.playedDates.append(l.DatePlayed)

        self._draw_lev_select(progress)

        if mb[0] == 1:
            self.highlight_level(mx, my)
        if mb[0] == 1 and event.type == pygame.MOUSEBUTTONUP:
            return self.select_level(mx, my)
        return "levelSelect"

    def select_story(self, mx, my):
        # goes to level select page when clicked
        if pygame.Rect(267, 343, 266, 32).collidepoint(mx, my):
            self.clickSound.play()
            return True
        return False

    def select_credits(self, mx, my):
        # scrolls credit page when clicked
        if pygame.Rect(267, 383, 266, 32).collidepoint(mx, my):
            self.clickSound.play()
            self.screen.fill((0,0,0))
            return True
        return False

    def _draw_lev_select(self, progress):
        # all visual element of level select are drawn here
        self.levels = progress.levels

        count = 1
        for lev in self.levels:
            if lev.LevelCompleted:
                count += 1

        self.screen.fill((0,0,0))
        for i in range(count):
            if i != 0 and i <=3:
                pygame.draw.rect(self.screen, (255, 255, 255),[100 + 160 * i, 200, 100, 50], 2)
                self.dateText = self.date_font.render(self.playedDates[i-1], 1, (255, 255, 255))

                self.screen.blit(self.lastPlayedText, ([115 + 160 * i, 210, 100, 50]))
                self.screen.blit(self.dateText, ([115 + 160 * i, 225, 100, 50]))

        self.screen.blit(self.loadButtonNew, (100, 200))

        for i in range(2):
            pygame.draw.line(self.screen, (141, 166, 141), (0, 80 + 320 * i), (800, 80 + 320 * i), 1)

        for i in range(count):
            if i <= 3:
                self.screen.blit(self.dayImages[i], (135 + 160 * i, 140))

        self.screen.blit(self.pushButton, (267, 440))
        self.screen.blit(self.backText, (374, 445))
        self.screen.blit(self.levelSelectText, (90, 15))

    def highlight_level(self, mx, my):
        # level highlighted when clicked
        if self.day1Rect.collidepoint(mx, my):
            self.screen.blit(self.loadButtonNewClick, (100, 200))

        elif self.day2Rect.collidepoint(mx, my) and self.levels[0]:
            rect = pygame.Surface((98, 48), pygame.SRCALPHA, 32)
            rect.fill((141, 166, 141, 100))
            self.screen.blit(rect, (260, 200))
        elif self.day3Rect.collidepoint(mx, my) and self.levels[1]:
            rect = pygame.Surface((98, 48), pygame.SRCALPHA, 32)
            rect.fill((141, 166, 141, 100))
            self.screen.blit(rect, (420, 200))
        elif self.day4Rect.collidepoint(mx, my) and self.levels[2]:
            rect = pygame.Surface((98, 48), pygame.SRCALPHA, 32)
            rect.fill((141, 166, 141, 100))
            self.screen.blit(rect, (580, 200))

        self.highlight_back(mx, my)

    def select_level(self, mx, my):
        # goes to corresponding level when clicked
        if self.day1Rect.collidepoint(mx, my):
            self.clickSound.play()
            return "lev1"
        elif self.day2Rect.collidepoint(mx, my) and self.levels[0]:
            self.clickSound.play()
            return "lev2"
        elif self.day3Rect.collidepoint(mx, my) and self.levels[1]:
            self.clickSound.play()
            return "lev3"
        elif self.day4Rect.collidepoint(mx, my) and self.levels[2]:
            self.clickSound.play()
            return "lev4"

        elif self.select_back(mx, my):
            return "menu"

        return "levelSelect"

    def highlight_back(self, mx, my):
        # highlights back button when clicked
        if pygame.Rect(267, 440, 266, 32).collidepoint(mx, my):
            self.screen.blit(self.pushButtonClick, (267, 440))
            self.screen.blit(self.backTextClicked, (374, 445))

    def select_back(self, mx, my):
        # returns to start menu page when clicked
        if pygame.Rect(267, 440, 266, 32).collidepoint(mx, my):
            self.clickSound.play()
            self.screen.fill((0, 0, 0))
            return True
        return False

    def credits_reset(self):
        # resets the credit location (when exit - so that starts over again)
        self.credit_y = 499

    def draw_escape_screen(self, mx, my, mb):
        # draws the pause menu (while you are playing a level)
        # activated by escape ESC key
        self.screen.fill((0, 0, 0))
        for i in range(2):
            self.screen.blit(self.pushButton, (267, 300 + 40 * i))

        self.screen.blit(self.resumeText, (362, 305))
        self.screen.blit(self.mainMenuText, (347, 346))

        self.screen.blit(self.pauseTop, (315, 130))
        self.screen.blit(self.pauseBottom, (325, 190))


    def esc_screen_select(self, mx, my, levNum):
        # returns proper page according to mouse click in pause menu
        pauseMenu = True
        page = "lev" + str(levNum)
        running = True

        if self.select_resume(mx, my):
            pauseMenu, page, running = False, "lev" + str(levNum), True
        if self.select_main_menu(mx, my):
            pauseMenu, page, running = False, "levelSelect", True
            return False, "menu", True

        return pauseMenu, page, running

    def esc_screen_highlight(self, mx, my):
        # highlights resume and main menu when clicked
        self.highlight_resume(mx, my)
        self.highlight_main_menu(mx, my)

    def highlight_resume(self, mx, my):
        # highlight resume when clicked
        if pygame.Rect(267, 300, 266, 32).collidepoint(mx, my):
            self.screen.blit(self.pushButtonClick, (267, 300))
            self.screen.blit(self.resumeTextClicked, (362, 305))

    def select_resume(self, mx, my):
        # returns True to resume level
        if pygame.Rect(267, 300, 266, 32).collidepoint(mx, my):
            self.clickSound.play()
            return True
        return False

    def highlight_main_menu(self, mx, my):
        # highlight main menu on click
        if pygame.Rect(267, 340, 266, 32).collidepoint(mx, my):
            self.screen.blit(self.pushButtonClick, (267, 340))
            self.screen.blit(self.mainMenuTextClicked, (347, 346))

    def select_main_menu(self, mx, my):
        # returns True to return to the start menu
        if pygame.Rect(267, 340, 266, 32).collidepoint(mx, my):
            self.clickSound.play()
            return True
        return False
