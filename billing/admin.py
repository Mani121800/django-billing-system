from django.contrib import admin
from .models import Product, Denomination, Bill, BillItem, BillChangeDenomination

admin.site.register(Product)
admin.site.register(Denomination)
admin.site.register(Bill)
admin.site.register(BillItem)
admin.site.register(BillChangeDenomination)
