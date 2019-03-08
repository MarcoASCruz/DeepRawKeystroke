import mysql.connector
from data.sqlConnection import SqlConnection

#put the name of the database
configConnectionDB = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'killourhy_and_maxion_2009',
    'charset': 'utf8',
    'use_unicode': True
}

configDBTableNames = {
    'keystrokes_attributes_per_string': 'keystrokes_attributes_per_string',
    'original_data': 'original_pre_processed_data',
    'user': 'user',
    'user_keystroke': 'user_keystroke',
    'user_key_string': 'user_key_string',
    'table_name_prefix': 'table_name_prefix',
    'trained_rbm': 'treined_rbm',
    'user_string_keystrokes': 'user_string_keystrokes',
}

class KeystrokeRawDataBase:

    def __init__(self, configConnectionDB = configConnectionDB, configDBTableNames = configDBTableNames, seed = 1):
        self.configConnectionDB = configConnectionDB
        self.configDBTableNames = configDBTableNames
        self.labelForTrueValues = 1
        self.labelForFalseValues = 0
        self.connection = SqlConnection(configConnectionDB)
        self.seed = seed

    def getDatasAndLabels(self, idUser):
        raise Exception('The method getDatasAndLabels was not implemented')

    def getTrueSamples(self, idUser):
        userDatas = self.selectSample(
            " WHERE id_user = %(idUser)s ",
            {
                'idUser': idUser
            }
        )
        labelsArray = ([self.labelForTrueValues] * len(userDatas))
        return userDatas, labelsArray

    def getFalseSamples(self, idUser, idFakeUser):
        userDatas = self.selectSample(
            selectString="(SELECT key_code, down, up, id_string, id_user, 0 as selec_order",
            constraints = " FROM (SELECT key_code, min(time) as down, max(time) as up, id_string, id_user FROM user_keystroke JOIN user_key_string ON (user_keystroke.id_string = user_key_string.id) GROUP BY id_user, id_string, key_code ) as ak JOIN ( SELECT id_user as user, min(id) as min_string_id FROM user_key_string GROUP BY id_user HAVING id_user <> %(idUser)s AND id_user <> %(idFakeUser)s ) mi ON (mi.user = ak.id_user AND (ak.id_string >= mi.min_string_id AND ak.id_string < mi.min_string_id + 4)) GROUP BY id_user, id_string, key_code ) "
                " UNION " +
                " (SELECT key_code, min(time) as down, max(time) as up, id_string, id_user, 1 as selec_order FROM user_keystroke JOIN user_key_string ON (user_keystroke.id_string = user_key_string.id) GROUP BY id_user, id_string, key_code HAVING id_user = %(idFakeUser)s )",
            parameters = {
                'idUser': idUser,
                'idFakeUser': idFakeUser
            },
            order = " ORDER BY selec_order, id_user, id_string, down "
        )
        labelsArray = ([self.labelForFalseValues] * len(userDatas))
        return userDatas, labelsArray

    def getAllSamples(self, constraints = ""):
        return self.selectSample(constraints = constraints, parameters = {})

    def selectSample(self, constraints, parameters, order = " ORDER BY id_user, id_string, down ", selectString = ""):
        if selectString == "":
            selectString = self.selectSampleString() + constraints + order
        else:
            selectString = selectString + constraints + order

        conn = self.connection
        if conn.getTransactionStatus() == False:
            conn.open()
        datas = conn.select(selectString, self.sampleSerializer, parameters)
        if conn.getTransactionStatus() == False:
            conn.close()
        return datas

    def selectSampleString(self):
        return " SELECT key_code, down, up, id_string, id_user FROM " + self.configDBTableNames['user_string_keystrokes'] + " "

    def sampleSerializer(self, cursor):
        datas = []
        sample = []
        idString = -1
        hasUnion = len(cursor.column_names) == 6
        for columns in cursor:
            if hasUnion:
                (key_code, down, up, id_string, id_user, selec_union) = columns
            else:
                (key_code, down, up, id_string, id_user) = columns
            #print("down {},  up {}".format(down, up))
            if (id_string != idString):
                if (idString != -1):
                    datas.append(sample)
                    sample = []
                idString = id_string
            sample.append(down)
            sample.append(up)
        datas.append(sample)
        return datas

    def selectUsers(self):
        selectString = "SELECT id FROM " + self.configDBTableNames['user']
        conn = self.connection
        conn.open()
        results = conn.select(selectString, self.userSerializer)
        conn.close()
        return results

    def userSerializer(self, cursor):
        models = []
        for (id,) in cursor:
            models.append(id)
        return models

    def selectSamples(self, constraints, parameters):
        selectString = "SELECT `H_period`, `DD_period_t`, `UD_period_t`,`H_t`,`DD_t_i`,`UD_t_i`,`H_i`,`DD_i_e`,`UD_i_e`,`H_e`,`DD_e_five`,`UD_e_five`,`H_five`,`DD_five_Shift_r`,`UD_five_Shift_r`,`H_Shift_r`,`DD_Shift_r_o`,`UD_Shift_r_o`,`H_o`,`DD_o_a`,`UD_o_a`,`H_a`,`DD_a_n`,`UD_a_n`,`H_n`,`DD_n_l`,`UD_n_l`,`H_l`,`DD_l_Return`,`UD_l_Return`,`H_Return` FROM `original_pre_processed_data` "
        selectString = selectString + constraints
        conn = self.connection
        conn.open()
        models = conn.select(selectString, self.sampleSerializer, parameters)
        conn.close()
        return models

    def savePredictions(self, user, outputs, targets, experimentConfigurations, fakeUser = ""):
        idExperiment = self.getExperimentConfigurationsId(experimentConfigurations)
        stringSql = "INSERT INTO experiment_output_data (`id_user`, fake_tested_user, `output`, target, session, rep, id_experiment) VALUES( %(idUser)s, %(fakeTestedUser)s, %(output)s, %(target)s, %(session)s, %(rep)s, %(idExperiment)s);"
        sqlDatas = {
            'idUser': user,
            'fakeTestedUser': fakeUser,
            'output': 0,
            'target': 0,
            'session': 0,
            'rep': 0,
            'idExperiment': idExperiment
        }

        i = 0
        self.connection.open()
        cursor = self.connection.getCursor()
        for output in outputs:
            sqlDatas['output'] = float(output[0])
            target = int(targets[i])
            sqlDatas['target'] = target
            cursor.execute(stringSql, sqlDatas)
            i += 1
        cursor.close()

        self.connection.commit()
        self.connection.close()

    def getExperimentConfigurationsId(self, experimentConfigurations):
        idConfiguration = None
        date = experimentConfigurations.date
        configurations = {
            'description': experimentConfigurations.description,
            'date': '{}-{}-{} {}:{}:{}'.format(date.year, date.month, date.day, date.hour, date.minute, date.second),
            'algorithmConfiguration': experimentConfigurations.algorithmConfiguration,
            'partitionMethod': experimentConfigurations.partitionMethod
        }
        selectString = "SELECT id FROM `experiment` WHERE " + \
                       " date = %(date)s AND " + \
                       " id_algorithm = %(algorithmConfiguration)s AND " + \
                       " id_partition_method = %(partitionMethod)s "
        connection = self.connection
        connection.open()
        selectedConfiguration = connection.select(selectString, self.configurationSerializer, configurations)
        if selectedConfiguration == None:
            idConfiguration = self.insertExperimentConfiguration(configurations, self.connection)
        else:
            idConfiguration = selectedConfiguration['id']
        connection.close()
        return idConfiguration

    def configurationSerializer(self, cursor):
        configuration = None
        for (id,) in cursor:
            configuration = {'id': id}
        return configuration

    def insertExperimentConfiguration(self, configurations, connection=None):
        if connection == None:
            connection = self.connection
            connection.open()

        insertString = "INSERT INTO experiment (description, date, id_algorithm, id_partition_method) " + \
                       "VALUES (%(description)s, %(date)s, %(algorithmConfiguration)s, %(partitionMethod)s) "

        idConfiguration = connection.execute(insertString, configurations)

        if connection == None:
            connection.close()

        return idConfiguration

    def selectExperimentResults(self, user, experimentDate, algorithmConfiguration):
        selectString = """
            SELECT id, target, output
            FROM output_test_original_data
            WHERE
                user = %(user)s AND
                IF (initial_date = %(experimentDate)s, True, IF(CONVERT(initial_date, DATE) = %(experimentDate)s, True, False)) AND
                id_configuration = %(algorithmConfiguration)s
        """
        parameters = {
            "user": user,
            "experimentDate": experimentDate,
            "algorithmConfiguration": algorithmConfiguration
        }
        conn = self.connection
        conn.open()
        targets, outputs, minOutput, maxOutput = conn.select(selectString, self.experimentResultsSerializer, parameters)
        conn.close()
        return targets, outputs, minOutput, maxOutput

    def experimentResultsSerializer(self, cursor):
        targets = []
        outputs = []
        minOutput = 0
        maxOutput = 0
        firstLoop = True
        for id, target, output in cursor:
            output = 1 - output
            targets.append(target)
            outputs.append(output)
            if firstLoop:
                minOutput = output
                maxOutput = output
                firstLoop = False
            else:
                if output < minOutput:
                    minOutput = output
                if output > maxOutput:
                    maxOutput = output
        return targets, outputs, minOutput, maxOutput

    def getAlgorithmConfigurationsId(self, algorithm):
        idConfiguration = None
        configurations = algorithm.createConfiguration()
        selectString = "SELECT id FROM `algorithm_config` WHERE " + \
                       " description = %(description)s AND " + \
                       " input_dim = %(inputDimensions)s AND " + \
                       " hiden_dim = %(hiddenDimensions)s AND " + \
                       " dropouts = %(dropouts)s AND " + \
                       " batch_size = %(batchSize)s AND " + \
                       " nb_epochs = %(nbEpochs)s AND " + \
                       " learning_rate = %(leaningRate)s AND " + \
                       " optimizer = %(optimizer)s AND " + \
                       " optimizer_configurations = %(optimizerConfigurations)s "
        connection = self.connection
        connection.open()
        selectedConfiguration = connection.select(selectString, self.configurationSerializer, configurations)
        if selectedConfiguration == None:
            idConfiguration = self.insertAlgorithmConfiguration(configurations, self.connection)
        else:
            idConfiguration = selectedConfiguration['id']
        connection.close()
        return idConfiguration

    def insertAlgorithmConfiguration(self, configurations, connection=None):
        if connection == None:
            connection = self.connection
            connection.open()

        insertString = "INSERT INTO algorithm_config (description, input_dim, hiden_dim, dropouts, batch_size, nb_epochs, learning_rate, optimizer, optimizer_configurations) " + \
                       "VALUES (%(description)s, %(inputDimensions)s, %(hiddenDimensions)s, %(dropouts)s, %(batchSize)s, %(nbEpochs)s, %(leaningRate)s, %(optimizer)s, %(optimizerConfigurations)s)"

        idConfiguration = connection.execute(insertString, configurations)

        if connection == None:
            connection.close()

        return idConfiguration

    def getPartitionMethodId(self, partitionMethod):
        idConfiguration = None
        configurations = partitionMethod.createConfiguration()

        selectString = "SELECT id FROM `partition_method` WHERE " + \
                       " first_impostor_samples = %(firstImpostorSamplesAmount)s AND " + \
                       " fake_users_subset_size_is_dynamic = %(fakeUsersSubsetSizeIsDynamic)s AND " + \
                       " samples_input_length = %(keyEvents)s AND " + \
                       " description = %(description)s AND " + \
                       " seed = %(seed)s AND " + \
                       " cross_validation_sets = %(crossValidationSets)s "

        connection = self.connection
        connection.open()
        selectedConfiguration = connection.select(selectString, self.configurationSerializer, configurations)
        if selectedConfiguration == None:
            idConfiguration = self.insertPartitionMethodConfiguration(configurations, self.connection)
        else:
            idConfiguration = selectedConfiguration['id']
        connection.close()
        return idConfiguration

    def insertPartitionMethodConfiguration(self, configurations, connection = None):
        if connection == None:
            connection = self.connection
            connection.open()

        insertString = "INSERT INTO partition_method (first_impostor_samples, fake_users_subset_size_is_dynamic, samples_input_length, description, seed, cross_validation_sets ) " \
                       "VALUES (%(firstImpostorSamplesAmount)s, %(fakeUsersSubsetSizeIsDynamic)s, %(keyEvents)s, %(description)s, %(seed)s, %(crossValidationSets)s) "

        idConfiguration = connection.execute(insertString, configurations)

        if connection == None:
            connection.close()

        return idConfiguration

    def setFakeUsersSubsetSize(self, value = 51):
        self.fakeUsersSubsetSize = value

    def getFakeUsersSubsetSize(self):
        if not(hasattr(self, 'fakeUsersSubsetSize')):
            self.setFakeUsersSubsetSize()
        return self.fakeUsersSubsetSize

    def getUserTrueDataSize(self, idUser):
        trueData, trueLabels = self.getTrueSamples(idUser)
        return len(trueLabels)