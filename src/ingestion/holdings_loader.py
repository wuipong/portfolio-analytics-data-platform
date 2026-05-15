from pathlib import Path
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

REQUIRED_COLUMNS = [
    "portfolio_id",
    "valuation_date",
    "isin",
    "issuer_name",
    "asset_type",
    "currency",
    "market_value",
    "clean_price",
    "coupon_rate",
    "maturity_date",
    "duration",
    "credit_rating",
    "sector",
    "country"
]


class HoldingsLoader:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load_data(self) -> pd.DataFrame:
        logging.info(f"Loading holdings data from {self.file_path}")

        df = pd.read_csv(self.file_path)

        self._validate_schema(df)
        self._check_duplicates(df)
        self._check_missing_values(df)

        logging.info(f"Loaded {len(df)} holdings records")

        return df

    @staticmethod
    def _validate_schema(df: pd.DataFrame):
        missing_columns = [
            col for col in REQUIRED_COLUMNS if col not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

    @staticmethod
    def _check_duplicates(df: pd.DataFrame):
        duplicate_count = df.duplicated(
            subset=["portfolio_id", "valuation_date", "isin"]
        ).sum()

        if duplicate_count > 0:
            logging.warning(
                f"Detected {duplicate_count} duplicate holdings records"
            )

    @staticmethod
    def _check_missing_values(df: pd.DataFrame):
        critical_columns = [
            "isin",
            "market_value",
            "currency"
        ]

        for column in critical_columns:
            missing_count = df[column].isnull().sum()

            if missing_count > 0:
                logging.warning(
                    f"Column {column} contains {missing_count} missing values"
                )


if __name__ == "__main__":
    loader = HoldingsLoader(
        "data/raw/portfolio_holdings.csv"
    )

    holdings_df = loader.load_data()

    print(holdings_df.head())
