import numpy as np
from decimal import Decimal
import datetime
import dateutil.parser
from .models import symbols,prices as prc,clients,BuySell
import pandas as pd

class subRes(object):
    supports=None
    ressists = None
    indexes = None
    df= None
    
    symbol=None
    def __init__(self, supports,ressists,indexes,df,symbol):
        self.supports = supports
        self.ressists = ressists
        self.indexes = indexes
        self.df = df
        self.calculate()
        self.ByCurrPrice()
        self.symbol = symbol
    def calculate(self):
        SupportsArr = np.array(self.supports)
        RessistsArr = np.array(self.ressists)

        SupportsArr = np.sort(SupportsArr)
        RessistsArr = np.sort(RessistsArr)

        self.supports = []
        for index1 in range(len(SupportsArr)):
            countIterate=1
            myindex1 = index1
            for index2 in range(myindex1+1,len(SupportsArr),1):
                if abs(SupportsArr[index2]-SupportsArr[myindex1])< self.getVariancedValue(SupportsArr[myindex1]):
                    break
                else:
                    index1=index2+1
                    countIterate+=1
            self.supports.append([SupportsArr[myindex1],countIterate])
        self.ressists = []
        for index1 in range(len(RessistsArr)):
            countIterate=1
            myindex1 = index1
            for index2 in range(myindex1+1,len(RessistsArr),1):
                if abs(RessistsArr[index2]-RessistsArr[myindex1])< self.getVariancedValue(RessistsArr[myindex1]):
                    break
                else:
                    index1=index2+1
                    countIterate+=1
            self.ressists.append([RessistsArr[myindex1],countIterate])
    def ByCurrPrice(self):
        lastSupports = self.supports
        lastRessists = self.ressists
        self.supports = []
        self.ressists = []
        for index in range(len(lastSupports)): #CALC REAL SUPPORT RESSISTANCE
            if self.df.loc[self.indexes[len(self.indexes)-1]]['close']>=lastSupports[index][0]:
                self.supports.append(lastSupports[index])
            elif self.df.loc[self.indexes[len(self.indexes)-1]]['close']<lastSupports[index][0]:
                self.ressists.append(lastSupports[index])
        
        for index in range(len(lastRessists)):#CALC REAL SUPPORT RESSISTANCE
            if self.df.loc[self.indexes[len(self.indexes)-1]]['close']>=lastRessists[index][0]:
                self.supports.append(lastRessists[index])
            elif self.df.loc[self.indexes[len(self.indexes)-1]]['close']<lastRessists[index][0]:
                self.ressists.append(lastRessists[index])
        
        # lastSupports = self.supports
        # lastRessists = self.ressists
        # self.supports = []
        # self.ressists = []

        # while len(lastSupports)>0:
        #     item = lastSupports[0]
        #     lastSupports.remove(lastSupports[0])
        #     removeableIndexes = []
        #     for index in range(len(lastSupports)):
        #         if abs(item[0]-lastSupports[index][0])< self.getVariancedValue(item[0]):
        #             removeableIndexes.append(index)
        #     for index in  range(len(removeableIndexes)-1,0,-1):
        #        item[1]+=lastSupports[index][1]
        #        lastSupports.remove(lastSupports[index])
        #     self.supports.append(item)
        
        # while len(lastRessists)>0:
        #     item = lastRessists[0]
        #     lastRessists.remove(lastRessists[0])
        #     removeableIndexes = []
        #     for index in range(len(lastRessists)):
        #         if abs(item[0]-lastRessists[index][0])< self.getVariancedValue(item[0]):
        #             removeableIndexes.append(index)
        #     for index in  range(len(removeableIndexes)-1,0,-1):
        #        item[1]+=lastRessists[index][1]
        #        lastRessists.remove(lastRessists[index])
        #     self.ressists.append(item)
        

        self.supports = sorted(self.supports,key=lambda x: x[0])
        self.ressists = sorted(self.ressists,key=lambda x: x[0])
    def BuySignal(self):
        try:
            lastPrice = self.df.loc[self.indexes[len(self.indexes)-1]]['close']
            lastSupport = self.supports[len(self.supports)-1]
            firstResistance = self.ressists[0]
            if (abs(lastPrice-lastSupport[0])<self.getVariancedValue(lastPrice) and 
                lastSupport[1]>1 and
                abs(lastPrice-firstResistance[0])>self.getPercent(lastPrice,10)):
                return True
            return False
        except:
            return False
    
    def SellSignal(self):
        try:
            lastPrice = self.df.loc[self.indexes[len(self.indexes)-1]]['close']
            lastSupport = self.supports[len(self.supports)-1]
            firstResistance = self.ressists[0]
            if (abs(lastPrice-firstResistance[0])<self.getVariancedValue(lastPrice)):
                return True
            return False
        except:
            return False

    def persiodMax(self,month):
        
        date_min = datetime.datetime.combine(datetime.datetime.now() - datetime.timedelta(days=month*30), datetime.time.min)
        date_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        self.prices = prc.objects.filter(symbol_id=self.symbol.pk,priceDate__range=(date_min, date_max)) 

    def getVariancedValue(self,value:Decimal)-> Decimal:
        return value*5/100
    def getPercent(self,value:Decimal,percent)-> Decimal:
        return value*percent/100
    def findInIndexes(self,obj):
        for index in self.indexes:
            if index==obj:
                return True
        return False