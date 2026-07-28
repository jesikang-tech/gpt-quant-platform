import pandas as pd

from src.exceptions import ValidationError


class TrendFactor:

    REQUIRED_COLUMNS = [
        "date",
        "close",
        "volume",
    ]

    from src.config import MIN_REQUIRED_ROWS

    ...

    MIN_ROWS = MIN_REQUIRED_ROWS

    def validate(self, df: pd.DataFrame):

        # -------------------------
        # 기본 검사
        # -------------------------
        if not isinstance(df, pd.DataFrame):
            raise ValidationError("Input must be DataFrame")

        if df.empty:
            raise ValidationError("DataFrame is empty")

        missing = [
            col
            for col in self.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValidationError(
                f"Missing columns : {missing}"
            )

        # -------------------------
        # 자동 정리
        # -------------------------
        df = df.copy()

        df["date"] = pd.to_datetime(df["date"])

        df = df.sort_values("date")

        df = df.drop_duplicates(subset="date")

        # -------------------------
        # 품질 검사
        # -------------------------
        if df["close"].isna().any():
            raise ValidationError("close contains NaN")

        if df["volume"].isna().any():
            raise ValidationError("volume contains NaN")

        if (df["close"] <= 0).any():
            raise ValidationError("Invalid close price")

        if (df["volume"] < 0).any():
            raise ValidationError("Invalid volume")

        if len(df) < self.MIN_ROWS:
            raise ValidationError(
                f"Need at least {self.MIN_ROWS} rows"
            )

        return df.reset_index(drop=True)

    def trend_score(self, df):
        pass

    def return_score(self, df):

        df = self.validate(df)

        start_price = df.iloc[0]["close"]
        end_price = df.iloc[-1]["close"]

        total_return = (
            (end_price - start_price)
            / start_price
        ) * 100

        if total_return >= 25:
            return 100

        elif total_return >= 20:
            return 90

        elif total_return >= 15:
            return 80

        elif total_return >= 10:
            return 60

        elif total_return >= 5:
            return 40

        elif total_return >= 0:
            return 20

        return 0

    def slope_score(self, df):
        pass

    def ma_score(self, df):
        pass

    def drawdown_score(self, df):
        pass