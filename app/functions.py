from decimal import Decimal
import datetime
import dateutil.parser
import pytz
from django.http import HttpResponse
import json 
import os
import pandas as pd
#from ta import add_all_ta_features
#from ta.utils import dropna
from .models import prices,BuySell,symbols,clients,symbols_info
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import re
import ast
def dateFromStr(dateStr,timeStr,pricesCells):
    dateStrYear = dateStr[0:4]
    dateStrMonth = dateStr[4:6]
    dateStrDay = dateStr[6:8]

    timeStrHour = timeStr[0:2]
    timeStrMin = timeStr[2:4]
    timeStrSec = timeStr[4:6]
    try:
        myDateStr = dateStrYear+"-"+dateStrMonth+"-"+dateStrDay+" "+timeStr+" +0430"
        myDate = dateutil.parser.parse(myDateStr)
    except:
        myDateStr = dateStrYear+"-"+dateStrMonth+"-"+dateStrDay+" "+pricesCells[0]+" +0430"
        myDate = dateutil.parser.parse(myDateStr)
    return myDate
def importSymbolFastDataPrice(symbol,dataUpperCells,returnText):
    try:
        pricesCells = dataUpperCells[0].split(',')
        timeStr=''
        try:
            timeStr=((dataUpperCells[1].split(','))[0].split(' '))[1]
        except:
            timeStr=(dataUpperCells[0].split(','))[0]
        symbolLastPriceList = (prices.objects.filter(symbol_id=symbol.pk))
        if symbolLastPriceList.count()==0:
            symbolPrice = prices(symbol_id=symbol,
            priceDate=dateFromStr(pricesCells[12],timeStr,pricesCells),
            open=Decimal(pricesCells[4]),
            hight=Decimal(pricesCells[6]),
            low=Decimal(pricesCells[7]),
            adjClose=Decimal(pricesCells[3]),
            value=Decimal(pricesCells[10]),
            volume=Decimal(pricesCells[9]),
            count=Decimal(pricesCells[8]),
            close=Decimal(pricesCells[2]))
            symbolPrice.pk=None
            symbolPrice.save()
        else:
            symbolLastPrice = symbolLastPriceList[symbolLastPriceList.count()-1]
            symbolPrice = prices(symbol_id=symbol,
            priceDate=dateFromStr(pricesCells[12],timeStr,pricesCells),
            open=Decimal(pricesCells[4]),
            hight=Decimal(pricesCells[6]),
            low=Decimal(pricesCells[7]),
            adjClose=Decimal(pricesCells[3]),
            value=Decimal(pricesCells[10]),
            volume=Decimal(pricesCells[9]),
            count=Decimal(pricesCells[8]),
            close=Decimal(pricesCells[2]))
            symbolPrice.pk=None

            if symbolLastPrice.priceDate<symbolPrice.priceDate:
                symbolPrice.save()
                returnText[0] += " Price Save OK"
            else:
                symbolPrice = None
                returnText[0] += " Price Save Duplicated"


        return dateFromStr(pricesCells[12],pricesCells[13],pricesCells)
    except Exception:
        returnText[0] += " Price Save Error"

    #     return None
def importSymbolFastDataBuySell(symbol,dataUpperCells,PriceDate,returnText):
    try:
        BuySellListCells = dataUpperCells[2].split(',')
        BuySell.objects.filter(symbol_id=symbol.pk).delete()
        for item in BuySellListCells:
            BuySellCellItems = item.split('@')
            for  BuySellCellItem in BuySellCellItems:
                try:
                    my_BuySell = BuySell('',symbol.pk,PriceDate,BuySellCellItem[0],BuySellCellItem[1],BuySellCellItem[2],BuySellCellItem[3],BuySellCellItem[4],BuySellCellItem[5])
                    my_BuySell.pk = None
                    my_BuySell.save()
                except:
                    continue
        returnText[0] += " BuySell Save OK"

        return True
    except Exception:
        returnText[0] += " BuySell Save Error ({})".format(str(BuySellListCells))

    #     return None
def importSymbolFastDataClients(symbol,dataUpperCells,PriceDate,returnText):
    try:
        clientTypeListCells = dataUpperCells[4].split(',')
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        clients.objects.filter(symbol_id=symbol.pk,date__range=(today_min, today_max)).delete()

        symbolClients = clients('',symbol.pk,PriceDate,clientTypeListCells[0],clientTypeListCells[1],clientTypeListCells[3],clientTypeListCells[4],clientTypeListCells[5],clientTypeListCells[6],clientTypeListCells[8],clientTypeListCells[9])
        symbolClients.pk = None
        symbolClients.save()
        returnText[0] += " Clients Save Ok"

        return True
    except Exception:
        returnText[0] += " Clients Save Error({})".format(str(clientTypeListCells))

    #     return None
def importSymbolFastData(sid):
    returnText=[""]
    try:
        symbol = symbols.objects.filter(pk = int(sid)).first()
        fastUrl = 'http://www.tsetmc.com/tsev2/data/instinfofast.aspx?i={}&c=57+'.format(symbol.symbolID)
        response = ticker_page_response(fastUrl)
        responseText=response.text.replace('b\'','').replace('b"','')
        dataUpperCells = responseText.split(';')
        symbolUrl = "http://tsetmc.com/Loader.aspx?ParTree=151311&i={}".format(symbol.symbolID)
        returnTseSiteInfo = ticker_page_response(symbolUrl)
        pricesCells = dataUpperCells[0].split(',')
        adjClose = Decimal(pricesCells[3])
        # Foundamental
        try:
            eps=0
            TWOPLACES = Decimal('0.01')
            eps = Decimal(getReValue("EstimatedEPS",returnTseSiteInfo)).quantize(TWOPLACES)
            pe=0
            pe=Decimal(str(adjClose/eps)).quantize(TWOPLACES)
            symbolInfo = symbols_info(
                symbol_id=symbol,
                date = datetime.datetime.now(),
                groupName =re.findall(r"LSecVal='([\D]*)',", returnTseSiteInfo.text)[0],
                baseVol=re.findall(r"BaseVol=([\d]*),", returnTseSiteInfo.text)[0]+".00",
                eps=eps,
                sahamCount=re.findall(r"ZTitad=([\d]*),", returnTseSiteInfo.text)[0]+".00",
                minValidPrice=getReValue("PSGelStaMin",returnTseSiteInfo),
                maxValidPrice=getReValue("PSGelStaMax",returnTseSiteInfo),
                MinWeek=getReValue("MinWeek",returnTseSiteInfo),
                MaxWeek=getReValue("MaxWeek",returnTseSiteInfo),
                MinYear=getReValue("MinYear",returnTseSiteInfo),
                MaxYear=getReValue("MaxYear",returnTseSiteInfo),
                monthlyAvgVol=getReValue("QTotTran5JAvg",returnTseSiteInfo),
                group_pe=getReValue("SectorPE",returnTseSiteInfo),
                pe=pe,
                shenavar=int(getReValue("KAjCapValCpsIdx",returnTseSiteInfo))
                )
            symbolInfo.save()
            returnText[0] += " Foundamental Save Ok"
        except:
            returnText[0] += " Foundamental Error"
    
        # Online Price Info
        PriceDate = importSymbolFastDataPrice(symbol,dataUpperCells,returnText)
        if PriceDate!=None:
            importSymbolFastDataBuySell(symbol,dataUpperCells,PriceDate,returnText)
            importSymbolFastDataClients(symbol,dataUpperCells,PriceDate,returnText)
        return symbol.symbolName+" Ok "+returnText[0]+"</br>"
    except:
        return symbol.symbolName+" Error "+returnText+"</br>"
def prepareTickers():
    from bs4 import BeautifulSoup     
    url = "http://www.tsetmc.com/Loader.aspx?ParTree=111C1417"
    r = requests.get(url)
    data = r.content
    soup = BeautifulSoup(data, "html5lib")

    table=soup.find_all('table')[0]
    rows=table.find_all('tr')[1:]

    data = []
    #     'Code' : [],
    #     'group' : [],
    #     'sanat' : [],
    #     'tablo' : [],
    #     'namadEng' : [],
    #     'nameLatin' : [],
    #     'namad' : [],
    #     'name' : [],
    #     'id' : [],
    # }

    for index in range(len(rows)):
        cols = rows[index].find_all('td')
        anchor = cols[7].find('a')
        data.append({'Code':cols[0].get_text(),'group':cols[1].get_text(),'sanat':cols[2].get_text(),'tablo':cols[3].get_text(),'namadEng':cols[4].get_text(),'nameLatin':cols[5].get_text(),'namad':cols[6].get_text(),'name':cols[7].get_text(),'id':(((anchor['href'].split('&'))[1].split('='))[1])})
    htmlRes=''
    JSONSTR = {}

    for row in data:
        # if symbols.objects.filter(symbolID=row['id']).count()==0:
        newSymbol = symbols(symbolName=to_arabic(row['namad']),symbolID=row['id'],symbolActive=True)
        newSymbol.pk=None
        newSymbol.save()
        htmlRes+=newSymbol.symbolName+' Added <br>'
    #     JSONSTR.update({
    #         row['namad']: row['id'],
    #     })
        
    # with open('data.txt', 'w', encoding='utf-8') as outfile:
    #     json.dump(JSONSTR, outfile, ensure_ascii=False)
    return htmlRes

def prepareTickersJson():
    symbolObj = symbols.objects.filter(symbolActive = True)
    data = {}
    for item in  symbolObj:
        data[item.symbolName]=item.symbolID
    return json.dumps(data, ensure_ascii=False)
def to_arabic(string: str):
        return string.replace('ک', 'ك').replace('ی', 'ي').replace('ی','ي').strip() 
def requests_retry_session(
        retries=10,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504, 503),
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
def ticker_page_response(url):
    return requests_retry_session().get(url, timeout=10)
def getReValue(val,returnTseSiteInfo):
    return re.findall(r""+val+"='[0-9,.]*',", returnTseSiteInfo.text)[0].replace(""+val+"='",'').replace("',",'')