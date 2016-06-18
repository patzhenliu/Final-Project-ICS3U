import pygame
import Menu
import Level
import Story
import Progress
import Helpers


class Game:
    """
    main class - to create game and to run it
    """

    def __init__(self):
        """
        creates game
        """

        pygame.init()

        # constants:
        self.clock = pygame.time.Clock()
        self.behaviour = pygame.RESIZABLE
        self.screensize = (800,500)
        self.caption = "Documents Desired"
        self.fps = 40  # frames per second speed of game
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        # set screen:
        self.screen = pygame.display.set_mode(self.screensize)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        pygame.display.set_caption(self.caption)
        self.icon = Helpers.load_image("images/menu/logoMini.png")
        pygame.display.set_icon(self.icon)

        # game and menu objects
        self.menu = Menu.Menu(self.screen)
        self.level = Level.Level(self.screen)
        self.story = Story.Story(self.screen)
        self.progress = Progress.Progress()
        self.progress.load_progress()
        self.currentLevel = None

        self.levelSummary = None
        self.pauseMenu = False
        # menu,  - menu screen
        # lev1,  - play level 1
        # lev2,  - play level 2
        # lev3,  - play level 3
        # lev4,  - play level 4
        # levelSummary
        # end
        self.page = "menu"

    def run(self):
        """
        Runs the game. This is main game loop
        :return:
        """
        running = True
        while running:
            self.screen.fill(self.black)
            keys = pygame.key.get_pressed()
            mx, my = pygame.mouse.get_pos()
            mb = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                # quit on q or window QUIT button
                if event.type == pygame.QUIT: #or keys[pygame.K_q]:
                    running = False

            self.menu.play_music(self.page)

            # main menu ************************************
            if self.page == "menu":
                self.page = self.menu.draw_start_menu(mx, my, mb, event)

            # credits ************************************
            elif self.page == "credits":
                self.page = self.menu.draw_credit_menu(mx, my, mb, event)

            # select levels ************************************
            elif self.page == "levelSelect":
                self.page = self.menu.draw_level_select_menu(mx, my, mb, event, self.progress)
                self.level.clear_level()
                self.story.reset_slides()

            # play levels ************************************
            elif self.page == "lev1":
                self.currentLevel = 1
                if self.story.process(mb, event, 1):
                    self._run_level(1, mx, my, mb, event, keys)

            elif self.page == "lev2":
                self.currentLevel = 2
                if self.story.process(mb, event, 2):
                    self._run_level(2, mx, my, mb, event, keys)

            elif self.page == "lev3":
                self.currentLevel = 3
                if self.story.process(mb, event, 3):
                    self._run_level(3, mx, my, mb, event, keys)

            elif self.page == "lev4":
                self.currentLevel = 4
                if self.story.process(mb, event, 4):
                    self._run_level(4, mx, my, mb, event, keys)


            # end level summary ********************************
            elif self.page == "levelSummary":
                self.levelSummary.set_progress(self.progress)
                if self.levelSummary.process(mx, my, mb, event):
                    self.progress.save_level(self.levelSummary)
                    self.progress.load_progress()
                    self.page = self._check_ending(mb, event)

            # end level summary ********************************
            elif self.page == "end":
                self.page = self._check_ending(mb, event)

            self._print_x_y_position(self.screen, mx, my)
            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()

    def _run_level(self, level_num, mx, my, mb, event, keys):
        if self.level.clearLevel:
            # start new Level
            self.level = Level.Level(self.screen)
        if not self.pauseMenu:
            # run level if not game paused. Keep updated summary
            self.levelSummary = self.level.run(level_num, mx, my, mb, event)
        if self.levelSummary.LevelOver:
            # level is completed!
            self.levelSummary.set_progress(self.progress)
            self.story.reset_slides()
            self.page = "levelSummary"

        # pause level on escape
        if keys[pygame.K_ESCAPE]:
            self.pauseMenu = True
        if self.pauseMenu:
            self.menu.draw_escape_screen(mx, my, mb)
            if mb[0] == 1:
                self.menu.esc_screen_highlight(mx, my)
            if event.type == pygame.MOUSEBUTTONUP and mb[0]==1:
                self.pauseMenu, self.page, running = self.menu.esc_screen_select(mx, my, level_num)

    def _check_ending(self, mb, event):
        # checks if an ending occurs otherwise none occurs
        progressLevels = self.progress.levels
        ending_type = 9

        got_citation = False
        hungry_count = 0
        cold_count = 0

        self._order_process(progressLevels)

        for i in range(self.currentLevel):
            if progressLevels[i].familyCold:
                cold_count += 1
            else:
                cold_count = 0
            if progressLevels[i].familyHungry:
                hungry_count += 1
            else:
                hungry_count = 0
            if progressLevels[i].gotCitation:
                got_citation = True

        # 6: jail - you are in debt
        if progressLevels[self.currentLevel - 1].Credits < 0:
            self.levelSummary.levelCompleted = False
            self.progress.save_level(self.levelSummary)
            ending_type = 6

        # 5 family dead - 2 feeding or 2 heating in a row
        elif hungry_count >= 2 or cold_count >= 2:
            self.levelSummary.levelCompleted = False
            self.progress.save_level(self.levelSummary)
            ending_type = 5

        # 8:  # full ending without citations
        elif not got_citation and self.currentLevel == 4:
            ending_type = 8

        # 7:  # full ending with citations
        elif self.currentLevel == 4:
            ending_type = 7

        # if all pass we go to level summary after slides:
        if self.story.process(mb, event, ending_type):
            return "levelSelect"
        return "end"

    def _print_x_y_position(self, screen, x, y):
        # for debugging, getting x and y position for fun :)
        if Helpers.DEBUG:
            coordinates_font = pygame.font.SysFont("Myriad Pro", 15)
            coordinates = coordinates_font.render(str(x) + "," + str(y), 1, self.white, self.black)
            screen.blit(coordinates, (5, 5))

    def _order_process(self, progressLevels):
        sorted(progressLevels, key=lambda level: level.LevelNumber)  # sort by LevelNumber
