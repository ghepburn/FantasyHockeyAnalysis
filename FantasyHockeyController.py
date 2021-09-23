import os
import pandas as pd
import datetime as dt

from transformers.BasicDataFrameTransformer import BasicDataFrameTransformer
from models.DfModel import DfModel
from maps.QuantHockeyMap import QuantHockeyMap
from models.Season import Season
from models.Map import Map

class FantasyHockeyController:
    season = str(dt.datetime.now().year - 1) + str(dt.datetime.now().year)
    dataTypes = ["players", "goalies"]
    dataSource = "QuantHockey"
    sheetName = "QuantHockey"
    numOfSeasons = 3
    transformer = BasicDataFrameTransformer
    dataModel = DfModel

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.key = key
            self.value = kwargs[key]

        self.map = Map(self.getMap(self.dataSource))
        self.seasons = self.getSeasons()

    def getSeasons(self):
        seasons = []
        if self.season:
            targetSeason = self.season
            yearsOfCoverage = self.numOfSeasons

            firstTargetYear = targetSeason[:4]
            secondTargetYear = targetSeason[4:]

            for i in reversed(range(yearsOfCoverage)):
                firstYear = int(firstTargetYear) - i
                secondYear = int(secondTargetYear) - i
                coveredSeason = str(firstYear) + str(secondYear)
                season = Season(coveredSeason)
                seasons.append(season)
        return seasons


    def getData(self, dataType, season):
        folderPath = season.dataPath + dataType
        dataList = []
        rawDataFiles = os.listdir(folderPath)

        for fileName in rawDataFiles:
            filePath = folderPath + "/" + fileName
            data = self.dataModel(filePath, self.sheetName, self.map.getHeaderRow(dataType), self.map.getIndexColumn(dataType))

            dataList.append(data)

        return dataList

    def consolidateData(self, dataModelList):

        consolidatedData = self.dataModel()

        for dataModel in dataModelList:
            consolidatedData.append(dataModel)

        return consolidatedData

    def cleanData(self, dataModel, dataType):

        # Remove Goalies from players data
        if dataType == "players":
            dataModel.removeRows("Pos=G")

        return dataModel

    def transformToCsv(self, dataModel):
        return dataModel.transformToCsv()

    def saveCsv(self, csvFile, name, season):
        path = season.resultsPath
        if not os.path.isdir(path):
            os.mkdir(path)
        fileName = name + self.season + ".csv"
        f = open(path + fileName, "w")
        f.write(csvFile)
        f.close()

    def transformData(self, data, dataType):
        transformer = self.transformer(dataType, self.map)
        transformedData = transformer.transform(data)
        return transformedData

    def buildCsv(self):
        for i in range(len(self.seasons)):
            season = self.seasons[i]

            if not season.isValid():
                print(season.error)
                return season.error
            else:
                for dataType in self.dataTypes:
                    dataList = self.getData(dataType, season)
                    data = self.consolidateData(dataList)
                    data = self.cleanData(data, dataType)
                    data = self.transformData(data, dataType)
                    csv = self.transformToCsv(data)
                    self.saveCsv(csv, dataType, season)

        

    def getMap(self, dataSource):
        if dataSource == "QuantHockey":
            return QuantHockeyMap
        else:
            return {}

    def addFantasyAverages(self, dataType, listOfDataModels):
        transformer = self.transformer(dataType, self.map)
        data = transformer.addAverages(listOfDataModels)
        return data