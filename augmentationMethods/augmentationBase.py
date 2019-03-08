import numpy as np

class AugmentationBase:
    def __init__(self, parameters = None):
        self.parameters = parameters

    def execute(self, data, labels):
        augmentedData = np.array([])
        augmentedLabels = np.array([])
        if self.parameters == None:
            newData, newLabels = self.createNewData(data, labels, None)
            augmentedData = newData
            augmentedLabels = newLabels
        else:
            for parameter in self.parameters:
                newData, newLabels = self.createNewData(data, labels, parameter)
                if len(augmentedData) == 0:
                    augmentedData = newData
                    augmentedLabels = newLabels
                else:
                    augmentedData = np.concatenate((augmentedData, newData))
                    augmentedLabels = np.concatenate((augmentedLabels, newLabels))
        return augmentedData, augmentedLabels

    def createNewData(self, data, labels, parameter):
        pass

    def shuffleEqually(self, data, labels):
        assert len(data) == len(labels)
        randomize = np.arange(len(data))
        np.random.shuffle(randomize)
        data = data[randomize]
        labels = labels[randomize]
        return data, labels