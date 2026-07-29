from repository import save_etf_info



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



if __name__ == "__main__":

    etf_list = get_sample_etf_list()


    load_etf_list(
        etf_list
    )