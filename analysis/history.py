class History():
    histories = []
    experimentDescription = ''

    def __init__(self, experimentDescription, histories):
        self.histories = histories
        self.experimentDescription = experimentDescription

    def saveTxt(self):
        file = open(self.experimentDescription + ".txt", "w")
        file.write(self.toString())
        file.close()
        self.histories = []

    def toString(self):
        return '{ "experimentDescription": "' + self.experimentDescription +'", "histories":  ' + str(self.histories) + "}"