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
from .models import prices,BuySell,symbols,clients
import requests
def dateFromStr(dateStr,timeStr):
    dateStrYear = dateStr[0:4]
    dateStrMonth = dateStr[4:6]
    dateStrDay = dateStr[6:8]

    # timeStrHour = timeStr[0:2]
    # timeStrMin = timeStr[2:4]
    # timeStrSec = timeStr[4:6]
    myDateStr = dateStrYear+"-"+dateStrMonth+"-"+dateStrDay+" "+timeStr+" +0430"
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
        symbolLastPrice = symbolLastPriceList[symbolLastPriceList.count()-1]
        symbolPrice = prices(symbol_id=symbol,
            priceDate=dateFromStr(pricesCells[12],timeStr),
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


        return dateFromStr(pricesCells[12],pricesCells[13])
    except Exception:
        returnText[0] += " Price Save Error"

        return None
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

        return None
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

        return None

def importSymbolFastData(sid,responseText):
    symbol = symbols.objects.get(pk=sid)
    dataUpperCells = responseText.split(';')
    returnText = [""]

    PriceDate = importSymbolFastDataPrice(symbol,dataUpperCells,returnText)
    if PriceDate!=None:
        importSymbolFastDataBuySell(symbol,dataUpperCells,PriceDate,returnText)
        importSymbolFastDataClients(symbol,dataUpperCells,PriceDate,returnText)
        return symbol.symbolName+" Ok "+returnText[0]+"</br>"
    return symbol.symbolName+" Error "+returnText[0]+"</br>"

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
        if symbols.objects.filter(symbolID=row['id']).count()==0:
            newSymbol = symbols(symbolName=row['namad'],symbolID=row['id'],symbolActive=True)
            newSymbol.pk=None
            newSymbol.save()
            htmlRes+=newSymbol.symbolName+' Added <br>'
    #     JSONSTR.update({
    #         row['namad']: row['id'],
    #     })
        
    # with open('data.txt', 'w', encoding='utf-8') as outfile:
    #     json.dump(JSONSTR, outfile, ensure_ascii=False)
    return htmlRes