class DataModel:
    def __init__(self, data):
        self.data = data

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getColumns(self):
        pass

    def setColumns(self, columns):
        pass

    def addColumn(self, name, data):
        pass

    def getRow(self, index):
        pass

    def editRow(self, index, data):
        pass

    def addRow(self, index, data):
        pass

    def transformToCsv(self):
        pass

    def append(self, data):
        pass