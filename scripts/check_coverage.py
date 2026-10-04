import json
from collections import defaultdict

data = json.load(open('data/blinkit_full_run.json'))
print(f'Total records: {len(data)}')

matrix = defaultdict(lambda: defaultdict(int))
all_categories = set()
all_cities = set()

for item in data:
    city = item['city']
    cat = item['searched_category']
    matrix[city][cat] += 1
    all_categories.add(cat)
    all_cities.add(city)

print(f'\nCities found: {sorted(all_cities)}')
print(f'Categories found: {sorted(all_categories)}')

print('\n--- Checking for gaps (category with 0 results in any city) ---')
gaps_found = False
for city in sorted(all_cities):
    for cat in sorted(all_categories):
        count = matrix[city].get(cat, 0)
        if count == 0:
            print(f'  GAP: {city} has ZERO results for "{cat}"')
            gaps_found = True

if not gaps_found:
    print('  None found - every city has at least some results for every category.')

print('\n--- Per-city totals ---')
for city in sorted(all_cities):
    total = sum(matrix[city].values())
    print(f'  {city}: {total} records')