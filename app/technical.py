import pandas as pd
from decimal import Decimal
import datetime
import dateutil.parser
from .models import symbols,prices as prc,clients,BuySell
from ta import add_all_ta_features
from ta.utils import dropna
import ta.trend,ta.momentum
class technical(object):
    symbol=None
    prices=None
    df = None
    columns= None
    indexes=None
    count=None

    BUYPoint = None #Every Indicator 10 points, Support and Resistance every Day One Point, hoghooghi be haghighi 50 point,hajme bishatr az miangin 50 point
    SELLPoint = None

    
    def __init__(self, symbol):
        self.symbol = symbol
        self.columns= ['open','high','low','adjclose','value','volume','count','close']
        self.indexes=[]
        self.count=0
        self.BUYPoint=0
        self.SELLPoint=0

    
    def dataRead(self):
        date_min = datetime.datetime.combine(datetime.datetime.now() - datetime.timedelta(days=365), datetime.time.min)
        date_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        self.prices = prc.objects.filter(symbol_id=self.symbol.pk,priceDate__range=(date_min, date_max))
        for item in self.prices:
            if self.findInIndexes(self.dateFormat(item.priceDate))==False:
                self.indexes.append(self.dateFormat(item.priceDate))
        
        self.df = pd.DataFrame(columns=self.columns, index=self.indexes)
        
        for dateIndex in self.indexes:  
            today_min = self.dateToObjMin(dateIndex)
            today_max = self.dateToObjMax(dateIndex)
            self.prices = prc.objects.filter(symbol_id=self.symbol.pk,priceDate__range=(today_min, today_max)).last()
            self.df.loc[dateIndex] = pd.Series({'open':self.prices.open, 'high':self.prices.hight, 'low':self.prices.low, 'adjclose':self.prices.adjClose,'value':self.prices.value, 'volume':self.prices.volume, 'count':self.prices.count, 'close':self.prices.close})  
            self.count+=1

    def macdSignal(self):
        df = dropna(self.df)
        try:
            macdDiffrnces = []
            macdDiffrnces.append( self.indexes[len(self.indexes)-1]) #TODAY
            macdDiffrnces.append( self.indexes[len(self.indexes)-2]) 
            macdDiffrnces.append( self.indexes[len(self.indexes)-3]) 
            macdDiffrnces.append( self.indexes[len(self.indexes)-4]) 
            macdDiffrnces.append( self.indexes[len(self.indexes)-5]) 
            

            #[indicator_bb.size-2] 
            MacD = ta.trend.macd(close=df["close"],n_slow=26, n_fast=12)
            MacDSignal = ta.trend.macd_signal(close=df["close"],n_slow=26, n_fast=12,n_sign=9)
            
            if (MacD[macdDiffrnces[0]] - MacDSignal[macdDiffrnces[0]] >0 and MacD[macdDiffrnces[1]] - MacDSignal[macdDiffrnces[1]] <=0 and MacD[macdDiffrnces[2]] - MacDSignal[macdDiffrnces[2]] <0 and MacD[macdDiffrnces[3]] - MacDSignal[macdDiffrnces[3]]<0 and MacD[macdDiffrnces[4]] - MacDSignal[macdDiffrnces[4]]<0 ) :
                self.BUYPoint+=10
            elif (MacD[macdDiffrnces[0]] - MacDSignal[macdDiffrnces[0]] <=0 and MacD[macdDiffrnces[1]] - MacDSignal[macdDiffrnces[1]] >0 ) : 
                self.SELLPoint+=10
            return True
        except:
            return False
    
    def rsiSignal(self):
        df = dropna(self.df)
        indicator_rsi = ta.momentum.rsi(close=df["close"],n=14)
        try:
            Diffrnces = []
            Diffrnces.append( self.indexes[len(self.indexes)-1]) #TODAY
            Diffrnces.append( self.indexes[len(self.indexes)-2]) 
            if (Decimal(indicator_rsi[Diffrnces[0]])<=30 and Decimal(indicator_rsi[Diffrnces[1]])<=30):
                self.BUYPoint+=10
            elif (Decimal(indicator_rsi[Diffrnces[0]])>=70 ):
                self.SELLPoint+=10
            return True
        except :
            return False

    def cciSignal(self):
        df = dropna(self.df)
        try:
        
            indicator_cci = ta.trend.CCIIndicator(high=df["high"],low=df["low"],close=df["close"])
        
            Diffrnces = []
            Diffrnces.append( self.indexes[len(self.indexes)-1]) #TODAY
            Diffrnces.append( self.indexes[len(self.indexes)-2]) 
            if (indicator_cci[Diffrnces[0]<=-100.0] and indicator_cci[Diffrnces[1]<=-100.0]):
                self.BUYPoint+=10
            elif (indicator_cci[Diffrnces[0]>=100] ):
                self.SELLPoint+=10
            return True
        except :
            return False


    def check(self):
        self.macdSignal()
        self.rsiSignal()
        self.cciSignal()
    def findInIndexes(self,obj):
        for index in self.indexes:
            if index==obj:
                return True
        return False
    
    def dateFormat(self,myDate:datetime):
        return "{:04}-{:02}-{:02}".format(myDate.year,myDate.month,myDate.day)
    def dateToObjMin(self,myDate:str):
        return dateutil.parser.parse(myDate+" 00:00:00")
    def dateToObjMax(self,myDate:str):
        return dateutil.parser.parse(myDate+" 23:59:00")
    
        

    
