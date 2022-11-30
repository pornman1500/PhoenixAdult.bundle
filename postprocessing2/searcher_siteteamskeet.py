## Dependencies
import time
import requests
import json
import logging
import enchant
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
## Other .py files
import LoggerFunction

def search(siteName,siteBaseURL,siteSearchURL,searchTitle,searchDate,WorkingDir):
    # Setup Selenium
    opts = Options()
    opts.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    driver = webdriver.Chrome(options=opts)

    ## Basic Log Configuration
    logger = LoggerFunction.setup_logger('Searcher', WorkingDir+'\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', WorkingDir+'\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    ResultsMatrix = [['0','0','0','0','0',0]]
    URL = (siteSearchURL + searchTitle.replace(" ","+") + "&page=0")
    logger.info ("******************** URL used section **********************")
    logger.info (URL)
    driver.get(URL)
    HTMLResponse = html.fromstring(driver.page_source)
    searchResults = HTMLResponse.xpath('//*[@id="root"]/div/div[2]/div[2]/div[2]/div[@class="d-inline p-lg-1 px-3 mb-4 text-white thumbScene"]')
    ScenesQuantity = len(searchResults)
    logger.info("Possible matching scenes found in results: " +str(ScenesQuantity))
    for searchResult in searchResults:
        if searchResult.xpath('.//a[contains(@href, "/movies")]'):
            curID = ''
            curDate = ''
            curSubsite = ''
            curActorstring = ''
            curTitle = searchResult.xpath('.//small[contains(@class, "description")]')[0].text_content().strip().replace(":"," ").replace("?","")
            curDate = datetime.datetime.strptime(str(searchResult.xpath('.//div[@class="sceneDate mt-n1 clearfix"]/small')[0].text_content().strip()),'%m/%d/%Y').strftime('%Y-%m-%d')
            curSubsite = searchResult.xpath('.//div[@class="siteName mr-2 px-2 rounded mb-0"]/small')[0].text_content().strip()
            actorssize = len(searchResult.xpath('.//div[contains(@class, "modelName text-white text-truncate pt-1")]/a'))
            for i in range(actorssize):
                actor = searchResult.xpath('.//div[contains(@class, "modelName text-white text-truncate pt-1")]/a')[i].text_content().strip()
                curActorstring += actor+' & '
            curActorstring = curActorstring[:-3]
            if (searchDate != None):
                curScore = 100 - enchant.utils.levenshtein(searchDate, curDate)
            else:
                curScore = 100 - enchant.utils.levenshtein(searchTitle.lower(), curTitle.lower())
            SceneNameLogger.debug ("************** Current Scene Matching section **************")
            SceneNameLogger.debug ("ID: " +curID)
            SceneNameLogger.debug ("Title: " +curTitle)
            SceneNameLogger.debug ("Date: " +curDate)
            SceneNameLogger.debug ("Actors: " +curActorstring)
            SceneNameLogger.debug ("Subsite: " +curSubsite)
            SceneNameLogger.debug ("Score: " +str(curScore))
            ResultsMatrix.append([curID, curTitle, curDate, curActorstring, curSubsite, curScore])
    ResultsMatrix.sort(key=lambda x:x[5],reverse=True)
    logger.info ("*************** Moving to Renamer Function *****************")
    SceneNameLogger.handlers.pop()
    logger.handlers.pop()
    return ResultsMatrix