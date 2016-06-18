import os
import time


class LevelData():
    def __init__(self, levelnum):
        """
        create object to receive data from the progress.txt file
        :param levelnum:
            which level (file line) to load from the file
        """
        self.LevelNumber = levelnum
        self.LevelCompleted = False
        self.Credits = 0
        self.DatePlayed = ""
        self.familyCold = False
        self.familyHungry = False
        self.gotCitation = False

    def load(self, input_str):
        """
        converts single line from the file into the level data object
        :param input_str:
            a text line from the file
        """
        input_str = input_str.strip("\n")
        input_str = input_str.split(',')

        self.LevelNumber = int(input_str[0]) # from 1 to 4
        self.LevelCompleted = (input_str[1] == "True")
        self.Credits = int(input_str[2])
        self.DatePlayed = input_str[3]
        self.familyCold = (input_str[4] == "True")
        self.familyHungry = (input_str[5] == "True")
        self.gotCitation = (input_str[6] == "True")

    def get_string(self):
        """
        converts this object to string in order to write it back to the file
        :return:
            string line to be written to the file
        """
        list = [self.LevelNumber,
                self.LevelCompleted,
                self.Credits,
                self.DatePlayed,
                self.familyCold,
                self.familyHungry,
                self.gotCitation]

        string = ""
        for i in list:
            string += str(i) + ","

        return string[:-1] + "\n"


class Progress:
    def __init__(self):
        """
        This object contains all the lines of the file inside levels array of LevelData
        """
        self.levels = []

    def save_progress(self):
        """
        saves progress to the file
        :return:
        """
        fullname = os.path.join('data', "Progress.txt")
        file = open(fullname, "w")
        for level in self.levels:
            file.write(level.get_string())
        file.close()

    def load_progress(self):
        """
        loads progress from the file into the levels array of LevelData
        :return:
        """
        fullname = os.path.join('data', "Progress.txt")
        file = open(fullname, "r")
        self.levels = []
        for i in range(4):
            lev = LevelData(None)
            lev.load(file.readline())
            self.levels.append(lev)
        file.close()

    def save_level(self, level_stats):
        """
        save one level into the progress file - by updating levels beyond this one
        :param level_stats:
        :return:
        """
        data = LevelData(None)
        data.LevelNumber = level_stats.LevelNumber
        data.LevelCompleted = level_stats.levelCompleted
        data.Credits = level_stats.totalMuns
        data.DatePlayed = time.strftime("%m/%d/%Y")
        data.familyCold = not level_stats.foodOption
        data.familyHungry = not level_stats.heatOption
        data.gotCitation = level_stats.numberOfCitations > 0

        for i in range(len(self.levels[:])):
            if self.levels[i].LevelNumber == data.LevelNumber:
                self.levels[i] = data
            elif self.levels[i].LevelNumber > data.LevelNumber: # clear levels beyond current one!!
                self.levels[i] = LevelData(self.levels[i].LevelNumber)
        self.save_progress()
