from django.db import models

class sanats(models.Model):
    name = models.CharField(max_length=50)
    
class symbols(models.Model):
    symbolName = models.CharField(max_length= 50)
    symbolID = models.CharField(max_length= 50)
    symbolActive = models.BooleanField(default=True)
    # sanat = models.OneToOneField(
    #                     sanats, on_delete=models.CASCADE,
    #                     parent_link=True,
    #                     primary_key=False,
    #                     default=0
    #                     )
    def __str__(self):
        return self.symbolName
    
class prices(models.Model):
    symbol_id = models.ForeignKey(symbols, on_delete=models.CASCADE)
    priceDate = models.DateTimeField()
    open = models.DecimalField(max_digits=8, decimal_places=1,default=0)
    hight = models.DecimalField(max_digits=8, decimal_places=1,default=0)
    low = models.DecimalField(max_digits=8, decimal_places=1,default=0)
    adjClose = models.DecimalField(max_digits=8, decimal_places=1,default=0)
    value = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    volume = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    count = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    close = models.DecimalField(max_digits=8, decimal_places=1,default=0)

class clients(models.Model):
    symbol_id = models.ForeignKey(symbols, on_delete=models.CASCADE)
    date = models.DateTimeField()
    haghighiBuyVolume = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    hoghooghiBuyVolume = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    haghighiSellVolume = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    hoghooghiSellVolume = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    haghighiBuyCount = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    hoghooghiBuyCount = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    haghighiSellCount = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    hoghooghiSellCount = models.DecimalField(max_digits=15, decimal_places=0,default=0)

class BuySell(models.Model):
    symbol_id = models.ForeignKey(symbols, on_delete=models.CASCADE)
    date = models.DateTimeField()
    buyCount = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    buyVolue = models.DecimalField(max_digits=8, decimal_places=1,default=0)
    buyPrice = models.DecimalField(max_digits=8, decimal_places=1,default=0)
    sellCount = models.DecimalField(max_digits=15, decimal_places=0,default=0)
    sellVolue = models.DecimalField(max_digits=8, decimal_places=1,default=0)
    sellPrice = models.DecimalField(max_digits=8, decimal_places=1,default=0)

    


    
    
