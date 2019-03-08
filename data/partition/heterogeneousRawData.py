import numpy as np
import random

from data.keystrokeRawDataBase import KeystrokeRawDataBase


class HeterogeneousKeystrokeDatas(KeystrokeRawDataBase):

    def getDatasAndLabels(self, idUser, testFirstKeysLimit = 5, samplesPerFakeUser = 5):
        trueData, trueLabels = self.getTrueSamples(idUser)
        fakeData, fakeLabels = self.getFalseSamples(idUser, testFirstKeysLimit, samplesPerFakeUser)
        data = np.concatenate((trueData, fakeData), axis=0)
        dataLabels = np.concatenate((trueLabels, fakeLabels), axis=0)
        return data, dataLabels

    def getFalseSamples(self, idUser, testFirstKeysLimit, samplesPerFakeUser):
        users = self.selectUsers()
        randomSamples = []
        firstKeysSet = []
        users.remove(idUser)
        random.seed(self.seed)
        users = random.sample(users, self.getFakeUsersSubsetSize())

        for user in users:
            firstKeysSet = self.selectFalseSamples(
                user,
                testFirstKeysLimit,
                firstKeysSet,
                samplesPerFakeUser
            )

        firstKeyLength = len(firstKeysSet)
        randomSamples = self.selectFalseSamples(
            idUser,
            testFirstKeysLimit,
            randomSamples,
            firstKeyLength,
            False
        )

        userDatas = np.concatenate((firstKeysSet, randomSamples), axis=0)
        labelsArray = ([self.labelForFalseValues] * len(userDatas))
        return userDatas, labelsArray

    def selectFalseSamples(self, user, firstKeysLimit, partialDataset, samplesAmount, firstKeys = True):
        selectString = """
        SELECT user_string_keystrokes.key_code, user_string_keystrokes.down, user_string_keystrokes.up, user_string_keystrokes.id_string, user_string_keystrokes.id_user
        FROM user_string_keystrokes JOIN (
            SELECT id_user, id_string, repetition
            FROM user_string_keystrokes
            GROUP BY id_string, repetition
            HAVING id_user {} %(idUser)s AND repetition {} %(firstKeysLimit)s
            ORDER BY RAND(0.5)
            LIMIT %(samplesAmount)s
        ) as rus ON (
            user_string_keystrokes.id_user = rus.id_user AND
            user_string_keystrokes.id_string = rus.id_string
        )
        """

        if firstKeys:
            selectString = selectString.format("=", "<=")
        else:
            selectString = selectString.format("<>", ">")

        datas = self.selectSample(
            selectString = selectString,
            constraints="",
            parameters = {
                'idUser': user,
                'firstKeysLimit': firstKeysLimit,
                'samplesAmount': samplesAmount
            },
            order=" ORDER BY id_user, id_string, down "
        )
        if partialDataset == []:
            partialDataset = datas
        else:
            partialDataset = np.concatenate((partialDataset, datas), axis=0)
        return partialDataset