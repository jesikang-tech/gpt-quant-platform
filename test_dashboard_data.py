from ranking_analyzer import (
    get_intelligence_dashboard_data
)


print("=" * 50)
print("Dashboard Intelligence Data Test")
print("=" * 50)


data = get_intelligence_dashboard_data()


print()

print(
    "Data Count :",
    len(data)
)


for item in data:

    print()

    print(item)