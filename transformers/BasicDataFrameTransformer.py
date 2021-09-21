from .BasicTransformer import BasicTransformer

class BasicDataFrameTransformer(BasicTransformer):
    def __init__(self, dataType, map):
        super().__init__(dataType, map)