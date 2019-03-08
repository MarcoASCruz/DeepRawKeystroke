from .analysisBuilder import AnalysisBuilder

from networks.DRK import DRK

from partitionMethods.trainedAndUntrainedImpostors import TrainedAndUntrainedImpostors
#from partitionMethods.simpleAnalyse import SimpleAnalyse

from data.keystrokeRawDataBase import configConnectionDB
from data.partition.heterogeneousRawData import HeterogeneousKeystrokeDatas as KeystrokeDatasRawData
#from data.partition.simpleRawDataPartitionMethod import SimpleRawDataPartitionMethod as KeystrokeDatasRawData

class RawDataAnalysisBuilder(AnalysisBuilder):

    _experimentPrefix = "R.D."

    def getClassifiers(self):
        return [
            DRK()
        ]

    def createPartitionMethod(self):
        partitionMethod = TrainedAndUntrainedImpostors(
            self.getKeystrokeDatas(),
            fakeUsersSubsetSizeIsDynamic = self.fakeUsersSubsetSizeIsDynamic,
            keyEvents = self.keyEvents,
            seed = self.seed
        )
        partitionMethod.limitUserAmount = self.limitUserAmount
        return partitionMethod

    def createKeystrokeDatas(self):
        configConnectionDB['database'] = self.databaseName
        self._keystrokeDatas = KeystrokeDatasRawData(
            configConnectionDB=configConnectionDB,
            seed = self.seed
        )
        return self._keystrokeDatas