from .rawDataAnalysisBuilder import RawDataAnalysisBuilder
from partitionMethods.simpleAnalyseDataAugmentation import SimpleAnalyseDataAugmentation

class RawDataAugmentedAnalysisBuilder(RawDataAnalysisBuilder):

    def __init__(self, augmentationBuilder, **kwargs):
        super(RawDataAugmentedAnalysisBuilder, self).__init__(**kwargs)
        self.augmentationBuilder = augmentationBuilder


    def createPartitionMethod(self):
        deepKeystrokeDataAugmentationAndCrossValidation = SimpleAnalyseDataAugmentation(
            self.getKeystrokeDatas(),
            fakeUsersSubsetSizeIsDynamic = self.fakeUsersSubsetSizeIsDynamic,
            keyEvents = self.keyEvents,
            seed = self.seed
        )
        deepKeystrokeDataAugmentationAndCrossValidation.limitUserAmount = self.limitUserAmount
        deepKeystrokeDataAugmentationAndCrossValidation.augmentationBuilder = self.augmentationBuilder
        return deepKeystrokeDataAugmentationAndCrossValidation