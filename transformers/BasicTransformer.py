import copy

class BasicTransformer:
    def __init__(self, dataType, map):
        self.transformerType = dataType
        self.map = map

    def transform(self, data):
        data = self.removeColumns(data)
        data = self.rearrangeColumns(data)
        data = self.renameColumns(data)
        return data

    def removeColumns(self, data):
        correctColumns = list(self.map["columns"].values())
        currentColumns = data.getColumns()
        for col in currentColumns:
            if col not in correctColumns:
                data.removeColumn(col)
        return data

    def rearrangeColumns(self, data):
        correctColumns = list(self.map["columns"].values())
        dataSource = copy.deepcopy(data)

        for i in range(len(correctColumns)):
            colName = correctColumns[i]
            colIndex = i
            if dataSource.getColumn(colName):
                data.setColumn(colIndex, colName, dataSource[colName])
        return data


    def renameColumns(self, data):
        currentColumns = data.getColumns()
        for i in range(len(currentColumns)):
            colName = currentColumns[i]
            correctedName = self.map["columns"][colName]
            data.setColumnName(i, correctedName)
        return data