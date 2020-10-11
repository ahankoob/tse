from django.contrib import admin

from . import models

admin.site.register(models.sanats)
admin.site.register(models.symbols)
admin.site.register(models.prices)
admin.site.register(models.clients)
admin.site.register(models.BuySell)
