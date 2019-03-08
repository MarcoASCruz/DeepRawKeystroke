from .partitionMethodBase import PartitionMethodBase
from sklearn.model_selection import KFold
from .data import Data

class TrainedAndUntrainedImpostors(PartitionMethodBase):

    crossValidationSets = 10

    def run(self, callAlgorithmsCallback):
        keyEvents = self.getkeyEvents()
        users = self.keystrokeDatas.selectUsers()
        if self.limitUserAmount:
            users = self.getUserSubset(users)
        for user in users:
            self.user = user
            trueUserSamplesAmount = self.keystrokeDatas.getUserTrueDataSize(user)

            self.userAmount = len(users)
            self.userSamples = trueUserSamplesAmount
            if self.fakeUsersSubsetSizeIsDynamic:
                self.fakeUsersSubsetSize = self.calculateFakeUserSubsetSize(trueUserSamplesAmount)

            self.keystrokeDatas.setFakeUsersSubsetSize(self.fakeUsersSubsetSize)

            data, labels = self.keystrokeDatas.getDatasAndLabels(
                user,
                self.testFirstKeysLimit,
                self.firstImpostorSamplesAmount
            )
            data, labels = self.shuffleEqually(data, labels)

            kFold = KFold(n_splits = self.crossValidationSets)

            for trainIndex, testIndex in kFold.split(data):
                trainData, testData = data[trainIndex], data[testIndex]
                trainLabels, testLabels = labels[trainIndex], labels[testIndex]

                self.originalLabels = testLabels

                callAlgorithmsCallback(
                    Data(trainData, trainLabels, testData, testLabels),
                    self
                )