from repository import save_etf_info



def load_etf_list(
    etf_list
):
    """
    ETF 목록 저장

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



if __name__ == "__main__":


    sample_etfs = [

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


    load_etf_list(
        sample_etfs
    )