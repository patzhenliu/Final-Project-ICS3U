import pygame
import Helpers


class SubDocument:

    def __init__(self, image_name, transparent):
        """
        load object storing inner or outer for a document
        :param image_name:
            path of image
        :param transparent:
            add transparency or not
        """
        self.image = Helpers.load_image(image_name, transparent)
        self.rect = self.image.get_rect()


class Document:

    def __init__(self, document_name, pos):
        """
        create a base class for all documents
        :param document_name:
            name of document
        :param pos:
            current location of document
        """
        if pos is None: # if there's no position pos is set to top left
            pos = (0, 0)

        # setting variables for all documents
        self.onTable = True
        self.docType = document_name
        self.inner = SubDocument("images/documents/" + str(document_name) + "Inner.png", None)
        self.outer = SubDocument("images/documents/" + str(document_name) + "Outer.png", None)
        self.image = self.outer.image
        self.rect = self.outer.rect
        self.rect.center = pos
        self.canStamp = False
        self.deskRect = pygame.Rect(20, 150, 280, 330)
        self.screenshot_image = None
        self.brown = (128, 64, 0)

    def move_to(self, x, y):
        # move to new x, y pos
        self.rect.center = (x, y)

    def is_on_document(self, mx, my):
        # if mouse if in contact with document
        return self.rect.collidepoint((mx, my)) == 1

    def set_inner(self):
        # uses the smaller version of document on left side of desk
        self.image = self.inner.image
        self.inner.rect.center = self.rect.center
        self.rect = self.inner.rect

    def set_outer(self):
        # uses the larger version of document on right side of desk
        self.image = self.outer.image
        self.outer.rect.center = self.rect.center
        self.rect = self.outer.rect


class DriversLicense(Document):
    def __init__(self, pos, data, photo_image):
        """
        getting data for this doc
        :param pos:
            current location of this doc
        :param data:
            data loaded from text files for this doc
        :param photo_image:
            client photo
        """
        super().__init__("DriversLicense", pos)
        self.onTable = False
        self.data = data
        self.font = pygame.font.SysFont("Arial", 12, True)
        self.last = self.font.render(self.data.Last + ",", 1, (0, 0, 0))
        self.first = self.font.render(self.data.First, 1, (0, 0, 0))
        self.sex = self.font.render(self.data.Sex, 1, (0, 0, 0))
        self.dob = self.font.render(self.data.DateOfBirth, 1, (0, 0, 0))
        self.exp = self.font.render(self.data.ExpirationDate, 1, (0, 0, 0))
        self.photoImage = photo_image

    def draw(self, screen, clip):
        """
        draws the doc
        :param screen:
            blitting stuff
        """
        if self.rect.center != (0, 0):
            if self.image == self.inner.image:
                if self.screenshot_image is None:
                    # create screenshot
                    self.rect.midbottom = (300, 480)  # if doc is outside of screen subsurface line will error
                    pygame.draw.rect(screen, self.brown, self.rect)
                    screen.blit(self.image, self.rect)
                    screen.blit(self.last, (self.rect.x + 80, self.rect.y + 30))
                    screen.blit(self.first, (self.rect.x + 80, self.rect.y + 42))
                    screen.blit(self.dob, (self.rect.x + 110, self.rect.y + 62))
                    screen.blit(self.sex, (self.rect.x + 110, self.rect.y + 80))
                    screen.blit(self.exp, (self.rect.x + 110, self.rect.y + 97))
                    screen.set_clip(pygame.Rect(self.rect.x + 10, self.rect.y + 30, 60, 80))
                    screen.blit(self.photoImage, (self.rect.x - 10, self.rect.y + 25))
                    screen.set_clip(None)
                    self.screenshot_image = screen.subsurface(self.rect).copy()
                    color_key = self.screenshot_image.get_at((0, 0))
                    self.screenshot_image.set_colorkey(color_key, pygame.RLEACCEL)

                else:
                    #blit screenshot
                    screen.set_clip(clip)
                    screen.blit(self.screenshot_image, (self.rect.x, self.rect.y))
                    screen.set_clip(None)
            else:
                screen.set_clip(self.deskRect)
                screen.blit(self.image, self.rect)
                screen.set_clip(None)


class Passport(Document):
    def __init__(self, pos, data, photo_image):
        """
        getting data for this doc
        :param pos:
            current location of this doc
        :param data:
            data loaded from text files for this doc
        :param photo_image:
            client photo
        """
        super().__init__("Passport", pos)
        self.onTable = False
        self.data = data
        self.font = pygame.font.SysFont("Arial", 12, True)
        self.lastFirst = self.font.render(self.data.Last + ", " + self.data.First, 1, (0, 0, 0))
        self.sex = self.font.render(self.data.Sex, 1, (0, 0, 0))
        self.exp = self.font.render(self.data.ExpirationDate, 1, (0, 0, 0))
        self.id = self.font.render(self.data.DocID, 1, (0, 0, 0))
        self.dob = self.font.render(self.data.DateOfBirth, 1, (0, 0, 0))
        self.photoImage = photo_image

    def draw(self, screen, clip):
        """
        draws the doc
        :param screen:
            blitting stuff
        """
        if self.rect.center != (0, 0):
            if self.image == self.inner.image:
                if self.screenshot_image is None:
                    # create screenshot
                    self.rect.midbottom = (300, 480)  # if doc is outside of screen subsurface line will error
                    screen.blit(self.image, self.rect)
                    screen.blit(self.lastFirst, (self.rect.x + 80, self.rect.y + 139))
                    screen.blit(self.dob, (self.rect.x + 110, self.rect.y + 163))
                    screen.blit(self.sex, (self.rect.x + 110, self.rect.y + 179))
                    screen.blit(self.id, (self.rect.x + 110, self.rect.y + 197))
                    screen.blit(self.exp, (self.rect.x + 110, self.rect.y + 214))
                    screen.set_clip(pygame.Rect(self.rect.x + 15, self.rect.y + 160, 60, 80))
                    screen.blit(self.photoImage, (self.rect.x - 5, self.rect.y + 150))
                    screen.set_clip(None)
                    self.screenshot_image = screen.subsurface(self.rect).copy()
                else:
                    # blit screenshot
                    screen.set_clip(clip)
                    screen.blit(self.screenshot_image, (self.rect.x, self.rect.y))
                    screen.set_clip(None)
            else:
                screen.set_clip(self.deskRect)
                screen.blit(self.image, self.rect)
                screen.set_clip(None)


class Badge(Document):
    def __init__(self, pos, data, photo_image):
        """
        getting data for this doc
        :param pos:
            current location of this doc
        :param data:
            data loaded from text files for this doc
        :param photo_image:
            client photo
        """
        super().__init__("Badge", pos)
        self.onTable = False
        self.data = data
        self.font = pygame.font.SysFont("Arial", 12, True)
        self.firstLast = self.font.render(self.data.First + " " + self.data.Last, 1, (0, 0, 0))
        self.photoImage = photo_image

    def draw(self, screen, clip):
        """
        draws the doc
        :param screen:
            blitting stuff
        """
        if self.rect.center != (0, 0):
            if self.image == self.inner.image:
                if self.screenshot_image is None:
                    # create screenshot
                    self.rect.midbottom = (300, 480)  # if doc is outside of screen subsurface line will error
                    pygame.draw.rect(screen, self.brown, self.rect)
                    screen.blit(self.image, self.rect)
                    screen.blit(self.firstLast, (self.rect.x + 20, self.rect.y + 146))
                    screen.blit(self.photoImage, (self.rect.x + 20, self.rect.y + 60))
                    self.screenshot_image = screen.subsurface(self.rect).copy()
                    color_key = self.screenshot_image.get_at((0, 0))
                    self.screenshot_image.set_colorkey(color_key, pygame.RLEACCEL)
                else:
                    # blit screenshot
                    screen.set_clip(clip)
                    screen.blit(self.screenshot_image, (self.rect.x, self.rect.y))
                    screen.set_clip(None)

            else:
                screen.set_clip(self.deskRect)
                screen.blit(self.image, self.rect)
                screen.set_clip(None)


class InsuranceClaim(Document):
    def __init__(self, pos, data, photo_image):
        """
        getting data for this doc
        :param pos:
            current location of this doc
        :param data:
            data loaded from text files for this doc
        :param photo_image:
            client photo
        """
        super().__init__("InsuranceClaim", pos)
        self.onTable = False
        self.data = data
        self.font = pygame.font.SysFont("Arial", 15, True)
        self.lastFirst = self.font.render(self.data.Last + ", " + self.data.First, 1, (0, 0, 0))
        self.reason = self.font.render(self.data.Reason, 1, (0, 0, 0))
        self.id = self.font.render(self.data.DocID, 1, (0, 0, 0))
        self.photoImage = photo_image
        self.canStamp = True

        self.isApproved = None
        self.stampDoc = None
        self.stampRelativeLocation = Helpers.Point(15, 15)

    def stamp_it(self, stamp_doc):
        self.stampDoc = stamp_doc
        self.isApproved = self.stampDoc.approved
        self.stampRelativeLocation.x = stamp_doc.rect.x - self.rect.x
        self.stampRelativeLocation.y = stamp_doc.rect.y - self.rect.y

    # clip so doc doesnt show beyond table top
    def draw(self, screen, clip):
        """
        draws the doc
        :param screen:
            blitting stuff
        """
        if self.rect.center != (0, 0):
            if self.image == self.inner.image:
                if self.screenshot_image is None:
                    # create screenshot
                    self.rect.midbottom = (300, 480)  # if doc is outside of screen subsurface line will error
                    pygame.draw.rect(screen, self.brown, self.rect)
                    screen.blit(self.image, self.rect)
                    screen.blit(self.lastFirst, (self.rect.x + 35, self.rect.y + 182))
                    screen.blit(self.reason, (self.rect.x + 35, self.rect.y + 219))
                    screen.blit(self.id, (self.rect.x + 35, self.rect.y + 255))
                    self.screenshot_image = screen.subsurface(self.rect).copy()
                    color_key = self.screenshot_image.get_at((0, 0))
                    self.screenshot_image.set_colorkey(color_key, pygame.RLEACCEL)
                else:
                    # blit screenshot
                    screen.set_clip(clip)
                    screen.blit(self.screenshot_image, (self.rect.x, self.rect.y))
                    screen.set_clip(None)

                if self.stampDoc is not None:
                    screen.set_clip(clip.clip(self.rect))
                    screen.blit(self.stampDoc.image, (self.rect.x + self.stampRelativeLocation.x, self.rect.y + self.stampRelativeLocation.y))
                    screen.set_clip(None)

            else:
                screen.set_clip(self.deskRect)
                screen.blit(self.image, self.rect)
                screen.set_clip(None)


class Insurance(Document):
    def __init__(self, pos, data, photo_image):
        """
        getting data for this doc
        :param pos:
            current location of this doc
        :param data:
            data loaded from text files for this doc
        :param photo_image:
            client photo
        """
        super().__init__("Insurance", pos)
        self.onTable = False
        self.data = data
        self.font = pygame.font.SysFont("Arial", 14, True)
        self.lastFirst = self.font.render(self.data.Last + ", " + self.data.First, 1, (0, 0, 0))
        self.id = self.font.render(self.data.DocID, 1, (0, 0, 0))
        self.type = self.font.render(self.data.Type, 1, (0, 0, 0))
        self.exp = self.font.render(self.data.ExpirationDate, 1, (0, 0, 0))
        self.photoImage = photo_image

    def draw(self, screen, clip):
        """
        draws the doc
        :param screen:
            blitting stuff
        """
        if self.rect.center != (0, 0):
            if self.image == self.inner.image:
                if self.screenshot_image is None:
                    # create screenshot
                    self.rect.midbottom = (300, 480)  # if doc is outside of screen subsurface line will error
                    pygame.draw.rect(screen, self.brown, self.rect)
                    screen.blit(self.image, self.rect)
                    screen.blit(self.lastFirst, (self.rect.x + 30, self.rect.y + 82))
                    screen.blit(self.id, (self.rect.x + 30, self.rect.y + 133))
                    screen.blit(self.type, (self.rect.x + 110, self.rect.y + 158))
                    screen.blit(self.exp, (self.rect.x + 110, self.rect.y + 185))
                    self.screenshot_image = screen.subsurface(self.rect).copy()
                    color_key = self.screenshot_image.get_at((0, 0))
                    self.screenshot_image.set_colorkey(color_key, pygame.RLEACCEL)
                else:
                    screen.set_clip(clip)
                    screen.blit(self.screenshot_image, self.rect)
                    screen.set_clip(None)
            else:
                screen.set_clip(self.deskRect)
                screen.blit(self.image, self.rect)
                screen.set_clip(None)


class Citation(Document):
    def __init__(self, reason):
        """
        getting data for this doc
        :param reason:
            reason why you got citation
        """
        super().__init__("Citation", (0,0))
        self.font = pygame.font.SysFont("Arial", 12, True)
        self.reason = self.font.render(reason, 1, (0, 0, 0))
        self.rect.center = (530, 510)
        self.endPos = (530, 400)
        self.doSlide = True
        self.set_inner()
        self.onTable = True

    def draw(self, screen, clip):
        """
        draws the doc
        :param screen:
            blitting stuff
        """
        if self.rect.center != (0, 0):
            if self.doSlide == True:
                self.slide()
            if self.image == self.inner.image:
                if not self.doSlide and self.screenshot_image is None:
                    # create screenshot
                    self.rect.center = (530, 400)  # if doc is outside of screen subsurface line will error
                    pygame.draw.rect(screen, self.brown, self.rect)
                    screen.blit(self.image, self.rect)
                    screen.blit(self.reason, (self.rect.x + 15, self.rect.y + 45))
                    self.screenshot_image = screen.subsurface(self.rect).copy()
                    color_key = self.screenshot_image.get_at((0, 0))
                    self.screenshot_image.set_colorkey(color_key, pygame.RLEACCEL)
                elif self.screenshot_image is None:
                    screen.blit(self.image, self.rect)
                    screen.blit(self.reason, (self.rect.x + 15, self.rect.y + 48))
                else:
                    screen.set_clip(clip)
                    screen.blit(self.screenshot_image, self.rect)
                    screen.set_clip(None)

            else:
                screen.set_clip(self.deskRect)
                screen.blit(self.image, self.rect)
                screen.set_clip(None)

    def slide(self):
        # slide up from bottom of screen
        if self.rect.center[1] >= self.endPos[1]:
            self.rect.center = (530, self.rect.center[1] - 8)
        else:
            self.rect.center = self.endPos
            self.doSlide=False

class Rulebook(Document):
    def __init__(self):
        """
        getting data for this doc
        """
        super().__init__("Rulebook", (0,0))
        self.font = pygame.font.SysFont("Arial", 12, True)
        self.rules = []
        self.rect.center = (255, 380)
        self.set_outer()
        self.onTable = True
        self.outer = SubDocument("images/documents/RulebookOuter.png", -1)

    def draw(self, screen, clip):
        """
        draws the doc
        :param screen:
            blitting stuff
        """
        if self.rect.center != (0, 0):
            if self.image == self.inner.image:
                if self.screenshot_image is None:
                    # create screenshot
                    self.rect.midbottom = (300, 480)  # if doc is outside of screen subsurface line will error
                    pygame.draw.rect(screen, self.brown, self.rect)
                    screen.blit(self.image, self.rect)
                    spacing = 20
                    for r in self.rules:
                        screen.blit(r, (self.rect.x + 15, self.rect.y + spacing))
                        spacing += 15
                    self.screenshot_image = screen.subsurface(self.rect).copy()
                    color_key = self.screenshot_image.get_at((0, 0))
                    self.screenshot_image.set_colorkey(color_key, pygame.RLEACCEL)
                else:
                    screen.set_clip(clip)
                    screen.blit(self.screenshot_image, self.rect)
                    screen.set_clip(None)

            else:
                screen.set_clip(self.deskRect)
                screen.blit(self.image, self.rect)
                screen.set_clip(None)

    # adding and setting rules to the rule book *******

    def set_rules_text(self, rules):
        for txt in rules:
            self.rules.append(self.font.render(txt, 1, (0, 0, 0)))

    def add_rules_text(self, rules):
        for txt in rules:
            self.rules.append(self.font.render(txt, 1, (0, 0, 0)))
