from .partitionMethodBase import PartitionMethodBase
import numpy as np
from .data import Data

class DeepKeystroke(PartitionMethodBase):

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

            trueData, fakeData = np.split(data, [self.getSamplesAmount()])
            trueLabels, fakeLabels = np.split(labels, [self.getSamplesAmount()])

            trainTrueData, testTrueData = np.split(trueData, [self.getTrueSamples()])
            labelsTrueTraining, labelsTrueTest = np.split(trueLabels, [self.getTrueSamples()])

            trainFalseData, testFalseData = np.split(fakeData, [self.getFalseSamples()])
            labelsFalseTraining, labelsFalseTest = np.split(fakeLabels, [self.getFalseSamples()])

            trainData, trainLabels = self.createTrainData(trainTrueData, trainFalseData, labelsTrueTraining, labelsFalseTraining)

            testData = np.concatenate((testTrueData, testFalseData), axis=0)
            testLabels = np.concatenate((labelsTrueTest, labelsFalseTest), axis=0)

            trainData, trainLabels = self.shuffleEqually(trainData, trainLabels)
            testData, testLabels = self.shuffleEqually(testData, testLabels)

            self.originalLabels = testLabels

            callAlgorithmsCallback(
                Data(trainData, trainLabels, testData, testLabels),
                self
            )

    def createTrainData(self, trainTrueData, trainFalseData, labelsTrueTraining, labelsFalseTraining):
        trainData = np.concatenate((trainTrueData, trainFalseData), axis=0)
        trainLabels = np.concatenate((labelsTrueTraining, labelsFalseTraining), axis=0)
        return trainData, trainLabels

