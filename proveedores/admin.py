from django.contrib import admin

# Register your models here.
from  .models import Invoice,Customer,Supplier

admin.site.register(Invoice)
admin.site.register(Customer)
admin.site.register(Supplier)
