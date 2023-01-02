from django.contrib import admin

# Register your models here.
from bank.models  import bankdetails,transaction
admin.site.register(bankdetails)
admin.site.register(transaction)

