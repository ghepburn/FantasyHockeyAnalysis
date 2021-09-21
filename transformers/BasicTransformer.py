import copy

class BasicTransformer:
    def __init__(self, dataType, map):
        self.transformerType = dataType
        self.map = map

    def transform(self, data):
        data = self.renameColumns(data)
        data = self.removeColumns(data)
        data = self.rearrangeColumns(data)
        data = self.add3YearAverages(data)
        data = self.addFantasyWeightings(data)
        data = self.sort(data)
        return data

    def removeColumns(self, data):
        correctColumns = self.map.getNewColumnNames(self.transformerType)
        currentColumns = data.getColumns()
        for col in currentColumns:
            if col not in correctColumns:
                data.removeColumn(col)
        return data

    def rearrangeColumns(self, data):
        correctColumnNames = self.map.getNewColumnNames(self.transformerType)
        currentColumnNames = data.getColumns()
        dataCopy = copy.deepcopy(data)

        for i in range(len(correctColumnNames)):

            if len(currentColumnNames) != i:
                correctColName = correctColumnNames[i+1]
                currentColName = currentColumnNames[i]
                if correctColName != currentColName:
                    correctColData = dataCopy.getColumn(correctColName)
                    data.setColumnName(i, correctColName)
                    data.setColumn(correctColName, correctColData)

        return data


    def renameColumns(self, data):
        currentColumns = data.getColumns()
    
        # columns
        for i in range(len(currentColumns)):
            colName = currentColumns[i]
            
            if colName in self.map.getOldColumnNames(self.transformerType):
                correctedName = self.map.getNewColumnName(self.transformerType, colName)
                if colName != correctedName:
                    data.setColumnName(i, correctedName)

        # index
        indexName = data.getIndexName()
        if indexName in self.map.getOldColumnNames(self.transformerType):
            data.setIndexName(self.map.getNewColumnName(self.transformerType, indexName))

        return data

    def add3YearAverages(self, data):
        return data

    def addFantasyWeightings(self, data):
        fantasyWeights = []

        numOfRows = data.getNumOfRows()
        columns = self.map.getNewColumnNames(self.transformerType)
        
        for i in range(numOfRows):
            row = data.getRow(i)
            rowFantasyPoints = 0
            for col in columns: 
                colWeight = self.map.getColumnWeight(self.transformerType, col)
                if colWeight:
                    colData = row[col]
                    itemFantasyWeight = colWeight * colData
                    rowFantasyPoints += itemFantasyWeight
            fantasyWeights.append(rowFantasyPoints)

        data.addColumn("FantasyPoints", fantasyWeights)        

        return data

    def sort(self, data):
        sortBy = "FantasyPoints"
        data.sort(sortBy)
        return data
