import os
fatherPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))
import sys
sys.path.append(fatherPath)

from analysis.rawDataAnalysisBuilder import RawDataAnalysisBuilder

analysisBuilder = RawDataAnalysisBuilder(
    'antal_2016_mobikey',
    30
)

if __name__ == '__main__':
    analysisBuilder.run(0)