import pandas as pd

from .DataModel import DataModel

class DfModel(DataModel):
    def __init__(self, data=None, sheetName=None, headerRow=0, indexCol=0):
        self.sheetName = sheetName

        if data and type(data) == str:
            self.data = self.createDataFrame(data, headerRow, indexCol)
        elif not data:
            self.data = self.createDataFrame()
        else:
            self.data = data

    def createDataFrame(self, path=None, headerRow=0, indexCol=False):
        if not path:
            return pd.DataFrame()

        pathList = path.split("/")
        fileName = pathList[-1]
        fileNameList = fileName.split(".")
        if fileNameList[-1] == "csv":
            df = pd.read_csv(path, header=headerRow, index_col=indexCol)
        elif fileNameList[-1] == "xlsx":
            df = pd.read_excel(path, self.sheetName, header=headerRow, index_col=indexCol)
        else:
            df = pd.DataFrame()

        return df

    def getIndexName(self):
        return self.data.index.name

    def setIndexName(self, indexName):
        self.data.index.name = indexName

    def getColumns(self):
        return list(self.data.columns)

    def getColumn(self, colName):
        return self.data[colName]

    def isColumn(self, colName):
        if colName in self.getColumns():
            return True
        else:
            return False

    def setColumnNames(self, columns):
        self.data.columns = columns
    
    def setColumnName(self, index, name):
        columns = self.getColumns()
        columns[index] = name
        self.setColumnNames(columns)

    def setColumn(self, name, colData):
        self.data[name] = colData

    def addColumn(self, colName, data):
        self.data[colName] = data

    def removeColumn(self, name):
        if self.isColumn(name):
            self.data.drop(columns=[name], inplace=True)

    def switchColumns(self, colName1, colName2):
        columns = self.getColumns()
        for i in range(len(columns)):
            if columns[i] == colName1:
                colName1Index = i
            elif columns[i] == colName2:
                colName2Index = i

        # remember data
        colName1Data = self.getColumn(colName1)
        colName2Data = self.getColumn(colName2)
        
        # switch names
        self.setColumnName(colName1Index, colName2)
        self.setColumnName(colName2Index, colName1)

        # switch data
        self.setColumn(colName1, colName1Data)
        self.setColumn(colName2, colName2Data)

    # def swapColumns(self, column1, column2):
    #     placeholder = self.df[column1]
    #     self.df[column1] = self.df[column2]

    def getRow(self, index):
        return self.data.iloc[index]

    def editRow(self, index, data):
        self.data.iloc[index] = data

    def addRow(self, index, data):
        self.data.iloc[index] = data

    def dropRow(self, index):
        self.data = self.data.drop(index)

    def transformToCsv(self):
        return self.data.to_csv()

    def append(self, df):
        self.data = self.data.append(df.data)
        return self.data

    def getItem(self, row, col):
        return self.data.iloc[row][col]

    def getNumOfRows(self):
        return len(self.data.index)

    def sort(self, sortBy):
        self.data.sort_values(by=sortBy, inplace=True, ascending=False)