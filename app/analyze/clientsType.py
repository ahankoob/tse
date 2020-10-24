import pandas as pd
from decimal import Decimal
import datetime
import dateutil.parser
from app.models import symbols,prices as prc,clients,BuySell,symbols_info
import pandas_ta as ta
import numpy as np
from .prepareSymbol import prepareSymbol
class clientsType(object):
    BUYPoint = None 
    SELLPoint = None
    prepare=None
    clientsList = None
    averages = None
    avgVol=None
    baseVol = None
    def __init__(self, prepare:prepareSymbol):
        self.columns= ['open','high','low','adjclose','value','volume','count','close']
        self.BUYPoint=[]
        self.SELLPoint=[]
        self.prepare= prepare
        
        date_min = datetime.datetime.combine(datetime.datetime.now() - datetime.timedelta(days=90), datetime.time.min)
        self.clientsList = pd.DataFrame(list(clients.objects.filter(symbol_id=self.prepare.symbol,date__gte=(date_min)).order_by('date').values()))
        foundamental = pd.DataFrame(list(symbols_info.objects.filter(symbol_id=self.prepare.symbol).values()))
        self.avgVol = foundamental.loc[len(foundamental)-1].monthlyAvgVol
        self.baseVol = foundamental.loc[len(foundamental)-1].baseVol
        self.averages = {   
                'haghighiBuyVolume':0,
                'hoghooghiBuyVolume':0,
                'haghighiSellVolume':0,
                'hoghooghiSellVolume':0,
                'haghighiBuyCount':0,
                'hoghooghiBuyCount':0,
                'haghighiSellCount':0,
                'hoghooghiSellCount':0
                        } 
        if(len(self.clientsList))>=10:
            self.avegaresCalc()
            self.hoghooghi_be_haghighi()
            self.haghighi_be_hoghooghi()
            self.hajm_mashkook_kharid()
            self.hajm_mashkook_foroosh()
    def avegaresCalc(self):
        self.averages['haghighiBuyVolume'] = np.mean( self.clientsList['haghighiBuyVolume'])
        self.averages['hoghooghiBuyVolume'] = np.mean( self.clientsList['hoghooghiBuyVolume'])
        self.averages['haghighiSellVolume'] = np.mean( self.clientsList['haghighiSellVolume'])
        self.averages['hoghooghiSellVolume'] = np.mean( self.clientsList['hoghooghiSellVolume'])
        self.averages['haghighiBuyCount'] = np.mean( self.clientsList['haghighiBuyCount'])
        self.averages['hoghooghiBuyCount'] = np.mean( self.clientsList['hoghooghiBuyCount'])
        self.averages['haghighiSellCount'] = np.mean( self.clientsList['haghighiSellCount'])
        self.averages['hoghooghiSellCount'] = np.mean( self.clientsList['hoghooghiSellCount'])
    def hoghooghi_be_haghighi(self):
        curr = self.clientsList.loc[len(self.clientsList)-1]
        if(
            curr.hoghooghiSellVolume>=self.getPercent(curr.hoghooghiSellVolume+curr.haghighiSellVolume,50) and
            curr.haghighiBuyVolume>=self.getPercent(curr.haghighiBuyVolume+curr.hoghooghiBuyVolume,50) 
            # and 
            # curr.haghighiBuyCount< self.averages['haghighiBuyCount']/10
            ):
            self.BUYPoint.append('حقوقی به حقیقی')
    def haghighi_be_hoghooghi(self):
        curr = self.clientsList.loc[len(self.clientsList)-1]
        if(
            curr.haghighiSellVolume>=self.getPercent(curr.hoghooghiSellVolume+curr.haghighiSellVolume,70) and
            curr.hoghooghiBuyVolume>=self.getPercent(curr.haghighiBuyVolume+curr.hoghooghiBuyVolume,60) and 
            curr.hoghooghiBuyCount< self.averages['hoghooghiBuyCount']/10
            ):
            self.SELLPoint.append('حقیقی به حقوقی')
    def hajm_mashkook_kharid(self):
        curr = self.clientsList.loc[len(self.clientsList)-1]
        if(
            (curr.hoghooghiBuyVolume+curr.haghighiBuyVolume)> (self.baseVol*5)
            ):
            self.BUYPoint.append('حجم خرید مشکوک')
    def hajm_mashkook_foroosh(self):
        curr = self.clientsList.loc[len(self.clientsList)-1]
        if(
            (curr.haghighiSellVolume+curr.haghighiSellVolume)> (self.baseVol*5)
            ):
            self.SELLPoint.append('حجم فروش مشکوک')
    def dateFormat(self,myDate):
        retArr = []
        for item in myDate:
            retArr.append( "{:04}-{:02}-{:02}".format(item.year,item.month,item.day))
        return retArr

    def dateToObj(self,myDate):
        retArr = []
        for item in myDate:
            retArr.append(dateutil.parser.parse(str(item))  )
        return retArr
    def getPercent(self,value:Decimal,percent)-> Decimal:
        return value*percent/100