from django.contrib import admin
from billing.models import Transaction, PriceToDays




class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'price', 'transaction_id', 'timestamp', 'startdate', 'enddate', 'description')
    search_fields = ['transaction_id']
    list_filter = ('timestamp', 'price')


class PriceToDaysAdmin(admin.ModelAdmin):
    list_display = ('id','label','cashprice','daystoadd','subplan','discount','active')



admin.site.register(Transaction, TransactionAdmin)
admin.site.register(PriceToDays, PriceToDaysAdmin)

