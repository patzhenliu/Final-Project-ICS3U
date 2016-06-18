import os


class ClientData:
    def __init__(self):
        # creating variables to load doc data into
        self.Passport = None
        self.DriversLicence = None
        self.Badge = None
        self.Claim = None
        self.Insurance = None
        self.InsuranceCopy = None
        self.Conversation = None
        self.IsGood = None
        self.lines_per_user = 8

    def load_data(self, level_num, user_seq):
        """
        loading data from text files according to client level and order number
        :param level_num:
            the level that client is in
        :param user_seq:
            order in which the client comes in
        """
        fullname = os.path.join('data', "Clients" + str(level_num) + ".txt")
        file = open(fullname, "r")

        lines_to_skip = (user_seq) * self.lines_per_user

        # skipping lines until desired client data is reached
        for i in range(lines_to_skip):
            garbage = file.readline()

        #loading the data for each doc
        self.Claim = ClaimData().load(file.readline())
        self.Insurance = InsuranceData().load(file.readline())
        self.Badge = BadgeData().load(file.readline())
        self.Passport = PassportData().load(file.readline())
        self.DriversLicence = DriversLicenceData().load(file.readline())
        self.Conversation = ConversationData().load(file.readline())
        self.IsGood = IsGoodData().load(file.readline())

        file.close()


class PassportData:
    def __init__(self):
        # creating variables to load passport data into
        self.First = None
        self.Last = None
        self.Sex = "F"
        self.ImageMatch = True
        self.ExpirationDate = None
        self.DocID = None
        self.DateOfBirth = None

    def load(self, input_str):
        """
        loading the data from the line in the text file starting with "PASSP:"
        :param input_str:
            the line in which the data is being taken from
        :return:
            passport object
        """
        input_str = input_str.strip("\n")
        if input_str.startswith("PASSP:"):
            input_str = input_str[6:]
            if input_str == "":
                return None
        else:
            raise ValueError('Cannot load passport. Please check file')

        input_str = input_str.split(',')
        self.First = input_str[0]
        self.Last = input_str[1]
        self.Sex = input_str[2]
        self.ImageMatch = (input_str[3] == "True")
        self.ExpirationDate = input_str[4]
        self.DocID = input_str[5]
        self.DateOfBirth = input_str[6]
        return self


class DriversLicenceData:
    # creating variables to load drivers license data into
    def __init__(self):
        self.First = None
        self.Last = None
        self.Sex = "F"
        self.ImageMatch = True
        self.DateOfBirth = None
        self.ExpirationDate = None

    def load(self, input_str):
        """
            loading the data from the line in the text file starting with "DRIVL:"
            :param input_str:
                the line in which the data is being taken from
            :return:
                drivers license object
        """
        input_str = input_str.strip("\n")
        if input_str.startswith("DRIVL:"):
            input_str = input_str[6:]
            if input_str == "":
                return None
        else:
            raise ValueError('Cannot load driver license. Please check file')

        input_str = input_str.split(',')
        self.First = input_str[0]
        self.Last = input_str[1]
        self.Sex = input_str[2]
        self.ImageMatch = (input_str[3] == "True")
        self.ExpirationDate = input_str[4]
        self.DateOfBirth = input_str[5]
        return self


class BadgeData:
    def __init__(self):
        # creating variables to load id badge data into
        self.First = None
        self.Last = None
        self.ImageMatch = True

    def load(self, input_str):
        """
            loading the data from the line in the text file starting with "BADGE:"
            :param input_str:
                the line in which the data is being taken from
            :return:
                id badge object
        """
        input_str = input_str.strip("\n")
        if input_str.startswith("BADGE:"):
            input_str = input_str[6:]
            if input_str == "":
                return None
        else:
            raise ValueError('Cannot load badge. Please check file')

        input_str = input_str.split(',')
        self.First = input_str[0]
        self.Last = input_str[1]
        self.ImageMatch = (input_str[2] == "True")
        return self


class ClaimData:
    def __init__(self):
        # creating variables to load insurance claim data into
        self.First = None
        self.Last = None
        self.DocID = None
        self.Reason = None

    def load(self, input_str):
        """
            loading the data from the line in the text file starting with "CLAIM:"
            :param input_str:
                the line in which the data is being taken from
            :return:
                insurance claim object
        """
        input_str = input_str.strip("\n")
        if input_str.startswith("CLAIM:"):
            input_str = input_str[6:]
            if input_str == "":
                return None
        else:
            raise ValueError('Cannot load claim. Please check file')

        input_str = input_str.split(',')
        self.First = input_str[0]
        self.Last = input_str[1]
        self.DocID = input_str[2]
        self.Reason = input_str[3]
        return self


class InsuranceData:
    def __init__(self):
        # creating variables to load insurance data into
        self.First = None
        self.Last = None
        self.DocID = None
        self.Type = None
        self.TypeMatchReason = True
        self.ExpirationDate = None

    def load(self, input_str):
        """
            loading the data from the line in the text file starting with "INSUR:"
            :param input_str:
                the line in which the data is being taken from
            :return:
                insurance object
        """
        input_str = input_str.strip("\n")
        if input_str.startswith("INSUR:"):
            input_str = input_str[6:]
            if input_str == "":
                return None
        else:
            raise ValueError('Cannot load insurance. Please check file')

        input_str = input_str.split(',')
        self.First = input_str[0]
        self.Last = input_str[1]
        self.DocID = input_str[2]
        self.Type = input_str[3]
        self.TypeMatchReason = (input_str[4] == "True")
        self.ExpirationDate = input_str[5]
        return self


class ConversationData:
    def __init__(self):
        # creating array to load conversation data into
        # tuple of (who, text) refers to who is talking and what they're saying
        # text is separated by ";" to separate Client and You
        # further text is separated by "&" to separate multi line
        self.ListOfText = []

    def load(self, input_str):
        """
            loading the data from the line in the text file starting with "CONVO:"
            :param input_str:
                the line in which the data is being taken from
            :return:
                conversation object
        """
        input_str = input_str.strip("\n")
        if input_str.startswith("CONVO:"):
            input_str = input_str[6:]
            if input_str == "":
                return None
        else:
            raise ValueError('Cannot load conversation. Please check file')

        who = "You"
        for text in input_str.split(";"):
            self.ListOfText.append((who, text))
            if who == "Client":
                who = "You"
            else:
                who = "Client"
        return self


class IsGoodData:
    def __init__(self):
        # creating variables to check if client has valid documents
        self.IsGood = None
        self.Reason = None

    def load(self, input_str):
        """
            loading the data from the line in the text file starting with "ISGUD:"
            :param input_str:
                the line in which the data is being taken from
            :return:
                object for validating client docs
        """
        input_str = input_str.strip("\n")
        if input_str.startswith("ISGUD:"):
            input_str = input_str[6:]
            if input_str == "":
                return None
        else:
            raise ValueError('Cannot load IsGood. Please check file')

        input_str = input_str.split(',')
        self.IsGood = (input_str[0] == "True")
        self.Reason = input_str[1]
        return self
