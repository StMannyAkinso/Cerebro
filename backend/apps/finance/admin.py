from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "provider",
        "account_type",
        "currency",
        "is_active",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_date",  
        "description", 
        "amount", 
        "account",
    )

    list_filter = (
        "account",
        "source",
    )

    search_fields = (
        "description",
        "reference",
    )