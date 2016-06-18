import pygame
import Helpers


class LevelSummary:

    def __init__(self, screen, num):
        """
        creating summary for end of level (budgeting money)
        :param screen:
            blitting stuff
        :param num:
            level num
        """

        # defining variable ********************
        self.screen = screen
        self.clientsProcessed = 0
        self.numberOfCitations = 0
        self.moneyPerClient = 5
        self.progress = None
        self.foodPrice = 15
        self.heatPrice = 10
        self.rentPrice = 20

        # your family members
        self.familyNames = ["Wife", "Son", "Daughter"]

        self.LevelNumber = num
        self.LevelOver = False
        self.foodOption = False
        self.heatOption = False
        self.levelCompleted = True

        # load images
        self.pushButton = Helpers.load_image("images/menu/PushButton.png")
        self.pushButtonClick = Helpers.load_image("images/menu/PushButtonClick.png")
        self.ok_icon = Helpers.load_image("images/ok_emotion.png")
        self.hungry_icon = Helpers.load_image("images/hungry_emotion.png")
        self.cold_icon = Helpers.load_image("images/cold_emotion.png")
        self.sleep = Helpers.load_image("images/menu/sleep.png")
        self.sleepClick = Helpers.load_image("images/menu/sleepClicked.png")
        self.check = Helpers.load_image("images/BudgetLineCheck.png")
        self.checkClick = Helpers.load_image("images/BudgetLineClick.png")

        # load sound
        self.clickSound = pygame.mixer.Sound("music/button-drop.wav")
        self.clickSound.set_volume(0.5)

        # fonts and text
        self.font = pygame.font.SysFont("Arial", 20, True)
        self.title_font = pygame.font.SysFont("Arial", 60, True)
        self.title = self.title_font.render("BUDGET", 1, (255, 255, 255))

        # image for whether food/heat is checked off or not
        self.check_food_image = self.check
        self.check_heat_image = self.check

        self.correctly_processed = self.clientsProcessed - self.numberOfCitations
        self.totalMuns = self.correctly_processed * self.moneyPerClient - self.rentPrice # total money after budgeting

    def set_client(self, num):
        # updating number of clients processed
        self.clientsProcessed = num
        self.correctly_processed = self.clientsProcessed - self.numberOfCitations
        self.totalMuns = self.correctly_processed * self.moneyPerClient - self.rentPrice

    def add_citation(self):
        # updating number of citations received
        self.numberOfCitations += 1
        self.correctly_processed = self.clientsProcessed - self.numberOfCitations
        self.totalMuns = self.correctly_processed * self.moneyPerClient - self.rentPrice

    def level_over(self):
        # sets level as completed
        self.LevelOver = True

    def set_progress(self, progress):
        # update progress with current level info
        self.progress = progress
        self.progress.save_level(self)

    def process(self, mx, my, mb, event):
        # runs all the printing/checking etc. for level summary (budgeting)
        self.screen.fill((0, 0, 0))
        self.select_food(mx, my, mb, event)
        self.select_heat(mx, my, mb, event)
        self.print()
        self.highlight_sleep(mx, my, mb)
        return self.select_sleep(mx, my, event) #if click sleep

    def print(self):
        # all the visual stuff (blitting)
        # load previous level info
        cold = False
        hungry = False
        savings = 0
        for l in self.progress.levels:
            if l.LevelNumber == self.LevelNumber - 1:
                cold = l.familyCold
                hungry = l.familyHungry
                savings = l.Credits

        # TEXT ******************
        salary = self.font.render("Salary(" + str(self.correctly_processed) + ")" +
                                   " " * 40 + str(self.correctly_processed * self.moneyPerClient), 1, (255, 255, 255))
        dash = self.font.render("-" * 50, 1, (255, 255, 255))
        rent = self.font.render("Rent" + " " * 45 + str(self.rentPrice), 1, (255, 255, 255))
        food = self.font.render("Food" + " " * 44 + str(0 - self.foodPrice), 1, (255, 255, 255))
        heat = self.font.render("Heat" + " " * 45 + str(0 - self.heatPrice), 1, (255, 255, 255))

        total_text = self.font.render(str(self.totalMuns), 1, (255, 255, 255))

        savings_text = self.font.render("Saving"+" " * 43 + str(savings), 1, (255, 255, 255))

        self.screen.blit(savings_text, (100, 110))
        self.screen.blit(salary, (100, 140))
        self.screen.blit(dash, (100, 160))
        self.screen.blit(rent, (100, 190))
        self.screen.blit(food, (100, 230))
        self.screen.blit(heat, (100, 270))
        pygame.draw.line(self.screen, (255, 255, 255), (100, 310), (400, 310), 2)
        self.screen.blit(total_text, (360, 335))

        # food/heat check circles
        self.screen.blit(self.check_food_image, (410, 234))
        self.screen.blit(self.check_heat_image, (410, 274))

        # title
        self.screen.blit(self.title, (280, 15))
        pygame.draw.line(self.screen, (141, 166, 141), (0, 90), (800, 90), 1)

        # sleep button
        self.screen.blit(self.pushButton, (267, 410))
        self.screen.blit(self.sleep, (367, 415))

        # blit family names
        for i in range(3):
            text = self.font.render(self.familyNames[i], 1, (255, 255, 255))
            self.screen.blit(text, (470 + 100 * i, 140))

        # blitting family status
        if not cold and not hungry:
            self.screen.blit(self.ok_icon, (473, 170))
            self.screen.blit(self.ok_icon, (573, 170))
            self.screen.blit(self.ok_icon, (695, 170))
        elif cold and not hungry:
            self.screen.blit(self.cold_icon, (473, 170))
            self.screen.blit(self.cold_icon, (573, 170))
            self.screen.blit(self.cold_icon, (695, 170))
        elif hungry and not cold:
            self.screen.blit(self.hungry_icon, (473, 170))
            self.screen.blit(self.hungry_icon, (573, 170))
            self.screen.blit(self.hungry_icon, (695, 170))
        else:
            self.screen.blit(self.cold_icon, (473, 220))
            self.screen.blit(self.cold_icon, (573, 220))
            self.screen.blit(self.cold_icon, (695, 220))

            self.screen.blit(self.hungry_icon, (473, 170))
            self.screen.blit(self.hungry_icon, (573, 170))
            self.screen.blit(self.hungry_icon, (695, 170))

    def select_food(self, mx, my, mb, event):
        # checks if food option is selected
        if pygame.Rect(410, 234, 16, 16).collidepoint(mx, my) and event.type == pygame.MOUSEBUTTONUP and mb[0] == 1:
            if self.totalMuns < self.foodPrice and not self.foodOption:
                return

            self.foodOption = not self.foodOption
            if self.foodOption and self.totalMuns >= self.foodPrice:
                self.check_food_image = self.checkClick
                self.totalMuns -= self.foodPrice
            if not self.foodOption:
                self.check_food_image = self.check
                self.totalMuns += self.foodPrice

    def select_heat(self, mx, my, mb, event):
        # checks if heat option is selected
        if pygame.Rect(410, 274, 16, 16).collidepoint(mx, my) and event.type == pygame.MOUSEBUTTONUP and mb[0] == 1:
            if self.totalMuns < self.heatPrice and not self.heatOption:
                return

            self.heatOption = not self.heatOption
            if self.heatOption and self.totalMuns >= self.heatPrice:
                self.check_heat_image = self.checkClick
                self.totalMuns -= self.heatPrice
            if not self.heatOption:
                self.check_heat_image = self.check
                self.totalMuns += self.heatPrice

    def highlight_sleep(self, mx, my, mb):
        # changes colour when clicked
        if mb[0] == 1:
            if pygame.Rect(267, 410, 266, 37).collidepoint(mx, my):
                self.screen.blit(self.pushButtonClick, (267, 410))
                self.screen.blit(self.sleepClick, (367, 415))

    def select_sleep(self, mx, my, event):
        """
        when click sleep button, exit level summary
        :return:
            True - clicked
            False - otherwise
        """

        if event.type == pygame.MOUSEBUTTONUP:
            if pygame.Rect(267, 410, 266, 37).collidepoint(mx, my):
                self.clickSound.play()
                return True
            return False
