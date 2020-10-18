from django.shortcuts import render
from django.http import HttpResponse
import json 
import os
import pandas as pd
#from ta import add_all_ta_features
#from ta.utils import dropna
from .models import symbols 
from .models import prices
import dateutil.parser
import requests
from . import functions
from .technical import technical
from .technical_pandata import technical_pandasta
from ta import add_all_ta_features
from ta.utils import dropna
import ta.trend
from .supRes import subRes
from .classes.symbolPack import symbolPack
def index(request):
    
        
    return HttpResponse('hi')

def tickersFromJsonFile(request):
    
    DIRNAME = os.path.dirname(__file__)
    errors=""
    with open(DIRNAME +'/static/symbols_name.json',encoding='utf-8') as f:
        tickers = json.load(f)    
        for ticker in tickers:
            #errors+=tickers[ticker]+"<br>"
            
            symbol = symbols('',ticker, tickers[ticker], True)
            symbol.pk = None
            symbol.save();
            
        context = {'tickers': tickers,'errors':errors}
        return render(request,'tcikers.html',context)
def tickersImportFromCsvWithWC(request): 
    from decimal import Decimal
    import csv
    DIRNAME = os.path.dirname(__file__)
    symbols_list = symbols.objects.filter(symbolActive=True)
    responseStr=""
    for item in  symbols_list:
        responseStr+=item.symbolName

        data = {
            "symbols": item.symbolName
            
        }

        URL = 'http://127.0.0.1:8000/app/tickersImportFromCsv/'+str(item.pk)
        #responseStr+= ' %%% '+str(requests.get(URL, data=data).content)+' %%% '
        from decimal import Decimal
        import csv
        symbol = item
        
        try:
            with open(DIRNAME +"/static/tickers_data/"+symbol.symbolName+".csv", "r") as csv_file:
                reader = csv.reader(csv_file)
                for index,row in enumerate(reader,start=0) :
                    if index==0:
                        continue
                    symbol_price = prices(None,symbol.pk, dateutil.parser.parse(row[0]+' 12:30:00 +0430'), Decimal( row[1]), Decimal(row[2]), Decimal(row[3]), Decimal(row[4]), Decimal(row[5]), Decimal(row[6]), Decimal(row[7]), Decimal(row[8]))
                    symbol_price.pk= None;
                    symbol_price.save()
        except:
            responseStr+= 'Error On '
        responseStr+=": Comlete \r\n"
        
    context = { 'text': responseStr}
    return render(request,'tickersExcelReader.html',context)
    #return HttpResponse(responseStr, "{1}")
def tickersImportFromCsv(request,sid):
    from decimal import Decimal
    import csv
    DIRNAME = os.path.dirname(__file__)
    symbol = symbols.objects.get(pk=sid)
    try:
        with open(DIRNAME +"/static/tickers_data/"+symbol.symbolName+".csv", "r") as csv_file:
                reader = csv.reader(csv_file)

                i=0
                for index,row in enumerate(reader,start=0) :
                    if index==0:
                        continue
                    symbol_price = prices(None,symbol.pk, dateutil.parser.parse(row[0]+' 12:30:00 +0430'), Decimal( row[1]), Decimal(row[2]), Decimal(row[3]), Decimal(row[4]), Decimal(row[5]), Decimal(row[6]), Decimal(row[7]), Decimal(row[8]))
                    symbol_price.pk= None;
                    symbol_price.save()

        # locations = Locations.objects.all()
        # serilaizer = LocationSerializers(locations, many=True)
        # return Response(serilaizer.data)
        return HttpResponse('')
    except Exception :
        return HttpResponse('!!!!!!!')
def tickersFromTseSite(request):
    return HttpResponse(functions.prepareTickers())

def importFastData(request):
    symbols_list = symbols.objects.filter(symbolActive=True)
    outputStr = ''
    responseText = {}
    for item in  symbols_list:
        # if(item.symbolName!='فولاد'):
        #     continue
        fastUrl = 'http://www.tsetmc.com/tsev2/data/instinfofast.aspx?i={}&c=57+'.format(item.symbolID)
        data = {}
        responseText.update({str(item.pk):str(requests.get(fastUrl, data=data).content).replace('b\'','').replace('b"','')})
    for id,resItem in responseText.items(): 
            outputStr+= functions.importSymbolFastData(int(id),resItem)
    return HttpResponse(outputStr)

def myTechnical(request):
    symbol_list = symbols.objects.filter(symbolActive=True)
    Technical_list = list()
    for i in symbol_list:
        Technical_list.append(technical_pandasta(i))
    returnStr=""
    index=0
    for technicalItem in Technical_list:
        #try:
        index+=1
        # if index<50:
        #     continue
        # elif index == 100 :
        #     break
        
        


        technicalItem.dataRead()
        technicalItem.supportRessists()
        mySubRes = subRes(technicalItem.supports,technicalItem.ressists,technicalItem.indexes,technicalItem.df,technicalItem.symbol)
        if(mySubRes.BuySignal() or mySubRes.SellSignal()):
            technicalItem.check()
            if technicalItem.BUYPoint>=10:
                returnStr+="{} : {}>>> Curr:{} S:{},R:{}<br>".format(technicalItem.symbol,'BUY',technicalItem.df.loc[technicalItem.indexes[len(technicalItem.indexes)-1]]['close'],mySubRes.supports[0][0],mySubRes.ressists[0][0])
            elif(technicalItem.SELLPoint>=10):
                returnStr+="{} : {}>>> Curr:{} S:{},R:{}<br>".format(technicalItem.symbol,'Sell',technicalItem.df.loc[technicalItem.indexes[len(technicalItem.indexes)-1]]['close'],mySubRes.supports[0][0],mySubRes.ressists[0][0])
        #technicalItem.check()
        # if technicalItem.BUYPoint>0 or technicalItem.SELLPoint>0:
        #     if technicalItem.BUYPoint>=10:
        #         returnStr+="{} : {} <br>".format(technicalItem.symbol,"Buy")
        #     if technicalItem.SELLPoint>=10:
        #         returnStr+="{} : {} <br>".format(technicalItem.symbol,"Sell")
        # returnStr+="{} : {} <br>".format(technicalItem.symbol,technicalItem.df)
        # except:
        #     returnStr+="{} : {} <br>".format(technicalItem.symbol,"Error")
        
    return HttpResponse(returnStr)
 

def getHistory(request,sid):
        
    symbolObj = symbols.objects.filter(pk = int(sid)).first()
    smbPack = symbolPack(symbolObj)
    if smbPack.get_history_from_tse()==True:
        return HttpResponse(f"{symbolObj.symbolName} Get Ok")
    else:
        return HttpResponse(f"{symbolObj.symbolName} Get Error")




