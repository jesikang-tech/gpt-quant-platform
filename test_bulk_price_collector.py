from collector.bulk_price_collector import BulkPriceCollector


collector = BulkPriceCollector()


collector.collect(
    "2026-01-01",
    "2026-07-28",
    limit=5
)