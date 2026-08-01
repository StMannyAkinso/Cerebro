from django.db import models

from django.db import models


class Market(models.Model):
    class MarketType(models.TextChoices):
        FOREX = "FOREX", "Forex"
        COMMODITY = "COMMODITY", "Commodity"

    symbol = models.CharField(
        max_length=20,
        unique=True,
        help_text="Internal symbol (e.g. EURUSD, XAUUSD)"
    )

    provider_symbol = models.CharField(
        max_length=30,
        unique=True,
        help_text="Symbol used by the data provider (e.g. EURUSD=X, GC=F)"
    )

    name = models.CharField(
        max_length=100
    )

    market_type = models.CharField(
        max_length=20,
        choices=MarketType.choices
    )

    active = models.BooleanField(
        default=True
    )

    last_synced = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return self.symbol


class MarketPrice(models.Model):
    class Timeframe(models.TextChoices):
        H1 = "1H", "1 Hour"
        H4 = "4H", "4 Hour"
        D1 = "1D", "Daily"

    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE,
        related_name="market_prices"
    )

    timeframe = models.CharField(
        max_length=2,
        choices=Timeframe.choices
    )

    datetime = models.DateTimeField()

    open = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

    high = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

    low = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

    close = models.DecimalField(
        max_digits=20,
        decimal_places=8
    )

    volume = models.BigIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["market", "timeframe", "-datetime"]

        constraints = [
            models.UniqueConstraint(
                fields=["market", "timeframe", "datetime"],
                name="unique_market_price"
            )
        ]

        indexes = [
            models.Index(fields=["market", "timeframe"]),
            models.Index(fields=["datetime"]),
        ]

    def __str__(self):
        return f"{self.market.symbol} ({self.timeframe}) - {self.datetime}"



class Feature(models.Model):
    market_price = models.ForeignKey(
        MarketPrice,
        on_delete=models.CASCADE,
        related_name="features"
    )

    name = models.CharField(max_length=100)

    value = models.FloatField()

    class Meta:
        unique_together = ("market_price", "name")

    def __str__(self):
        return f"{self.market_price.market.symbol} - {self.name}"