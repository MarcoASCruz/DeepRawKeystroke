import numpy as np
from keras import optimizers
from keras.layers import Dense, Input, Concatenate, PReLU, BatchNormalization, Dropout, GaussianNoise, GaussianDropout
from keras.models import Model

from .networkConfigurationBase import NetworkConfigurationBase


def getOptimizer():
    return optimizers.Adagrad()

class DRK(NetworkConfigurationBase):
    def __init__(self,
                 experimentDescription = 'RawInput + Pair A. + FullyC.',
                 inputDim = 22,
                 hiddenDim = [50, 100],
                 optimizer = getOptimizer,
                 dropouts = [0.1, 0.25, 0.25],
                 batchSize = 10,
                 epochs = 200,
                 learningRate = 0,
                 lossFunction = 'binary_crossentropy',
                 fineTunningHiddenLayerActivation = "PReLU",
                 fineTunningOutputLayerActivation = "sigmoid"):
        super().__init__(
            experimentDescription,
            inputDim,
            hiddenDim,
            optimizer,
            dropouts,
            batchSize,
            epochs,
            learningRate,
            lossFunction,
            0,
            0,
            fineTunningHiddenLayerActivation,
            fineTunningOutputLayerActivation
        )

    def create(self, trainData, trainLabels, testData, testLabels):
        keyAmount = int(self.inputDim / 2)
        firstHiddenLayerPieces = []
        firstHiddenLayerNames = []
        keyLength = 2

        trainData = self.reshapeInputData(trainData, keyAmount, self.inputDim, keyLength)
        testData = self.reshapeInputData(testData, keyAmount, self.inputDim, keyLength)

        inputs = []

        for i in range(0, keyAmount):
            name = 'input_' + str(i)
            input = Input(
                shape=(keyLength,),
                name=name
            )
            inputs.append(input)

        for i in range(0, keyAmount - 1):
            name = 'pair_' + str(i)
            firstHiddenLayerNames.append(name)
            inputConcatenation = Concatenate()([inputs[i], inputs[i + 1]])
            inputConcatenationActivation = PReLU()(inputConcatenation)
            hiddenPiece = Dense(
                units=self.hiddenDim[0],
                name=name
            )(inputConcatenationActivation)
            pairActivation = PReLU()(hiddenPiece)
            dropout = Dropout(self.dropouts[0])(pairActivation)
            firstHiddenLayerPieces.append(dropout)

        concatenationLayer = Concatenate()(firstHiddenLayerPieces)
        batchLayer2 = BatchNormalization()(concatenationLayer)
        activationLayer2 = PReLU()(batchLayer2)
        dropout2 = Dropout(self.dropouts[1])(activationLayer2)

        hiddenLayer2 = Dense(self.hiddenDim[1])(dropout2)
        batchLayer3 = BatchNormalization()(hiddenLayer2)
        activationLayer4 = PReLU()(batchLayer3)
        dropout3 = Dropout(self.dropouts[2])(activationLayer4)

        output = Dense(units=1, activation=self.fineTunningOutputLayerActivation)(dropout3)

        model = Model(inputs=inputs, outputs=output)

        self.compile(model)
        print(model.summary())
        self.fit(model, trainData, np.array(trainLabels), testData, np.array(testLabels))

        return model.predict(testData)