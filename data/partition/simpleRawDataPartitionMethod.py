import numpy as np

from data.keystrokeRawDataBase import KeystrokeRawDataBase


class SimpleRawDataPartitionMethod(KeystrokeRawDataBase):

    def getDatasAndLabels(self, idUser):
        trueData, trueLabels = self.getTrueSamples(idUser)
        fakeData, fakeLabels = self.getFalseSamples(idUser, len(trueLabels))
        data = np.concatenate((trueData, fakeData), axis=0)
        dataLabels = np.concatenate((trueLabels, fakeLabels), axis=0)
        return data, dataLabels

    def getFalseSamples(self, idUser, trueSamplesAmount):
        falseSamples = []
        falseSamples = self.selectFalseSamples(
            [idUser],
            0,
            falseSamples,
            trueSamplesAmount,
            firstKeys = False,
            userIn = False,
            randomSeed = idUser
        )
        labelsArray = ([self.labelForFalseValues] * len(falseSamples))
        return falseSamples, labelsArray

    def selectFalseSamples(self, user, firstKeysLimit, partialDataset, samplesAmount, firstKeys = True, userIn = True, randomSeed = 0.5):
        selectString = """
        SELECT user_string_keystrokes.key_code, user_string_keystrokes.down, user_string_keystrokes.up, user_string_keystrokes.id_string, user_string_keystrokes.id_user 
        FROM user_string_keystrokes JOIN (
            SELECT id_user, id_string, repetition
            FROM user_string_keystrokes
            GROUP BY id_string, repetition
            HAVING id_user {} (%(idUser)s) AND repetition {} %(firstKeysLimit)s
            ORDER BY RAND(%(randomSeed)s)
            LIMIT %(samplesAmount)s
        ) as rus ON (
            user_string_keystrokes.id_user = rus.id_user AND
            user_string_keystrokes.id_string = rus.id_string
        )
        """

        if firstKeys:
            selectString = selectString.format("IN", "<=")
        else:
            if userIn:
                selectString = selectString.format("IN", ">")
            else:
                selectString = selectString.format("NOT IN (" + ",".join(map(str, user)) + ") AND 1 = ", ">")
                user = 1

        datas = self.selectSample(
            selectString = selectString,
            constraints="",
            parameters = {
                'idUser': user,
                'firstKeysLimit': firstKeysLimit,
                'samplesAmount': samplesAmount,
                'randomSeed': randomSeed
            },
            order=" ORDER BY id_user, id_string, down "
        )
        if partialDataset == []:
            partialDataset = datas
        else:
            partialDataset = np.concatenate((partialDataset, datas), axis=0)
        return partialDataset