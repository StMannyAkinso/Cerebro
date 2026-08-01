from django.contrib import admin

from .models import Market, MarketPrice


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "provider_symbol",
        "market_type",
        "active",
    )

    list_filter = (
        "market_type",
        "active",
    )

    search_fields = (
        "symbol",
        "name",
    )


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = (
        "market",
        "timeframe",
        "datetime",
        "close",
    )

    list_filter = (
        "market",
        "timeframe",
    )

    search_fields = (
        "market__symbol",
    )

    ordering = (
        "-datetime",
    )