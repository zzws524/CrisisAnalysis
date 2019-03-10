import logging
from ziwenLog import myLogConfig

#######Configuration items are here############
csvFileNeedToBeParsed='./Tables/ds07-Table 1.csv'
lostRatio=0.8
crisisThreshold=0.05
firstCrisisCountry='AN'
##############################################








######Don't change contents below#############

def parseCsvFile(fileName):
    with open(fileName,'r') as f:
        myLines=f.readlines()
    logger.info(myLines[0])

if __name__=='__main__':
    myLog=myLogConfig.ConfigMyLog(logFileName='DataProcess',withFolder=False)
    logger=logging.getLogger(__name__)
    logger.info('start data process ...')

    parseCsvFile(csvFileNeedToBeParsed)
