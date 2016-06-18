import pygame
import Helpers
import Document


class Stamp:

    def __init__(self, screen):
        """
        this object is for the stamp that appears on the table top on the middle right section of the screen
        :param screen:
            blitting stuff
        """
        self.screen = screen

        # load pictures and set up Approved and Denied stamp positions
        self.approveStamp = Document.SubDocument("images/stamp/InkApproved.png", None)
        self.approveStamp.rect.topleft = (598, 295)
        self.approveStamp.approved = True
        self.deniedStamp = Document.SubDocument("images/stamp/InkDenied.png", None)
        self.deniedStamp.rect.topleft = (406, 295)
        self.deniedStamp.approved = False

        # load pictures related to the popup stamp bar
        self.approveBot = Helpers.load_image("images/stamp/StampBotApproved.png")
        self.deniedBot = Helpers.load_image("images/stamp/StampBotDenied.png")
        self.barTop = Helpers.load_image("images/stamp/StampBarTop.png")
        self.barMid = Helpers.load_image("images/stamp/StampBarMid.png")

        # stamp bot locations
        self.ApprovedLocation = None
        self.DeniedLocation = None

        # position:
        self.startPoint = Helpers.Point(760, 200)
        self.endPoint = Helpers.Point(342, 200)
        self.currentLocation = self.startPoint.clone()
        self.isMoving = "none" # "right" "left"
        self.bar_speed = 20

        # variables for speed and stamp movement
        self.stampMovement = "none"  # "deny-down" "deny-up" "approve-down" "approve-up"
        self.stamp_speed = 8
        self.deny_y = 20
        self.approve_y = 20

        # load sounds
        self.stampBarOpen = pygame.mixer.Sound("music/stampbar-open.wav")
        self.stampBarClose = pygame.mixer.Sound("music/stampbar-close.wav")
        self.stampSound = pygame.mixer.Sound("music/button-drop.wav")

        self.draw()

    def process(self, mx, my, mb, event):
        # drawing the stamp bots on the screen (whether they are pulling in or out when clicking in arrow)
        self.pull_check(mx, my, mb, event)
        stampImage = self.stamp_check(mx, my, mb, event)
        self.draw()
        return stampImage

    def draw(self):
        # draw all stamp parts:
        self.screen.blit(self.barTop, self.currentLocation.get_xy() )

        # draw approved
        self.ApprovedLocation = self.currentLocation.clone()
        self.ApprovedLocation.move_right(256)
        self.ApprovedLocation.move_up(self.approve_y)
        self.screen.blit(self.approveBot, self.ApprovedLocation.get_xy())

        # draw denied
        self.DeniedLocation = self.currentLocation.clone()
        self.DeniedLocation.move_right(64)
        self.DeniedLocation.move_up(self.deny_y)
        self.screen.blit(self.deniedBot, self.DeniedLocation.get_xy())

        # draw bottom
        MidBarLocation = self.currentLocation.clone()
        MidBarLocation.move_down(75)
        self.screen.blit(self.barMid, MidBarLocation.get_xy())
        # draw border
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, 780, 480), 20)

    def is_mouse_over_stamp_area(self, mx, my):
        area = pygame.Rect(self.currentLocation.x, self.currentLocation.y, 280, 63)
        return area.collidepoint(mx, my)

    def pull_check(self, mx, my, mb, event):
        # check and set stamp bot in motion
        self.is_bar_arrow_clicked(mx, my, mb, event)
        if self.isMoving == "right":
            self.pull_in()
        if self.isMoving == "left":
            self.pull_out()

    def pull_out(self):
        # pull bar out
        if self.currentLocation.x > self.endPoint.x:
            self.currentLocation.move_left(self.bar_speed)
        if self.currentLocation.x <= self.endPoint.x:
            self.currentLocation.x = self.endPoint.x
            self.isMoving = "none"

    def pull_in(self):
        # pull bar in
        if self.currentLocation.x < self.startPoint.x:
            self.currentLocation.move_right(self.bar_speed)
        if self.currentLocation.x >= self.startPoint.x:
            self.currentLocation.x = self.startPoint.x
            self.isMoving = "none"

    def is_bar_arrow_clicked(self, mx, my, mb, event):
        keys = pygame.key.get_pressed()
        if (mb[0] == 1 and event.type == pygame.MOUSEBUTTONUP) and self.isMoving == "none":
            click_rect = pygame.Rect(self.currentLocation.x, self.currentLocation.y + 10, 15, 80)
            if click_rect.collidepoint(mx, my):
                if self.startPoint.x == self.currentLocation.x:
                    self.stampBarOpen.play()
                    self.isMoving = "left"
                if self.endPoint.x == self.currentLocation.x:
                    self.stampBarClose.play()
                    self.isMoving = "right"

    def stamp_check(self, mx, my, mb, event):
        # set the stamp bots in motion
        if self.stampMovement == "none":
            if self.is_denied_clicked(mx, my, mb, event):
                self.stampSound.play()
                self.stampMovement = "deny-down"
            if self.is_approved_clicked(mx, my, mb, event):
                self.stampSound.play()
                self.stampMovement = "approve-down"
        if self.stampMovement[:7] == "approve":
            return self.stamp_approve()
        if self.stampMovement[:4] == "deny":
            return self.stamp_deny()
        return None

    def is_denied_clicked(self, mx, my, mb, event):
        denied_rect = pygame.Rect(self.DeniedLocation.x, self.DeniedLocation.y, self.deniedBot.get_rect().w, self.deniedBot.get_rect().h)
        if self.endPoint.x == self.currentLocation.x and mb[0] == 1 and event.type == pygame.MOUSEBUTTONUP:
            return denied_rect.collidepoint(mx, my)

    def is_approved_clicked(self, mx, my, mb, event):
        approved_rect = pygame.Rect(self.ApprovedLocation.x, self.ApprovedLocation.y, self.approveBot.get_rect().w,
                                 self.approveBot.get_rect().h)
        if self.endPoint.x == self.currentLocation.x and mb[0] == 1 and event.type == pygame.MOUSEBUTTONUP:
            return approved_rect.collidepoint(mx, my)

    def stamp_approve(self):
        # move approve bot
        if self.stampMovement == "approve-down":
            self.approve_y -= self.stamp_speed
            if self.approve_y <= -20:
                self.approve_y = -20
                self.stampMovement = "approve-up"
                return self.approveStamp

        if self.stampMovement == "approve-up":
            self.approve_y += self.stamp_speed
            if self.approve_y >= 20:
                self.approve_y = 20
                self.stampMovement = "none"
        return None

    def stamp_deny(self):
        # move deny bot
        if self.stampMovement == "deny-down":
            self.deny_y -= self.stamp_speed
            if self.deny_y <= -20:
                self.deny_y = -20
                self.stampMovement = "deny-up"
                return self.deniedStamp

        if self.stampMovement == "deny-up":
            self.deny_y += self.stamp_speed
            if self.deny_y >= 20:
                self.deny_y = 20
                self.stampMovement = "none"
        return None
