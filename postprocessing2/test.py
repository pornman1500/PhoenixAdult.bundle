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
import os
## Other .py files
import LoggerFunction

def main():
    opts = Options()
    opts.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    driver = webdriver.Chrome(options=opts)


    siteSearchURL = "https://www.teamskeet.com/search?filter="
    searchTitle = "natalie+lust+sexors"
    ResultsMatrix = [['0','0','0','0','0',0]]
    URL = (siteSearchURL + searchTitle.replace(" ","+") + "&page=0")
    print("******************** URL used section **********************")
    print(URL)
    driver.get(URL)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'authority': 'www.teamskeet.com',}
    req = requests.get(URL, headers=headers)
    #HTMLResponse = html.fromstring(str(req.content))
    HTMLResponse = html.fromstring(driver.page_source)
    #searchResults = HTMLResponse.xpath('//div[@class="thumbsHolder elipsTxt"]/div[1]/div[@class="echThumb"]')
    searchResults = HTMLResponse.xpath('//*[@id="root"]/div/div[2]/div[2]/div[2]/div[@class="d-inline p-lg-1 px-3 mb-4 text-white thumbScene"]')
    #html.open_in_browser(HTMLResponse)
    ScenesQuantity = len(searchResults)
    print("Possible matching scenes found in results: " +str(ScenesQuantity))
    for searchResult in searchResults:
        if searchResult.xpath('.//a[contains(@href, "/movies")]'):
            curID = ''
            curDate = ''
            curSubsite = ''
            curActorstring = ''
            curTitle = searchResult.xpath('.//small[contains(@class, "description")]')[0].text_content().strip().replace(":"," ")
            curDate = datetime.datetime.strptime(str(searchResult.xpath('.//div[@class="sceneDate mt-n1 clearfix"]/small')[0].text_content().strip()),'%m/%d/%Y').strftime('%Y-%m-%d')
            curSubsite = searchResult.xpath('.//div[@class="siteName mr-2 px-2 rounded mb-0"]/small')[0].text_content().strip()
            actorssize = len(searchResult.xpath('.//div[contains(@class, "modelName text-white text-truncate pt-1")]/a'))
            for i in range(actorssize):
                actor = searchResult.xpath('.//div[contains(@class, "modelName text-white text-truncate pt-1")]/a')[i].text_content().strip()
                curActorstring += actor+' & '
            curActorstring = curActorstring[:-3]
            # if (searchDate != None):
            #     curScore = 100 - enchant.utils.levenshtein(searchDate, curDate)
            # else:
            #     curScore = 100 - enchant.utils.levenshtein(searchTitle.lower(), curTitle.lower())
            print("************** Current Scene Matching section **************")
            print("ID: " +curID)
            print("Title: " +curTitle)
            print("Date: " +curDate)
            print("Actors: " +curActorstring)
            print("Subsite: " +curSubsite)
            # print("Score: " +str(curScore))
            ResultsMatrix.append([curID, curTitle, curDate, curActorstring, curSubsite])
    #ResultsMatrix.sort(key=lambda x:x[5],reverse=True)
    print("*************** Moving to Renamer Function *****************")
    return ResultsMatrix

if __name__ == "__main__":
    main()