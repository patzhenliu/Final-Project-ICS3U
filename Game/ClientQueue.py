import pygame
import Helpers
import random


class ClientQueue:
    def __init__(self, queue_size, screen):
        """
        creating the shadows walking in the top left of level
        :param queue_size:
            how many people are in line
        :param screen:
            blitting things
        """
        self.screen = screen

        # list of all people in line
        self.list_of_clients = []
        self.timeToGoHome = False # when its 5 o clock and they leave

        # y position where is the door of the cubicle.
        # Clients will walk in
        self.queue_start_y_position = 75
        self.clients_space = 10  # how much space between each person in line
        self.queue_end_y_position = self.queue_start_y_position - self.clients_space

        # create line
        for i in range(queue_size):
            clients = Client(self.queue_end_y_position, self.queue_start_y_position)
            self.queue_end_y_position -= self.clients_space
            self.list_of_clients.append(clients )

    def next(self):
        # move everyone up (it will call next client in the office)
        for client in self.list_of_clients:
            client.move_line(self.clients_space)

    def let_client_go(self):
        # release client from the office
        for client in self.list_of_clients:
            if client.state == "in_office":
                client.state = "leaving"

    def process(self):
        # draw all client

        # clients leave if timeToGoHome is True
        if self.timeToGoHome:
            for client in self.list_of_clients:
                client.go_home(self.screen)

        # always printing them on the screen
        for client in self.list_of_clients:
            client.process(self.screen)

    def all_go_home(self):
        # setting variable to trigger people in line to leave
        self.timeToGoHome = True


class Client:
    def __init__(self, client_y_destination, queue_start_y_position):
        """
        Creating each individual person in line
        :param client_y_destination:
            the y position where the people stop walking downwards
        :param queue_start_y_position:
            where the people start walking from (past top corner)
        """
        # loading and setting sprites
        self.image = Helpers.load_image("images/clients/clients.png")
        self.image_sprite_size = 11, 23
        self.number_of_sprites = 9
        self.sprites_walk_down = [0, 1, 2, 3]     # walk up-down sprites
        self.sprites_walk_side = [4, 5, 6, 7, 8]  # walk left-right sprites
        self.current_sprite = 0

        # timing of walking
        self.last_sprite_time = pygame.time.get_ticks()
        self.walk_speed = 0.5    # how fast they walk
        self.move_speed = 100  # how fast their body move while they walk (too fast is just a blur)

        # all positions where are clients in the line
        self.client_y_destination = client_y_destination   # need to walk to it
        self.human_x_position = random.randrange(27, 44) # scatters x pos of people in line
        self.current_position = Helpers.Point(self.human_x_position, -10)  # create them off screen so they can walk in

        # all the path points for client coming and leaving office
        self.end_down_position = Helpers.Point(self.human_x_position, queue_start_y_position)
        self.end_right_position = Helpers.Point(115, queue_start_y_position)
        self.end_right_exit_position = Helpers.Point(80, queue_start_y_position)

        # STATES:
        # "in_queue",  - client is in the queue
        # "coming",    - client is walking toward the office
        # "in_office", - client is in the office (front desk)
        # "leaving",   - client is walking outside of the office
        # "gone"       - client is outside of the game screen
        self.state = "in_queue"

    def move_line(self, spaces):
        # people move down by var spaces
        self.client_y_destination += spaces

    def process(self, screen):
        # processing the people in line and client coming and leaving office
        if self.state == "in_queue":
            if self._walk_down(screen):
                self.state = "coming"
        if self.state == "coming":
            if self._walk_right(screen):
                self.state = "in_office"
        if self.state == "in_office":
            self.print(screen)

        if self.state == "leaving":
            if self._walk_left(screen):
                if self._walk_up(screen):
                    self.state = "gone"

        if self.state == "home":
            self._walk_up(screen)

    def go_home(self, screen):
        # the people in line leaving at 5 o clock
        if self.state != "in_office" and self.state != "leaving" and self.state != "coming":
            self.state = "home"

    def get_image(self, num):
        # loading sprites (num is the order it comes in from the image of sprites)
        if num >= self.number_of_sprites:
            raise ValueError('There are only 0-' + str(self.number_of_sprites-1) + ' sprites. Cannot load ' + str(num))
        rect = pygame.Rect(11 * num, 0, 11, 23)  # x, y w, h
        image = pygame.Surface(rect.size).convert()
        image.blit(self.image, (0, 0), rect)
        image.set_colorkey(image.get_at((0, 0)), pygame.RLEACCEL)
        return image

    def print(self, screen):
        # printing current sprite
        screen.blit(self.get_image(self.current_sprite), (self.current_position.x, self.current_position.y))

    def _change_sprite(self):
        """
        changing sprite image by movement speed
        :return:
            True - if sprite image changes
            False - otherwise
        """
        if pygame.time.get_ticks() - self.move_speed >= self.last_sprite_time:
            self.current_sprite += 1
            self.last_sprite_time = pygame.time.get_ticks()
            return True
        return False

    # different ways of moving client ***************************

    def _walk_down(self, screen):
        if self.current_position.y < self.client_y_destination:
            self.current_position.move_down(self.walk_speed)
            self._change_sprite_down()

        self.print(screen)
        return self.current_position.y >= self.end_down_position.y

    def _walk_right(self, screen):
        if self.current_position.x < self.end_right_position.x:
            self.current_position.move_right(self.walk_speed)
            self._change_sprite_side()

        self.print(screen)
        return self.current_position.x >= self.end_right_position.x

    def _walk_left(self, screen):
        if self.current_position.x > self.end_right_exit_position.x:
            self.current_position.move_left(self.walk_speed)
            self._change_sprite_side()

        self.print(screen)
        return self.current_position.x <= self.end_right_exit_position.x

    def _walk_up(self, screen):
        if self.current_position.y > -10:
            self.current_position.move_up(self.walk_speed)
            self._change_sprite_down()

        self.print(screen)
        return self.current_position.y <= -10

    def _change_sprite_down(self):
        if self._change_sprite():
            self._make_down_sprite()

    def _change_sprite_side(self):
        if self._change_sprite():
            self._make_side_sprite()

    def _make_down_sprite(self):
        if not self.current_sprite in self.sprites_walk_down:
            self.current_sprite = self.sprites_walk_down[0]

    def _make_side_sprite(self):
        if not self.current_sprite in self.sprites_walk_side:
            self.current_sprite = self.sprites_walk_side[0]
