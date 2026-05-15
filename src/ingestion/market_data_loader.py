from pathlib import Path
import logging
import pandas as pd
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class MarketDataLoader:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load_data(self) -> pd.DataFrame:
        logging.info(f"Loading market data from {self.file_path}")

        df = pd.read_csv(self.file_path)

        df["valuation_date"] = pd.to_datetime(df["valuation_date"])

        self._validate_market_prices(df)
        self._check_stale_prices(df)

        logging.info(f"Loaded {len(df)} market price records")

        return df

    @staticmethod
    def _validate_market_prices(df: pd.DataFrame):
        invalid_prices = df[df["market_price"] <= 0]

        if not invalid_prices.empty:
            logging.warning(
                f"Detected {len(invalid_prices)} invalid market prices"
            )

    @staticmethod
    def _check_stale_prices(df: pd.DataFrame):
        latest_date = df["valuation_date"].max()

        stale_records = df[
            (latest_date - df["valuation_date"]).dt.days > 3
        ]

        if not stale_records.empty:
            logging.warning(
                f"Detected {len(stale_records)} stale pricing records"
            )


if __name__ == "__main__":
    loader = MarketDataLoader(
        "data/raw/market_prices.csv"
    )

    market_df = loader.load_data()

    print(market_df.head())
