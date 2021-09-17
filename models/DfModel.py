import pandas as pd

from .DataModel import DataModel

class DfModel(DataModel):
    def __init__(self, data=None, sheetName=None):
        self.sheetName = sheetName

        if data and type(data) == str:
            self.data = self.createDataFrame(data)
        elif not data:
            self.data = self.createDataFrame()
        else:
            self.data = data

    def createDataFrame(self, path=None):
        if not path:
            return pd.DataFrame()

        pathList = path.split("/")
        fileName = pathList[-1]
        if fileName[-1] == "csv":
            df = pd.read_csv(path, self.sheetName, index_col=0)
        elif fileName[-1] == "xlsx":
            df = pd.read_excel(path, self.sheetName, index_col=0)
        else:
            df = pd.DataFrame()

        return df

    def getColumns(self):
        return self.data.columns

    def getColumn(self, name):
        try:
            return self.data[name]
        except:
            return False

    def setColumnNames(self, columns):
        self.data.columns = columns

    def setColumn(self, index, name, data):
        self.data.columns[index] = name
        self.data[name] = data

    def addColumn(self, name, data):
        self.data[name] = data

    def removeColumn(self, name):
        if self.getColumn(name):
            self.data.drop(columns=[name])

    # def swapColumns(self, column1, column2):
    #     placeholder = self.df[column1]
    #     self.df[column1] = self.df[column2]

    def getRow(self, index):
        return self.data.iloc[index]

    def editRow(self, index, data):
        self.data.iloc[index] = data

    def addRow(self, index, data):
        self.data.iloc[index] = data

    def transformToCsv(self):
        return self.data.to_csv()