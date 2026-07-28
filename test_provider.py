from providers.fdr_provider import FDRProvider

provider = FDRProvider()

df = provider.get_etf_list()

print(df.head())

print()

print(f"ETF 개수 : {len(df)}")