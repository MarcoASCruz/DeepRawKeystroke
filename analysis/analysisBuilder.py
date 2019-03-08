from .analysisBase import AnalysisBase

class AnalysisBuilder:

    _keystrokeDatas = None
    _experimentPrefix = ''

    def __init__(self, databaseName, keyEvents, experimentDescription = "", allocateMemoryDynamically = False, saveResults = True, fakeUsersSubsetSizeIsDynamic = True, seed = 1, limitUserAmount = 0, saveClassifiersFitHistory = False):
        self.databaseName = databaseName
        self.experimentDescription = experimentDescription
        self.allocateMemoryDynamically = allocateMemoryDynamically
        self.saveResults = saveResults
        self.keyEvents = keyEvents
        self.fakeUsersSubsetSizeIsDynamic = fakeUsersSubsetSizeIsDynamic
        self.seed = seed
        self.limitUserAmount = limitUserAmount
        self.saveClassifiersFitHistory = saveClassifiersFitHistory

    def run(self, classifierIndex):
        analysisBase = AnalysisBase(
            self.getKeystrokeDatas(),
            self.createPartitionMethod(),
            [(self.getClassifiers())[classifierIndex]],
            saveResults = self.saveResults,
            experimentDescription = self._experimentPrefix + self.experimentDescription,
            allocateMemoryDynamically = self.allocateMemoryDynamically,
            seed = self.seed,
            saveClassifiersFitHistory = self.saveClassifiersFitHistory
        )
        analysisBase.run()

    def getClassifiers(self):
        pass

    def createPartitionMethod(self):
       pass

    def getKeystrokeDatas(self):
        result = self._keystrokeDatas
        if self._keystrokeDatas == None:
            result = self.createKeystrokeDatas()
        return result

    def createKeystrokeDatas(self):
        pass