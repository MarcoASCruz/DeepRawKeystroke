import random
import math
import numpy as np
from keras.utils.np_utils import to_categorical

class PartitionMethodBase():

    id = None
    userAmount = 51
    userSamples = 400
    firstImpostorSamplesAmount = 5
    testFirstKeysLimit = 5
    fakeUsersSubsetSize = 51
    description = ""
    limitUserAmount = 0
    originalLabels = None
    fakeUser = 0
    crossValidationSets = 0

    def __init__(self, keystrokeDatas, fakeUsersSubsetSizeIsDynamic = True, keyEvents = 31, seed = 1):
        self.keystrokeDatas = keystrokeDatas
        self.fakeUsersSubsetSizeIsDynamic = fakeUsersSubsetSizeIsDynamic
        self.keyEvents = keyEvents
        self.seed = seed

    def run(self, callAlgorithmsCallback):
        raise 'run was not implemented'

    def toCategorical(self, labels, numClasses=2):
        return to_categorical(labels, num_classes=numClasses)

    def getkeyEvents(self):
        return self.keyEvents

    def shuffleEqually(self, data, labels):
        assert len(data) == len(labels)
        np.random.seed(seed = self.seed)
        randomize = np.arange(len(data))
        np.random.shuffle(randomize)
        data = data[randomize]
        labels = labels[randomize]
        return data, labels

    def calculateFakeUserSubsetSize(self, trueUserSamplesAmount):
        return math.ceil((trueUserSamplesAmount / 2) / self.firstImpostorSamplesAmount)

    def getUserSubset(self, users):
        result = None
        if type(self.limitUserAmount) is list:
            result = self.limitUserAmount
        else:
            if self.limitUserAmount:
                random.seed(self.seed)
                result = random.sample(users, self.limitUserAmount)
            else:
                raise Exception("The limitUserAmount parameter needs to be higher than 0")
        print(result)
        return result


    def getUsersAmount(self):
        return self.userAmount

    def getSamplesAmount(self):
        return self.userSamples

    def getTrueSamples(self):
        # or without ceil?
        return math.ceil(self.getSamplesAmount() / 2)

    def getFalseSamples(self):
        return self.fakeUsersSubsetSize * self.getFirstImpostorSamplesAmount()

    def getFirstImpostorSamplesAmount(self):
        return self.firstImpostorSamplesAmount

    def getAllSamplesAmount(self):
        return self.getTrueSamples() + self.getFalseSamples()

    def createConfiguration(self):
        configurations = {
            'firstImpostorSamplesAmount': self.firstImpostorSamplesAmount,
            'fakeUsersSubsetSizeIsDynamic': self.fakeUsersSubsetSizeIsDynamic,
            'keyEvents': self.keyEvents,
            'description': self.__class__.__name__,
            'seed': self.seed,
            'crossValidationSets': self.crossValidationSets
        }
        return configurations