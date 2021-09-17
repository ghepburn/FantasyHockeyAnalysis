from .BasicTransformer import BasicTransformer

class BasicDataFrameTransformer(BasicTransformer):
    # def __init__(self, dataType):
    #     super().__init__(self, dataType)
        

    def transform(self, data):
        # df = self.setColumns(df)
        # df = self.addFantasyColumns(df)
        return data

    # def 

    def setColumns(self, data):
        columns = data.columns

        return data

    def addFantasyColumns(self, data):
        return data