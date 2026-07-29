from repository import save_etf_info
import csv
from pathlib import Path


def load_etf_list(
    etf_list
):
    """
    ETF 목록 DB 저장

    etf_list 형식:

    [
        {
            "ticker": "069500",
            "name": "KODEX 200",
            "market": "KR"
        }
    ]

    """

    for etf in etf_list:

        save_etf_info(
            etf["ticker"],
            etf["name"],
            etf["market"]
        )


    print(
        f"{len(etf_list)} ETFs loaded"
    )



def get_sample_etf_list():
    """
    테스트용 ETF 목록

    추후 실제 ETF 데이터 Loader로 교체
    """

    return [

        {
            "ticker": "069500",
            "name": "KODEX 200",
            "market": "KR"
        },

        {
            "ticker": "102110",
            "name": "TIGER 200",
            "market": "KR"
        },

        {
            "ticker": "148020",
            "name": "KBSTAR 200",
            "market": "KR"
        }

    ]



def get_csv_etf_list(
    filename="etf_data.csv"
):
    """
    CSV 파일에서 ETF 목록 읽기
    """

    etf_list = []


    path = Path(filename)


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(
            file
        )


        for row in reader:

            etf_list.append(
                {
                    "ticker": row["ticker"],
                    "name": row["name"],
                    "market": row["market"]
                }
            )


    return etf_list


if __name__ == "__main__":

    etf_list = get_csv_etf_list()


    load_etf_list(
        etf_list
    )