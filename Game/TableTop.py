import Helpers


class TableTop:

    def __init__(self, screen):
        """
        Draws table top working area in the bottom right
        :param screen:
            bliting stuff
        """
        self.screen = screen

        # loads image for the table top and set location
        self.image = Helpers.load_image("images/tabletop.png")
        self.top_left = (300, 150)
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.top_left)  # since we need rect for collision, move where it is drawn

    def draw(self):
        # draws the table on the screen
        self.screen.blit(self.image, self.top_left)
