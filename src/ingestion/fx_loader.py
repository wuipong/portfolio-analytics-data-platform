from pathlib import Path
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class FXRatesLoader:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load_data(self) -> pd.DataFrame:
        logging.info(f"Loading FX rates from {self.file_path}")

        df = pd.read_csv(self.file_path)

        self._validate_fx_rates(df)

        logging.info(f"Loaded {len(df)} FX records")

        return df

    @staticmethod
    def _validate_fx_rates(df: pd.DataFrame):
        invalid_rates = df[df["fx_rate"] <= 0]

        if not invalid_rates.empty:
            logging.warning(
                f"Detected {len(invalid_rates)} invalid FX rates"
            )

    @staticmethod
    def convert_to_base_currency(
        holdings_df: pd.DataFrame,
        fx_df: pd.DataFrame,
        reporting_currency: str = "USD"
    ) -> pd.DataFrame:

        fx_filtered = fx_df[
            fx_df["quote_currency"] == reporting_currency
        ]

        merged_df = holdings_df.merge(
            fx_filtered,
            left_on="currency",
            right_on="base_currency",
            how="left"
        )

        merged_df["market_value_reporting_ccy"] = (
            merged_df["market_value"] * merged_df["fx_rate"]
        )

        return merged_df


if __name__ == "__main__":
    fx_loader = FXRatesLoader(
        "data/raw/fx_rates.csv"
    )

    fx_df = fx_loader.load_data()

    print(fx_df.head())
