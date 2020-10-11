import pandas as pd
from decimal import Decimal
import datetime
import dateutil.parser
from .models import symbols,prices as prc,clients,BuySell
import pandas_ta as ta
import numpy as np
class technical_pandasta(object):
    symbol=None
    prices=None
    df = None
    columns= None
    indexes=None
    count=None
    BUYPoint = None #Every Indicator 10 points, Support and Resistance every Day One Point, hoghooghi be haghighi 50 point,hajme bishatr az miangin 50 point
    SELLPoint = None
    supports=None
    ressists=None
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.columns= ['open','high','low','adjclose','value','volume','count','close']
        self.indexes=[]
        self.count=0
        self.BUYPoint=0
        self.SELLPoint=0
        self.supports = []
        self.ressists = []
        self.df=[]

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
        # strategy_a = ta.Strategy(name="strategy1",
        #     ta=[
        #         {"kind":"sma", "length": 10},
        #         {"kind":"sma", "length": 20},
        #         {"kind":"ema", "length": 8},
        #         {"kind":"ema", "length": 21},
        #         {"kind":"macd"},
        #         {"kind":"bbands", "length": 20},
        #         {"kind":"rsi"}
        #         ])   
        # self.df.ta.strategy(strategy_a,append=True)
        # np.concatenate((self.df, ta.sma(self.df["close"],length=10)), axis=1)
        # self.df.combine(ta.sma(self.df["close"],length=20,append=True),fill_value=True)
        # self.df.ta.sma(self.df["close"],length=50, append=True,prefix='dsds')
    
    def supportRessists(self):
        
        for index in  range(len(self.indexes)):
            if index<3:
                continue
            if self.supportFinder(index):
                try:
                    self.supports.append(self.df.loc[self.indexes[index]]['close'])
                except:
                    a=''
            if self.ressistFinder(index):
                try:
                    self.ressists.append(self.df.loc[self.indexes[index]]['close'])
                except:
                    a=''
    def supportFinder(self,index):
        try:
            if (#self.df.loc[self.indexes[index-3]]['close']>self.df.loc[self.indexes[index-2]]['close'] and 
                #self.df.loc[self.indexes[index-2]]['close']>self.df.loc[self.indexes[index-1]]['close'] and 
                self.df.loc[self.indexes[index-1]]['close']>self.df.loc[self.indexes[index]]['close'] and
                self.df.loc[self.indexes[index]]['close']<self.df.loc[self.indexes[index+1]]['close'] #and
                #self.df.loc[self.indexes[index+1]]['close']>self.df.loc[self.indexes[index+2]]['close'] and
                #self.df.loc[self.indexes[index+1]]['close']>self.df.loc[self.indexes[index+2]]['close']
            ):
                return True
        except:
            return False
    def ressistFinder(self,index):
        try:
            if (#self.df.loc[self.indexes[index-3]]['close']>self.df.loc[self.indexes[index-2]]['close'] and 
                #self.df.loc[self.indexes[index-2]]['close']>self.df.loc[self.indexes[index-1]]['close'] and 
                self.df.loc[self.indexes[index-1]]['close']<self.df.loc[self.indexes[index]]['close'] and
                self.df.loc[self.indexes[index]]['close']>self.df.loc[self.indexes[index+1]]['close'] #and
                #self.df.loc[self.indexes[index+1]]['close']>self.df.loc[self.indexes[index+2]]['close'] and
                #self.df.loc[self.indexes[index+1]]['close']>self.df.loc[self.indexes[index+2]]['close']
            ):
                return True
        except:
            return False
    def smaSignal(self):
        try:
            Diffrnces = []
            Diffrnces.append( self.indexes[len(self.indexes)-1]) #TODAY
            Diffrnces.append( self.indexes[len(self.indexes)-2]) 
            Diffrnces.append( self.indexes[len(self.indexes)-3]) 
            Diffrnces.append( self.indexes[len(self.indexes)-4]) 
            Diffrnces.append( self.indexes[len(self.indexes)-5]) 
            
        
            #[indicator_bb.size-2] 
            samShort = ta.sma(self.df["close"], length=10)
            samLong = ta.sma(self.df["close"], length=20)
            
            if (samShort[Diffrnces[0]] - samLong[Diffrnces[0]] >0 and samShort[Diffrnces[1]] - samLong[Diffrnces[1]] <=0 and samShort[Diffrnces[2]] - samLong[Diffrnces[2]] <0 and samShort[Diffrnces[3]] - samLong[Diffrnces[3]]<0 and samShort[Diffrnces[4]] - samLong[Diffrnces[4]]<0 ) :
                self.BUYPoint+=10
            elif (samShort[Diffrnces[0]] - samLong[Diffrnces[0]] <=0 and samShort[Diffrnces[1]] - samLong[Diffrnces[1]] >0 ) : 
                self.SELLPoint+=10
            return True
        except:
            return False
    
    def macdSignal(self):
        try:
            macdDiffrnces = []
            macdDiffrnces.append( self.indexes[len(self.indexes)-1]) #TODAY
            macdDiffrnces.append( self.indexes[len(self.indexes)-2]) 
            macdDiffrnces.append( self.indexes[len(self.indexes)-3]) 
            macdDiffrnces.append( self.indexes[len(self.indexes)-4]) 
            macdDiffrnces.append( self.indexes[len(self.indexes)-5]) 
            
        
            #[indicator_bb.size-2] 
            samShort = ta.macd(self.df["close"], length=10)
            samLong = ta.sma(self.df["close"], length=20)
            
            if (samShort[macdDiffrnces[0]] - samLong[macdDiffrnces[0]] >0 and samShort[macdDiffrnces[1]] - samLong[macdDiffrnces[1]] <=0 and samShort[macdDiffrnces[2]] - samLong[macdDiffrnces[2]] <0 and samShort[macdDiffrnces[3]] - samLong[macdDiffrnces[3]]<0 and samShort[macdDiffrnces[4]] - samLong[macdDiffrnces[4]]<0 ) :
                self.BUYPoint+=10
            elif (samShort[macdDiffrnces[0]] - samLong[macdDiffrnces[0]] <=0 and samShort[macdDiffrnces[1]] - samLong[macdDiffrnces[1]] >0 ) : 
                self.SELLPoint+=10
            return True
        except:
            return False    
    
    def rsiSignal(self):
        indicator_rsi = ta.rsi(close=self.df["close"])
        try:
            Diffrnces = []
            Diffrnces.append( self.indexes[len(self.indexes)-1]) #TODAY
            Diffrnces.append( self.indexes[len(self.indexes)-2]) 
            if (indicator_rsi[Diffrnces[0]]>=30 and indicator_rsi[Diffrnces[1]]<=30):
                self.BUYPoint+=10
            elif (indicator_rsi[Diffrnces[1]]>=70 and indicator_rsi[Diffrnces[0]]<=70 ):
                self.SELLPoint+=10
            return True
        except :
            return False

    def cciSignal(self):
        indicator_cci = ta.cci(high=self.df["high"],low=self.df["low"],close=self.df["close"])
        try:
            Diffrnces = []
            Diffrnces.append( self.indexes[len(self.indexes)-1]) #TODAY
            Diffrnces.append( self.indexes[len(self.indexes)-2]) 
            if (indicator_cci[Diffrnces[0]]>=30 and indicator_cci[Diffrnces[1]]<=30):
                self.BUYPoint+=10
            elif (indicator_cci[Diffrnces[1]]>=70 and indicator_cci[Diffrnces[0]]<=70 ):
                self.SELLPoint+=10
            return True
        except :
            return False

    def check(self):
        self.smaSignal()
        self.macdSignal()
        self.rsiSignal()
        #self.cciSignal()
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
    
        

    
