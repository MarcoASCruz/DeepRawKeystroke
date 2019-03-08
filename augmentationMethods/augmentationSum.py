import math
from .augmentationBase import AugmentationBase

class AugmentationSum(AugmentationBase):

    def createNewData(self, data, labels, sumNumber):
        sumNumber = (sumNumber * math.pow(10, -3))
        newData = data + sumNumber
        return newData, labels