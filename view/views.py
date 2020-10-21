from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
import json 
import os
from app.models import symbols,prices,clients,BuySell

def index(request):
    return HttpResponse("Ok!")
def getHistory(request):
    symbolList = symbols.objects.filter(symbolActive=True) 
    tickers = []
    for index in range(len(symbolList)):
        tickers.append(symbolList[index].pk)
    context = {'tickers': tickers}
    prices.objects.all().delete()
    clients.objects.all().delete()
    return render(request,'view/getHistory.html',context)
def getOnlineRecords(request):
    symbolList = symbols.objects.filter(symbolActive=True) 
    tickers = []
    for index in range(len(symbolList)):
        tickers.append(symbolList[index].pk)
    context = {'tickers': tickers}

    return render(request,'view/getOnlineRecords.html',context)
def technical(request):
    symbolList = symbols.objects.filter(symbolActive=True) 
    tickers = []
    for index in range(len(symbolList)):
        tickers.append(symbolList[index].pk)
    context = {'tickers': tickers}

    return render(request,'view/technical.html',context)
