from .trainedAndUntrainedImpostorsBlockApproach import TrainedAndUntrainedImpostorsBlockApproach
from .partitionMethodBase import PartitionMethodBase

class TrainedAndUntrainedImpostorsBlockApproachDataAugmentation(TrainedAndUntrainedImpostorsBlockApproach, PartitionMethodBase):

    def createTrainData(self, trainDataBlocks, trainLabelsBlocks):
        trainData, trainLabels = self.convertBlockDataToAlgorithmsDataInputFormat(trainDataBlocks, trainLabelsBlocks)
        trainData, trainLabels = self.createAugmentedData(trainData, trainLabels)
        return trainData, trainLabels

    def createAugmentedData(self, trainData, trainLabels):
        return self.augmentationBuilder.execute(trainData, trainLabels)