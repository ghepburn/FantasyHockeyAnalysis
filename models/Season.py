import os

class Season:
    
    def __init__(self, season):
        self.season = season
        self.dataPath = os.getcwd() + "/data/" + season + "/"
        self.resultsPath = os.getcwd() + "/results/" + season + "/"
        self.error = ""
        self.data = {}

    def getData(self, dataType=None):
        if dataType:
            return self.data[dataType]
        else:
            return self.data

    def setData(self, dataType, data):
        self.data[dataType] = data

    def isValid(self):

        # Required params are set
        if not self.season or len(self.season) != 8:
            self.error = "No Season Specified."
            return False

        # Required data is present
        dataTypes = os.listdir(self.dataPath)
        for typeOfData in dataTypes:
            if typeOfData[0] != ".":
                dataFiles = os.listdir(self.dataPath + typeOfData)
                if len(dataFiles) < 1:
                    self.error = "No " + typeOfData + " Data Available." 
                    return False

        return True