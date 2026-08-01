import yfinance as yf


class YahooProvider:
    def download(self, provider_symbol, period="2y", interval="1d"):
        df = yf.download(
            provider_symbol,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=False,
        )

        # Flatten MultiIndex columns
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        return df