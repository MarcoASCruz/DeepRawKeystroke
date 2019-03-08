import numpy as np

class AugmentationDataBuilder():

    def __init__(self, augmentationMethods):
        self.augmentationMethods = augmentationMethods

    def execute(self, data, labels):
        newData = data
        newLabels = labels
        for augmentationMethod in self.augmentationMethods:
            augmentedData, augmentedLabels = augmentationMethod.execute(data, labels)
            newData = np.concatenate((newData, augmentedData))
            newLabels = np.concatenate((newLabels, augmentedLabels))
        return newData, newLabels

    def toString(self):
        result = ""
        for augmentationMethod in self.augmentationMethods:
            result = result + "- " + augmentationMethod.__class__.__name__ + " - " + str(augmentationMethod.parameters)
        return result

