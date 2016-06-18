import pygame
import Document
import Helpers
import ClientData


class Client:

    def __init__(self, level, num):
        """
        Getting info for client (level and order in the level)
        :param level:
            level number
        :param num:
            client order number within the level
        """
        # loading images
        client_num = str(num + 1 + (level - 1) * 10)
        self.image = Helpers.load_image("images/clients/client" + client_num + ".png", -1)
        self.shadowImage = Helpers.load_image("images/clients/client" + client_num + "Shadow.png", -1)
        self.photoImage = Helpers.load_image("images/clients/client" + client_num + "Photo.png", -1)

        # load info for this client from file
        self.Data = ClientData.ClientData()
        self.Data.load_data(level, num)

        # creating a list to store client's documents, loading documents and flag if client dropped docs on table
        self.Documents = []
        self.process_data()
        self.gaveDocs = False

        # loading conversation into array and tracking who's talking (you - even, client - odd)
        self.Conversation = self.Data.Conversation.ListOfText
        self.NextConversation = 0

        # client in office area (bottom left of level);
        # shadow walking in or out, pos and done (when they're allowed to leave)
        self.status = "walkIn" # walkIn, stay, walkOut
        self.position = (-120, 230)
        self.done = False

    def process(self, screen, speed):
        """
        client (bottom left of level) status; whether they are walking or staying still
        :param screen:
            for blitting things
        :param speed:
            speed of how fast shadow moves
        :return:
            True - client has left the screen
            False - otherwise
        """
        if self.status == "walkIn":
            screen.blit(self.shadowImage, self.position)
            self.position = (self.position[0] + speed, self.position[1])
            if self.position[0] >= 90:
                self.status = "stay"

        elif self.status == "stay":
            screen.blit(self.image, self.position)

            if self.done:
                self.status = "walkOut"

        elif self.status == "walkOut":
            screen.blit(self.shadowImage, self.position)
            self.position = (self.position[0] - speed, self.position[1])
            if self.position[0] <= 0:
                self.status = ""
                return True

        return False

    def get_dialog(self):
        """
        returns next piece of the conversation
        :return:
            next conversation line
            otherwise none is there's nothing left to say
        """
        if self.status == "stay": # only when customer is still
            if self.NextConversation < len(self.Conversation):
                to_say = self.Conversation[self.NextConversation]
                self.NextConversation += 1
                return to_say
        return None

    def process_data(self):
        """
        loads all document with data to the document array
        """

        # Drivers License
        if self.Data.DriversLicence is not None:
            doc = Document.DriversLicense(None, self.Data.DriversLicence, self.photoImage)
            self.Documents.append(doc)
        # PASSPORT
        if self.Data.Passport is not None:
            doc = Document.Passport(None, self.Data.Passport, self.photoImage)
            self.Documents.append(doc)
        # Badge
        if self.Data.Badge is not None:
            doc = Document.Badge(None, self.Data.Badge, self.photoImage)
            self.Documents.append(doc)
        # INSURANCE
        if self.Data.Insurance is not None:
            doc = Document.Insurance(None, self.Data.Insurance, self.photoImage)
            self.Documents.append(doc)
        # CLAIM
        if self.Data.Claim is not None:
            doc = Document.InsuranceClaim(None, self.Data.Claim, self.photoImage)
            self.Documents.append(doc)
        # CONVERSATION
        if self.Data.Conversation is not None:
            self.Conversation = self.Data.Conversation.ListOfText


    def get_documents(self, pos):
        """
        this will give out all docs and setting flag for checking if docs are already on table
        :param pos:
            where to drop docs on the table
        :return:
            returns updated document array
        """
        if self.status == "stay":
            self.gaveDocs = True
            for doc in self.Documents:
                if not doc.onTable:
                    doc.move_to(pos[0], pos[1])
                    doc.onTable = True
        return self.Documents

    def set_done(self):
        """
        set variable to release client out of office (bottom left)
        """
        self.done = True

    def are_docs_ready(self):
        """
        checks if docs can be given to client (if insurance claim is stamped)
        :return:
            True - claim is stamped and docs are ready to be given back
            False - otherwise
        """
        for i in self.Documents:
            if i.canStamp and i.isApproved is None:
                return False
        return True

    def take_doc(self, doc):
        """
        set False for docs that are already given back to client
        :param doc:
            the doc that has been given back to client
        """
        doc.onTable = False

    def has_all_docs(self):
        """
        checks if client has all their docs back
        :return:
        """
        for i in self.Documents:
            if i.onTable and i.docType != "Citation":
                return False
        return True

    def stamp_doc(self, doc):
        """
        applying stamp to doc (insurance claim only)
        :param doc:
            the doc with the stamp
        """
        for my_doc in self.Documents:
            if my_doc.docType == doc.docType:
                my_doc.stamp_it(doc.stampDoc)

    def is_client_approved(self):
        """
        checks if the client was denied or approved
        :return:
            True - approved
            False - denied
        """
        for my_doc in self.Documents:
            if my_doc.docType == "InsuranceClaim":
                return my_doc.isApproved
