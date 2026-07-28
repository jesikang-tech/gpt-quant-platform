from pathlib import Path

from providers.fdr_provider import FDRProvider
from repository import save_etf_list


class ETFCollector:
    def __init__(self):
        self.provider = FDRProvider()

    def collect(self):
        # ETF 목록 수집
        df = self.provider.get_etf_list()

        # data 폴더가 없으면 생성
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        # CSV 저장
        csv_file = data_dir / "etf_list.csv"
        df.to_csv(
            csv_file,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"ETF 목록이 저장되었습니다: {csv_file}")

        # SQLite 저장
        save_etf_list(df)

        return df