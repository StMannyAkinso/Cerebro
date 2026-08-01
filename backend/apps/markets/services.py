from django.utils import timezone

from .models import Market, MarketPrice
from .providers import YahooProvider


class MarketUpdateService:

    def __init__(self):
        self.provider = YahooProvider()

    def update_market(self, market):
        print(f"Updating {market.symbol}...")

        df = self.provider.download(market.provider_symbol)

        if df.empty:
            print(f"⚠ No data returned for {market.symbol}")
            return 0

        added = 0

        for timestamp, row in df.iterrows():

            dt = timestamp.to_pydatetime()

            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)

            _, created = MarketPrice.objects.get_or_create(
                market=market,
                timeframe=MarketPrice.Timeframe.D1,
                datetime=dt,
                defaults={
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": int(row["Volume"]) if row["Volume"] else 0,
                },
            )

            if created:
                added += 1

        market.last_synced = timezone.now()
        market.save(update_fields=["last_synced"])

        print(f"✓ {market.symbol}: {added} new candles")

        return added

    def update_all(self):
        total_added = 0

        for market in Market.objects.filter(active=True):
            try:
                total_added += self.update_market(market)
            except Exception as e:
                print(f"❌ {market.symbol}: {e}")

        print(f"\nFinished. {total_added} candles added.")

        return total_added