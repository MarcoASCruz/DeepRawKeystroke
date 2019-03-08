import datetime
from .experimentConfiguration import ExperimentConfiguration
from .history import History

class AnalysisBase():

    classifiersFitHistory = []

    def __init__(self, keystrokeDatas, scenario, classifiers, saveResults = True, allocateMemoryDynamically = False, experimentDescription = "", seed = 1, saveClassifiersFitHistory = False):
        self.keystrokeDatas = keystrokeDatas
        self.scenario = scenario
        self.classifiers = classifiers
        self.initialDate = datetime.datetime.now()
        self.saveResults = saveResults
        self.allocateMemoryDynamically = allocateMemoryDynamically
        self.experimentDescription = experimentDescription
        self.seed = seed
        self.saveClassifiersFitHistory = saveClassifiersFitHistory

    def run(self):
        self.scenario.run(self.classifiersCallback)
        if self.saveClassifiersFitHistory:
            self.saveClassifiersFitHistoryTxt()


    def classifiersCallback(self, data, partitionMethod):
        for classifier in self.classifiers:
            self.classify(data, partitionMethod, classifier)

    def classify(self, data, partitionMethod, classifier):
        classifier.seed = self.seed
        classifier.inputDim = partitionMethod.keyEvents
        classifier.tensorBoardTrackDescription = str(partitionMethod.user)
        classifier.allocateMemoryDynamically = self.allocateMemoryDynamically
        classificationResults = classifier.run(
            data.trainData,
            data.trainLabels,
            data.testData,
            data.testLabels
        )
        if self.saveClassifiersFitHistory:
            self.classifiersFitHistory.append(classifier.getLastHistory())

        if self.saveResults:
            self.saveAnalysis(
                partitionMethod,
                classificationResults,
                self.createExperimentConfiguration(classifier, partitionMethod)
            )

    def saveAnalysis(self, partitionMethod, predictionsProbs, experimentConfigs):
        self.keystrokeDatas.savePredictions(
            partitionMethod.user,
            predictionsProbs,
            partitionMethod.originalLabels,
            experimentConfigs,
            fakeUser = partitionMethod.fakeUser
        )

    def createExperimentConfiguration(self, classifier, partitionMethod):
        description = classifier.experimentDescription
        if self.experimentDescription != "":
            description = classifier.experimentDescription + " - " + self.experimentDescription

        if classifier.id == None:
            classifier.id = self.keystrokeDatas.getAlgorithmConfigurationsId(classifier)

        if partitionMethod.id == None:
            partitionMethod.id = self.keystrokeDatas.getPartitionMethodId(partitionMethod)

        experimentConfiguration = ExperimentConfiguration(
            description = description,
            algorithmConfiguration = classifier.id,
            partitionMethod = partitionMethod.id,
            date = self.initialDate
        )

        return experimentConfiguration

    def saveClassifiersFitHistoryTxt(self):
        description = self.keystrokeDatas.configConnectionDB["database"] + "_classifierId-" + str(self.classifiers[0].id) + "_" + (str(self.initialDate).replace(":", "-"))
        history = History(description, self.classifiersFitHistory)
        history.saveTxt()
        self.classifiersFitHistory = []