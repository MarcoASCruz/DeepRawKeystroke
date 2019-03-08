from .partitionMethodBase import PartitionMethodBase
from sklearn.model_selection import KFold
from .data import Data

class SimpleAnalyseDataAugmentation(PartitionMethodBase):

    crossValidationSets = 10

    def run(self, callAlgorithmsCallback):
        keyEvents = self.getkeyEvents()
        users = self.keystrokeDatas.selectUsers()
        if self.limitUserAmount:
            users = self.getUserSubset(users)
        for user in users:
            self.user = user

            data, labels = self.keystrokeDatas.getDatasAndLabels(user)
            data, labels = self.shuffleEqually(data, labels)

            kFold = KFold(n_splits = self.crossValidationSets)

            for trainIndex, testIndex in kFold.split(data):
                trainData, testData = data[trainIndex], data[testIndex]
                trainLabels, testLabels = labels[trainIndex], labels[testIndex]

                trainData, trainLabels = self.createAugmentedData(trainData, trainLabels)

                self.originalLabels = testLabels

                callAlgorithmsCallback(
                    Data(trainData, trainLabels, testData, testLabels),
                    self
                )

    def createAugmentedData(self, trainData, trainLabels):
        return self.augmentationBuilder.execute(trainData, trainLabels)