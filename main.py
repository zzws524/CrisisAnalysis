import os
import logging
from ziwenLog import myLogConfig

#######Configuration items are here############
csvFileNeedToBeParsed='./Tables/ds07-Table 1.csv'
lostRatio=0.8
crisisThreshold=0.05
firstCrisisCountry=['AN']
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

    logger.info('Parse all rows.')
    dataRowDict={};
    for i in range(1,totalRowCnt): #i is the row number -1
        tmpDict={}
        tmpDict['country']=myLines[i].strip().split(',')[0]
        tmpDataList=[]
        for j in range(1,len(myLines[i].strip().split(','))):
            tmpDataList.append(int(myLines[i].strip().split(',')[j]))
        tmpDict['data']=tmpDataList
        dataRowDict[i+1]=tmpDict  #dataRowDict[2]->{'country':'AD','data':[0,0,...]}

    logger.info('Parse all columns')
    dataColDict={};
    for i in range(1,totalColCnt): #i is the col number -1
        tmpDict={}
        tmpDict['country']=myLines[0].strip().split(',')[i]
        tmpDataList=[]
        for j in range(2,totalColCnt+1):
            tmpDataList.append(dataRowDict[j]['data'][i-1])
        tmpDict['data']=tmpDataList
        dataColDict[i+1]=tmpDict #dataColDict[3]->{'country':'AE','data':[0,0,...]}

    for i in range(2,totalColCnt+1):
        if dataRowDict[i]['country'] != dataColDict[i]['country']:
            logger.error('Check col country vs. row country in matrix.')
            logger.error('col %s is not match with row %s'%(str(i),str(i)))
            os._exit(1)

    return(dataRowDict,dataColDict)





def analyzeAffectedCountry(roundNum,thisRoundCrisisCountries,lastRoundAffectedCountries,dataRowDict,dataColDict):
    logger.info('This is %s round crisis simulation'%str(roundNum))

    #calculate loss first
    nextRoundCrisisCountries=[]
    totalLossForAllNewCrisisCountries=[]
    for newCrisis in thisRoundCrisisCountries:
        logger.debug('Now crisis would hit %s'%newCrisis)
        for colNum in range(2,len(dataColDict.keys())+2):
            if dataColDict[colNum]['country']==newCrisis:
                logger.debug("Find country %s in col %s"%(newCrisis,colNum))
                tmpOneColLoss=[round(x*lostRatio,2) for x in dataColDict[colNum]['data']]
                logger.debug('Loss for country %s (one column * lossRation) is:'%newCrisis)
                logger.debug(tmpOneColLoss)
                if len(totalLossForAllNewCrisisCountries)==0:
                    totalLossForAllNewCrisisCountries=tmpOneColLoss
                else:
                    totalLossForAllNewCrisisCountries=[round(x+y,2) for x,y in zip(totalLossForAllNewCrisisCountries, tmpOneColLoss)]
    logger.debug('Total loss for all latest countries in crisis is:')
    logger.debug(totalLossForAllNewCrisisCountries)

    #check threshold for all other contries,exclude lastRoundAffactedCountries
    for rowNum in range(2,len(dataRowDict.keys())+2):
        if dataRowDict[rowNum]['country'] not in lastRoundAffectedCountries:
            tmpRowThreshold=round(sum(dataRowDict[rowNum]['data'])*crisisThreshold,2)
            if totalLossForAllNewCrisisCountries[rowNum-2]>tmpRowThreshold:
                logger.debug('Another country was impacted (row %s):%s'%(str(rowNum),dataRowDict[rowNum]['country']))
                logger.debug('Lost %s is greater than %s'%(str(totalLossForAllNewCrisisCountries[rowNum-2]),str(tmpRowThreshold)))
                nextRoundCrisisCountries.append(dataRowDict[rowNum]['country'])

    #summary for this round
    logger.info('Summary of round %s :'%roundNum)
    if len(nextRoundCrisisCountries)>0:
        logger.info('After this round, %s was/were impacted'%nextRoundCrisisCountries)


    return nextRoundCrisisCountries




if __name__=='__main__':
    myLog=myLogConfig.ConfigMyLog(logFileName='DataProcess',withFolder=False,consoleLevel=logging.INFO,logLevel=logging.DEBUG)
    logger=logging.getLogger(__name__)
    logger.info('start data process ...')


    (dataRowDict,dataColDict)=parseCsvFile(csvFileNeedToBeParsed)

    allAffectedCountriesFromPreviousRounds=firstCrisisCountry;
    nextRoundCrisisCountries=firstCrisisCountry;
    for i in range(1,4):
        thisRoundCrisisCountries=nextRoundCrisisCountries
        nextRoundCrisisCountries=analyzeAffectedCountry(i,thisRoundCrisisCountries,allAffectedCountriesFromPreviousRounds,dataRowDict,dataColDict)
        allAffectedCountriesFromPreviousRounds.append(thisRoundCrisisCountries)
        if len(nextRoundCrisisCountries)==0:
            logger.info('No more countries were impacted any more.So stop...')
            break







