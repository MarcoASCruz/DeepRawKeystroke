import os
fatherPath = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))
import sys
sys.path.append(fatherPath)

from analysis.rawDataAugmentedAnalysisBuilder import RawDataAugmentedAnalysisBuilder
import math

x = 5
scaledNumbers = [x]
#scaledNumbers = [x, int(math.pow(x,2)), int(math.pow(x,3)), int(math.pow(x,4)), int(math.pow(x,5))]
#scaledNumbers = [x, x*2, x*3, x*4, x*5]
#scaledNumbers = [x, x+1, x+2, x+3, x+4]

analysisBuilder = RawDataAugmentedAnalysisBuilder(
    'killourhy_and_maxion_2009',
    22,
    experimentDescription = "scaledNumbers = " + str(scaledNumbers)
)

if __name__ == '__main__':
    analysisBuilder.run(0)