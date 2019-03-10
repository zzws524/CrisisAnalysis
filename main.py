import os
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
    logger.info('Totally %s lines (including title) will be analyzed.'%str(len(myLines)))
    totalRowCnt=len(myLines)

    if ((myLines[0].strip().split(','))[0] != "DS"):
        logger.error('First chars of first line should be DS')
        os._exit(1)

    logger.info('Totall %s countries will be analyzed.'%str(len(myLines[0].strip().split(','))-1))
    totalColCnt=len(myLines[0].strip().split(','))

    dataRowDict={};
    dataColDict={};
    for i in range(1,len(myLines)): #i is the row number -1
        tmpDict={}
        tmpDict['country']=myLines[i].strip().split(',')[0]
        tmpDataList=[]
        for j in range(1,len(myLines[i].strip().split(','))):
            tmpDataList.append(myLines[i].strip().split(',')[j])
        tmpDict['data']=tmpDataList
        dataRowDict[i+1]=tmpDict  #dataRowDict[0]->{'country':'AD','data':[0,0,...]}


if __name__=='__main__':
    myLog=myLogConfig.ConfigMyLog(logFileName='DataProcess',withFolder=False)
    logger=logging.getLogger(__name__)
    logger.info('start data process ...')

    parseCsvFile(csvFileNeedToBeParsed)
