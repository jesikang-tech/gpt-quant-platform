from ranking_analyzer import analyze_ranking_trend


print("==============================")
print("Ranking Analytics Test")
print("==============================")


result = analyze_ranking_trend("069500")


print(result)


from ranking_analyzer import calculate_rank_direction


print("\n==============================")
print("Ranking Direction Test")
print("==============================")


direction = calculate_rank_direction("069500")


print("Direction :", direction)


from ranking_analyzer import get_ranking_analytics


print("\n==============================")
print("Full Ranking Analytics Test")
print("==============================")


analytics = get_ranking_analytics("069500")


print(analytics)



from ranking_analyzer import calculate_analytics_grade


print("\n==============================")
print("Analytics Grade Test")
print("==============================")


grade = calculate_analytics_grade("069500")


print("Grade :", grade)


from ranking_analyzer import generate_ranking_assessment


print("\n==============================")
print("Ranking Assessment Test")
print("==============================")


assessment = generate_ranking_assessment(
    "069500"
)


print(assessment)