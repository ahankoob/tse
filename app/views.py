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
from .analyze.technical import technical
from .analyze.supports import supports
from .analyze.prepareSymbol import prepareSymbol
from .analyze.clientsType import clientsType
from .classes.symbolPack import symbolPack
import functools
import os
import re
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
def importFastData(request,sid):
    outputStr = ''
    
    outputStr+= functions.importSymbolFastData(sid)
    return HttpResponse(outputStr)
def myTechnical(request,sid):
    symbolObj = symbols.objects.filter(pk = int(sid)).first()
    prepare = prepareSymbol(symbolObj)
    technicalItem = technical(prepare)
    supportlItem = supports(prepare)
    clientsItem = clientsType(prepare)
    
    returnStr=""
    # returnStr = symbolObj.symbolName+":"+str(clientsItem.BUYPoint)
    if(len(technicalItem.BUYPoint)  or len(technicalItem.SELLPoint) or len(supportlItem.BUYPoint) or len(supportlItem.SELLPoint) or len(clientsItem.BUYPoint) or len(clientsItem.SELLPoint)  ):
        returnStr+="<br>{}({}) -><br><pre>\t تحلیل تکنیکال:<br>\t\t خرید:{}<br> \t\t فروش:{} <br> \t حمایت و مقاومت:<br>\t\t خرید:{} <br>\t\t فروش:{} <br> \t اطلاعات خریداران:<br>\t\t خرید:{} <br>\t\t فروش:{}</pre>".format(symbolObj.symbolName,str(symbolObj.pk),str(technicalItem.BUYPoint),str(technicalItem.SELLPoint),str(supportlItem.BUYPoint),str(supportlItem.SELLPoint),str(clientsItem.BUYPoint),str(clientsItem.SELLPoint))
    return HttpResponse(returnStr)
def getHistory(request,sid):
        
    symbolObj = symbols.objects.filter(pk = int(sid)).first()
    smbPack = symbolPack(symbolObj)
    
    return HttpResponse(symbolObj.symbolName+"( "+str(symbolObj.pk)+" ) " +smbPack.get_from_csv())
def symbolsJson(request):
    return HttpResponse(functions.prepareTickersJson(), content_type="application/json")
def symbolsCheckActive(request):
    symbolObj = symbols.objects.all()
    for item in  symbolObj:
        smbPack = symbolPack(item)
        smbPack.checkActive()
    return HttpResponse('Done!')




