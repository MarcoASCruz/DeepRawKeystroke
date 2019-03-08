from .partitionMethodBase import PartitionMethodBase
import numpy as np
import math
from .data import Data
from sklearn.model_selection import LeaveOneOut

class TrainedAndUntrainedImpostorsBlockApproach(PartitionMethodBase):

    firstHalfTrueSamples = []
    labelsFirstHalfTrueSamples = []

    secondHalfTrueSamples = []
    labelsSecondHalfTrueSamples = []

    firstHalfKnowFakes = []
    labelsFirstHalfKnowFakes = []

    secondHalfKnowFake = []
    labelsSecondHalfKnowFake = []

    firstHalfUnknowFake = []
    labelsFirstHalfUnknowFake = []

    secondHalfUnknowFakes = []
    labelsSecondHalfUnknowFakes = []

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

            self.firstHalfTrueSamples, self.secondHalfTrueSamples = np.split(trueData, [self.getTrueSamples()])
            self.labelsFirstHalfTrueSamples, self.labelsSecondHalfTrueSamples = np.split(trueLabels, [self.getTrueSamples()])
            self.firstHalfTrueSamples, self.labelsFirstHalfTrueSamples = self.shuffleEqually(self.firstHalfTrueSamples, self.labelsFirstHalfTrueSamples)
            self.secondHalfTrueSamples, self.labelsSecondHalfTrueSamples = self.shuffleEqually(self.secondHalfTrueSamples, self.labelsSecondHalfTrueSamples)

            knowFakes, unknowFakes = np.split(fakeData, [self.getFalseSamples()])
            labelsKnowFakes, labelsUnknowFakes = np.split(fakeLabels, [self.getFalseSamples()])

            self.firstHalfKnowFakes, self.secondHalfKnowFakes = np.split(knowFakes, [self.getKnowFakeSampleSize()])
            self.labelsFirstHalfKnowFakes, self.labelsSecondHalfKnowFakes = np.split(labelsKnowFakes, [self.getKnowFakeSampleSize()])

            self.firstHalfUnknowFakes, self.secondHalfUnknowFakes = np.split(unknowFakes, [self.getUnknowFakeSampleSize()])
            self.labelsFirstHalfUnknowFakes, self.labelsSecondHalfUnknowFakes = np.split(labelsUnknowFakes, [self.getUnknowFakeSampleSize()])

            kBlocks, kBlocksLabels = self.getKblocks()

            leaveOneOut = LeaveOneOut()
            for trainIndex, testIndex in leaveOneOut.split(kBlocks):
                trainDataBlocks = kBlocks[trainIndex]
                trainLabelsBlocks = kBlocksLabels[trainIndex]
                testDataBlock = kBlocks[testIndex]
                testLabelsBlock = kBlocksLabels[testIndex]

                trainData, trainLabels = self.createTrainData(trainDataBlocks, trainLabelsBlocks)
                testData, testLabels = self.convertBlockDataToAlgorithmsDataInputFormat(testDataBlock, testLabelsBlock)

                trainData, trainLabels = self.shuffleEqually(trainData, trainLabels)
                testData, testLabels = self.shuffleEqually(testData, testLabels)

                self.originalLabels = testLabels

                callAlgorithmsCallback(
                    Data(trainData, trainLabels, testData, testLabels),
                    self
                )

    def getFalseSamples(self):
        return self.getKnowFakeSampleSize() * 2

    def getKnowFakeSampleSize(self):
        return (math.ceil(self.fakeUsersSubsetSize/2) * self.getFirstImpostorSamplesAmount())

    def getUnknowFakeSampleSize(self):
        return ((self.fakeUsersSubsetSize - math.ceil(self.fakeUsersSubsetSize/2)) * self.getFirstImpostorSamplesAmount())

    def getKblocks(self):

        kBlocks = []
        kBlocksLabels = []

        unknowSetOrder = self.getUnknowSetOrder(len(self.firstHalfUnknowFakes))

        while (
            len(self.firstHalfTrueSamples) > 0 or
            len(self.secondHalfTrueSamples) > 0 or
            len(self.firstHalfKnowFakes) > 0 or
            len(self.secondHalfKnowFakes) > 0 or
            len(self.firstHalfUnknowFakes) > 0 or
            len(self.secondHalfUnknowFakes) > 0
        ):

            currentBlock = []
            currentBlockLabels = []

            self.firstHalfTrueSamples, currentBlock = self.getcurrentBlock(currentBlock, self.firstHalfTrueSamples)
            self.labelsFirstHalfTrueSamples, currentBlockLabels = self.getcurrentBlock(currentBlockLabels, self.labelsFirstHalfTrueSamples)

            if len(self.firstHalfKnowFakes) > 0:
                self.firstHalfKnowFakes, currentBlock = self.getcurrentBlock(currentBlock, self.firstHalfKnowFakes)
                self.labelsFirstHalfKnowFakes, currentBlockLabels = self.getcurrentBlock(currentBlockLabels, self.labelsFirstHalfKnowFakes)
            else:
                self.secondHalfKnowFakes, currentBlock = self.getcurrentBlock(currentBlock, self.secondHalfKnowFakes)
                self.labelsSecondHalfKnowFakes, currentBlockLabels = self.getcurrentBlock(currentBlockLabels, self.labelsSecondHalfKnowFakes)

            self.secondHalfTrueSamples, currentBlock = self.getcurrentBlock(currentBlock, self.secondHalfTrueSamples)
            self.labelsSecondHalfTrueSamples, currentBlockLabels = self.getcurrentBlock(currentBlockLabels, self.labelsSecondHalfTrueSamples)

            order = 0
            if len(unknowSetOrder) > 0:
                order = unknowSetOrder[0]
                unknowSetOrder = np.delete(unknowSetOrder, [0], axis=0)

            if order == 1:
                self.firstHalfUnknowFakes, currentBlock = self.getcurrentBlock(currentBlock, self.firstHalfUnknowFakes)
                self.labelsFirstHalfUnknowFakes, currentBlockLabels = self.getcurrentBlock(currentBlockLabels, self.labelsFirstHalfUnknowFakes)
            else:
                self.secondHalfUnknowFakes, currentBlock = self.getcurrentBlock(currentBlock, self.secondHalfUnknowFakes)
                self.labelsSecondHalfUnknowFakes, currentBlockLabels = self.getcurrentBlock(currentBlockLabels, self.labelsSecondHalfUnknowFakes)

            kBlocks.append(currentBlock)
            kBlocksLabels.append(currentBlockLabels)

        return np.array(kBlocks), np.array(kBlocksLabels)

    def getcurrentBlock(self, resultArray, samples):
        if len(samples) > 0:
            for i in range(self.getFirstImpostorSamplesAmount()):
                if len(samples) > 0:
                    resultArray.append(samples[0])
                    samples = np.delete(samples, [0], axis=0)
        return samples, resultArray

    def getUnknowSetOrder(self, subsetSize):
        size = int(subsetSize / self.getFirstImpostorSamplesAmount())
        ones = np.ones(size)
        zeros = np.zeros(size)
        result = np.concatenate((ones, zeros), axis=0)
        np.random.seed(seed=self.seed)
        np.random.shuffle(result)
        return result

    def createTrainData(self, trainDataBlocks, trainLabelsBlocks):
        trainData, trainLabels = self.convertBlockDataToAlgorithmsDataInputFormat(trainDataBlocks, trainLabelsBlocks)
        return trainData, trainLabels

    '''
        Numpy reshape seems not work for irregular arrays
    '''
    def convertBlockDataToAlgorithmsDataInputFormat(self, data, labels):
        newData = []
        newLabels = []

        dataSize = len(data)
        for i in range(dataSize):
            blockSize = len(data[i])
            for j in range(blockSize):
                newData.append(data[i][j])
                newLabels.append(labels[i][j])

        return np.array(newData), np.array(newLabels)