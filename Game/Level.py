import pygame
import Background
import Desk
import TableTop
import Client
import ClientQueue
import Stamp
import Document
import Clock
import LevelSummary


class Level:
    """
    Create Level, and run it
    """

    def __init__(self, screen):
        """
        Creates level
        :param screen:
            this is where we draw
        """
        self.screen = screen
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        # conversation variables
        self.conversation = []  # hold conversation info
        self.conversation_timeout = 1000  # 2 secs between each conversation line
        self.last_talk_time = pygame.time.get_ticks()
        self.conversation_font = pygame.font.SysFont("Arial", 12, True)

        self.client = None  # holds current client
        self.clientCount = 0  # count current client number
        self.clientPerLevel = 10
        self.currentLevel = None # current level: 1, 2, 3, 4

        # all objects:
        self.desk = Desk.Desk(self.screen)
        self.tabletop = TableTop.TableTop(self.screen)
        self.background = Background.Background(self.screen)
        self.stamp = Stamp.Stamp(self.screen)
        self.clock = Clock.Clock(self.screen, (700,26))
        self.clock_speed = 10  # 30 min is this many seconds

        self.client_queue = ClientQueue.ClientQueue(50, self.screen)
        self.walk_speed = 1  # pix per frame

        self.citations = []  # documents that are always here
        self.documents = []  # documents that are given back by client

        self.dragging = None

        self.dropping = [] # hold docs that are in air so they can drop
        self.document_drop_speed = 10  # pix per frame

        self.pastFive = False  # is it past five
        self.exit = False  # can we exit

        self.intercom_audio = pygame.mixer.Sound("music/speech-announce.wav")
        self.intercom_audio.set_volume(0.7)

        self.set_level_summary = False  # is summary set yet
        self.level_summary = None

        # add rule book:
        self.ruleDoc = Document.Rulebook()
        self.citations.append(self.ruleDoc)
        self.rulebook_added = 0

        self.clearLevel = False  # is it safe to discard this level

    def clear_level(self):
        """
        flag it is safe to discard this level
        :return:
        """
        self.clearLevel = True

    def run(self, level_number, mx, my, mb, event):
        """
        runs the level
        :param level_number:
            level we are running 1, 2, 3, 4
        :param mx:
            pass x mouse coordinate
        :param my:
            pass y mouse coordinate
        :param mb:
            pass mouse button status
        :param event:
            pass event (for mousebutton events)
        :return:
            return Summary object when level is over
            Level is over when user walk out of screen.
        """
        # if self.clientCount > self.clientPerLevel:
        #     self.level_summary.LevelOver = True
        #     return self.level_summary

        self.currentLevel = level_number

        if not self.set_level_summary:
            self.level_summary = LevelSummary.LevelSummary(self.screen, self.currentLevel + 1)
            self.set_level_summary = True

        # draw background:
        self.level_summary.LevelNumber = self.currentLevel
        self.background.draw()
        self.tabletop.draw()
        self.desk.draw_background()
        self.pastFive = self.clock.draw(40 * self.clock_speed)  # draw clock and also return True is time has ran out

        # highlight intercom
        self.background.highlight_intercom(mx, my)

        # fill rulebook info
        if level_number >= 1 and self.rulebook_added == 0:
            self.ruleDoc.set_rules_text(["  Client must have:",
                                         "   ° Insurance Claim",
                                         "   ° Valid Insurance"])
            self.rulebook_added += 1
        if level_number >= 2 and self.rulebook_added == 1:
            self.ruleDoc.add_rules_text(["   ° ID badge"])
            self.rulebook_added += 1
        if level_number >= 4 and self.rulebook_added == 2:
            self.ruleDoc.add_rules_text(["   ° either:",
                                         "      Driver's License",
                                         "      or Passport"])
            self.rulebook_added += 1

        # drag document:
        if self.dragging or not self.stamp.is_mouse_over_stamp_area(mx, my):
            self._manage_dragging_documents(mx, my, mb)

        # draw client:
        # returns True if level is over
        if self.process_customer(mx, my, mb):
            self.level_summary.level_over()
            self.level_summary.set_client(self.clientCount)
            self.level_summary.level_over()
            return self.level_summary

        # draw desk with clock so the customer isn't blocking it :)
        self.desk.draw(level_number)

        # draw all documents
        for doc in self.documents:
            if doc.onTable:
                doc.draw(self.screen, self.tabletop.rect)

        # draw client queue:
        if self.pastFive:
            self.client_queue.all_go_home()

        self.client_queue.process()

        # draw stamper:
        stamp_doc = self.stamp.process(mx, my, mb, event)

        # if document is stamp-able - mark it on doc
        if stamp_doc is not None:
            for doc in self.documents:
                if doc.canStamp and stamp_doc.rect.colliderect(doc.rect):
                    #stamp it now on doc!
                    doc.stamp_it(stamp_doc)

        self.level_summary.set_client(self.clientCount)
        return self.level_summary

    def process_customer(self, mx, my, mb):
        """
        process clients (walk-in, create, walk-out, documents, citations etc)
        :param mx:
            pass x mouse coordinate
        :param my:
            pass y mouse coordinate
        :param mb:
            pass mouse button status
        :return:
            return True when client is done or level is over
        """

        if self.client is None and \
                pygame.MOUSEBUTTONUP and mb[0] == 1 and \
                self.background.get_intercom_area().collidepoint(mx, my):
            self.intercom_audio.play()
            self.client = Client.Client(self.currentLevel, self.clientCount)
            self.client_queue.next()
            self.clock.start()
            self.clientCount += 1

        if self.client is None and self.clientCount == self.clientPerLevel:
            return True

        if self.client is not None:
            if self.client.process(self.screen, self.walk_speed):

                if self.client.Data.IsGood.IsGood != self.client.is_client_approved():
                    # ceate new citation!!!
                    self.citations.append(Document.Citation(self.client.Data.IsGood.Reason))
                    self.level_summary.add_citation()
                self.client = None
                self.conversation = []
                if self.pastFive:
                    return True
            else:

                # only once:
                if not self.client.gaveDocs:
                    self.documents = self.client.get_documents(self.desk.get_desk_ticket_position)
                    temp = self.citations
                    temp.extend(self.documents)

                    self.documents = temp
                self._show_text()
        else:
            # WHEN CLIENT IS GONE ONLY CITATIONS ARE LEFT:
            self.documents = self.citations
            if self.pastFive:
                return True

    def _manage_dragging_documents(self, mx, my, mb):
        if mb[0] == 1:
            if self.dragging is None:
                # check all draggable docs, find one we are dragging:
                for doc in self.documents:
                    if doc.is_on_document(mx, my):
                        self.dragging = doc
        else:
            # nothing is dragging now:
            if self.dragging is not None:
                self.dropping.append(self.dragging)
                self.dragging = None

        if self.dragging:
            # make sure dragging image is last to be drawn (on top of them all)
            self._reorder_list(self.documents, self.dragging)
            # switch between big and small images:
            if self.desk.rect.right <= self.dragging.rect.center[0]:
                self.dragging.set_inner()
            else:
                self.dragging.set_outer()

            # prevent from getting out of area:
            self._keep_docs_inside_area(self.dragging, mx, my)

        for drop in self.dropping[:]:  # iterate copy so we can delete from original
            # drop until inside table
            if drop.rect.center[1] == self.desk.get_desk_ticket_position[1] or self.tabletop.rect.collidepoint(
                    drop.rect.center):
                self.dropping.remove(drop)
            else:
                # drop to Client if documents are ready
                if self.client is not None and self.client.are_docs_ready():
                    if drop.docType != "Citation" and drop.docType != "Rulebook":
                        self.client.take_doc(drop)
                        self.dropping.remove(drop)
                        self.documents.remove(drop)

                    if self.client.has_all_docs():
                        self.client.set_done()  # client can leave office now
                        self.client_queue.let_client_go()

                if drop.rect.center[1] <= self.desk.get_desk_ticket_position[1]:
                    drop.move_to(drop.rect.center[0], drop.rect.center[1] + self.document_drop_speed)
                    if drop.rect.center[1] >= self.desk.get_desk_ticket_position[1]:
                        drop.move_to(drop.rect.center[0], self.desk.get_desk_ticket_position[1])

    def _keep_docs_inside_area(self, drag, x, y):
        # extend Desk so that we can move document past the border
        extend_pixels = 100
        extended_tabletop = self.tabletop.rect.copy()
        extended_tabletop.inflate_ip(extend_pixels, extend_pixels)
        extended_tabletop.move_ip(extend_pixels, 0)

        area = pygame.Rect.union(self.desk.rect, self.tabletop)
        new_rect_position = drag.rect.copy()
        new_rect_position.center = (x, y)
        if extended_tabletop.contains(new_rect_position) or self.desk.rect.contains(new_rect_position):
            # make sure doesnt pass the mid desk line
            if self.desk.rect.contains(new_rect_position) and new_rect_position.center[1] >= \
                    self.desk.get_desk_ticket_position[1]:
                x = new_rect_position.center[0]
                y = self.desk.get_desk_ticket_position[1]
            drag.move_to(x, y)
        else:
            if new_rect_position.left < self.desk.rect.left:
                new_rect_position.left = self.desk.rect.left

            if new_rect_position.right > extended_tabletop.right:
                new_rect_position.right = extended_tabletop.right

            if new_rect_position.center[0] >= extended_tabletop.left:  # table top restriction
                if new_rect_position.bottom > extended_tabletop.bottom:
                    new_rect_position.bottom = extended_tabletop.bottom
            else:  # desk restriction
                if new_rect_position.bottom > self.desk.rect.bottom:
                    new_rect_position.bottom = self.desk.rect.bottom

            if new_rect_position.center[0] >= extended_tabletop.left:  # table top restriction
                if new_rect_position.top < extended_tabletop.top:
                    new_rect_position.top = extended_tabletop.top
            else:  # desk restriction
                if new_rect_position.top < self.desk.rect.top:
                    new_rect_position.top = self.desk.rect.top

            if self.desk.rect.collidepoint(new_rect_position.center) and new_rect_position.center[1] >= \
                    self.desk.get_desk_ticket_position[1]:
                new_rect_position.center = new_rect_position.center[0], self.desk.get_desk_ticket_position[1]
            drag.move_to(new_rect_position.center[0], new_rect_position.center[1])

    def _reorder_list(self, list_to_sort, item_to_append_last):
        # documents most recently touched go on the top
        list_to_sort.remove(item_to_append_last)
        list_to_sort.append(item_to_append_last)

    # printing conversation ***************************************

    def _show_text(self):
        self._print_conversation()
        if pygame.time.get_ticks() - self.last_talk_time > self.conversation_timeout:
            who_str = self.client.get_dialog()
            if who_str is not None:
                self.conversation.append(who_str)
                self.last_talk_time = pygame.time.get_ticks()

    def _print_conversation(self):
        conversation_position = 0
        for c in self.conversation:
            if c[0] == "You":
                conversation_position = self._print_person_convo(c[1], conversation_position, True)
            else:
                conversation_position = self._print_person_convo(c[1], conversation_position, False)

    def _print_one_convo_line(self, text, pos, right):
        conversation_line = self.conversation_font.render(" " + text + " ", 1, self.black, (237, 224, 216))
        conversation_size = conversation_line.get_width() + 10
        if right:
            new_position_x = self.desk.rect.x + 10
        else:
            new_position_x = self.desk.rect.x + self.desk.rect.width - conversation_size

        new_position = (new_position_x, self.desk.rect.y + 20 + pos)
        self.screen.blit(conversation_line, new_position)

    def _print_person_convo(self, text, pos, right):
        if len(text.split("&")) > 1:
            for sub in text.split("&"):
                self._print_one_convo_line(sub, pos, right)
                pos += 14
            return pos + 6
        else:
            self._print_one_convo_line(text, pos, right)
            return pos + 20
