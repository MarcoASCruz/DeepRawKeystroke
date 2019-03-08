import os
currentPath = os.getcwd()
fatherPath = os.path.abspath(os.path.join(currentPath, os.pardir, os.pardir))
import sys
sys.path.append(fatherPath)

from analysis.rawDataAnalysisBuilder import RawDataAnalysisBuilder
from data.keystrokeRawDataBase import configConnectionDB
from data.keystrokeRawDataBase import KeystrokeRawDataBase

import multiprocessing

databaseName = 'killourhy_and_maxion_2009'

def analyseUser(idUser):
    analysisBuilder = RawDataAnalysisBuilder(
        databaseName,
        22,
        allocateMemoryDynamically=True,
        limitUserAmount=[idUser]
    )
    analysisBuilder.run(0)

if __name__ == '__main__':
    configConnectionDB['database'] = databaseName
    keystrokeData = KeystrokeRawDataBase(
        configConnectionDB=configConnectionDB
    )
    users = keystrokeData.selectUsers()
    print(users)

    cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpus)
    pool.map(analyseUser, users)
