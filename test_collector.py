from collector.etf_collector import ETFCollector

collector = ETFCollector()

df = collector.collect()

print(df.head())

print()

print(df.columns)

print()

print(len(df))