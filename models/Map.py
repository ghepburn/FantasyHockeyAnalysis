class Map:
    def __init__(self, map):
        self.map = map
        self.types = self.getMapTypes()

    def getMapTypes(self):
        return self.map.keys()

    def getHeaderRow(self, mapType):
        return self.map[mapType]["headerRow"]

    def getIndexColumn(self, mapType):
        return self.map[mapType]["indexCol"]

    def getNewColumnNames(self, mapType):
        columns = []
        for col in self.map[mapType]["columns"].keys():
            newColumnName = self.map[mapType]["columns"][col]["Name"]
            columns.append(newColumnName)
        return columns

    def getOldColumnNames(self, mapType):
        return self.map[mapType]["columns"].keys()

    def getNewColumnName(self, mapType, oldColName):
        return self.map[mapType]["columns"][oldColName]["Name"]
        
    def getColumnWeight(self, mapType, column):
        keys = self.map[mapType]["columns"].keys()
        for key in keys:
            value = self.map[mapType]["columns"][key]
            columnName = value["Name"]
            if column == columnName:
                if "Weight" in value.keys():
                    return value["Weight"]
                else:
                    return False