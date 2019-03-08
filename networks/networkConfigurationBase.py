from keras import backend as K
from keras.callbacks import TensorBoard
import numpy as np
import random as rn
import os
import tensorflow as tf

class NetworkConfigurationBase():

    id = None
    seed = 1
    lastFitHistory = []

    def __init__(self,
                 experimentDescription,
                 inputDim,
                 hiddenDim,
                 optimizer,
                 dropouts = "",
                 batchSize = 1,
                 epochs = 32,
                 learningRate = 0.001,
                 lossFunction = 'mean_squared_error',
                 nbGibbsSteps = 0,
                 fineTunningEpochs = 0,
                 fineTunningHiddenLayerActivation = '',
                 fineTunningOutputLayerActivation = '',
                 tensorBoardTrack = False,
                 allocateMemoryDynamically = False):
        self.experimentDescription = experimentDescription
        self.inputDim = inputDim
        self.hiddenDim = hiddenDim
        self.dropouts = dropouts
        self.batchSize = batchSize
        self.epochs = epochs
        self.learningRate = learningRate
        self.optimizer = optimizer
        self.lossFunction = lossFunction

        self.nbGibbsSteps = nbGibbsSteps
        self.fineTunningEpochs = fineTunningEpochs
        self.fineTunningHiddenLayerActivation = fineTunningHiddenLayerActivation
        self.fineTunningOutputLayerActivation = fineTunningOutputLayerActivation

        self.allocateMemoryDynamically = allocateMemoryDynamically
        self.tensorBoardTrack = tensorBoardTrack
        self.tensorBoardTrackPath = 'config'
        self.tensorBoardTrackDescription = '000'

    def getOptimizer(self):
        return self.optimizer()

    def run(self, trainData, trainLabels, testData, testLabels):
        np.random.seed(self.seed)
        rn.seed(self.seed)
        os.environ['PYTHONHASHSEED'] = '0'

        if K.backend() == 'tensorflow':

            tf.set_random_seed(self.seed)

            if self.allocateMemoryDynamically:
                config = tf.ConfigProto()
                config.gpu_options.allow_growth = True
                session = tf.Session(config=config)
                K.set_session(session)

        predictionsProbs = self.create(trainData, trainLabels, testData, testLabels)
        if "clear_session" in dir(K):
            K.clear_session()
        return predictionsProbs

    def compile(self, model):
        model.compile(
            self.optimizer(),
            loss=self.lossFunction,
            metrics=['accuracy']
        )
        return model

    def fit(self, model, trainData, trainLabels, testData, testLabels, epochs = None, callbacks=[]):
        if epochs == None:
            epochs = self.epochs
        if callbacks == []:
            callbacks = self.getCallbacks()
        fitHistory = model.fit(
            trainData,
            trainLabels,
            epochs = epochs,
            verbose = 0,
            batch_size = self.batchSize,
            validation_data = (testData, testLabels),
            shuffle = False,
            callbacks = callbacks
        )
        self.lastFitHistory = fitHistory
        return model

    def getCallbacks(self):
        callbacks = []
        if self.tensorBoardTrack:
            callbacks = [
                TensorBoard(
                    log_dir= self.getDirName(),
                    batch_size = self.batchSize,
                    histogram_freq = round(self.batchSize/2),
                    write_graph = True,
                    write_grads = False,
                    write_images = False
                )
            ]
        return callbacks

    def getDirName(self):
        return './{}/{}/{}'.format(self.__class__.__name__, self.tensorBoardTrackPath, self.tensorBoardTrackDescription)

    def create(self, trainData, trainLabels, testData, testLabels):
        raise "create was not implemented"

    def reshapeInputData(self, data, keyAmount, sampleSize, keyLength):
        result = []

        for i in range(0, keyAmount):
            result.append([])

        for i in range(0, len(data)):
            k = 0
            for j in range(0, sampleSize, keyLength):
                result[k].append([data[i][j], data[i][j + 1]])
                k = k + 1

        for i in range(0, keyAmount):
            result[i] = np.array(result[i])

        return result

    def createConfiguration(self):
        optimizer = self.getOptimizer()
        optimizerConfigurations = ''

        if optimizer:
            optimizerParameters = optimizer.get_config()
            optimizerConfigurations = str(sorted(optimizerParameters.items(), key=lambda x:x[0])).replace("'", "")

        configurations = {
            'description': str(self.experimentDescription),
            'inputDimensions': str(self.inputDim),
            'hiddenDimensions': str(self.hiddenDim),
            'dropouts': str(self.dropouts),
            'batchSize': str(self.batchSize),
            'nbEpochs': str(self.epochs),
            'leaningRate': str(self.learningRate),
            'optimizer': optimizer.__class__.__name__,
            'optimizerConfigurations': optimizerConfigurations,
            'nbGibbsSteps': self.nbGibbsSteps,
            'fineTunningEpochs': self.fineTunningEpochs,
            'fineTunningHiddenLayerActivation': self.fineTunningHiddenLayerActivation,
            'fineTunningOutputLayerActivation': self.fineTunningOutputLayerActivation
        }
        return configurations

    def getLastHistory(self):
        return self.lastFitHistory.history