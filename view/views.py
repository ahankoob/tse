from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
import json 
import os
from app.models import symbols,prices,clients,BuySell

def index(request):
    symbolList = symbols.objects.filter(symbolActive=True) 
    tickers = []
    for index in range(len(symbolList)):
        tickers.append(symbolList[index].pk)
    context = {'tickers': tickers}
    return render(request,'view/index.html',context)
