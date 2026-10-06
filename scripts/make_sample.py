import json

data = json.load(open("data/normalized_combined.json"))
sample = data[:500]

with open("data/sample/sample_combined.json", "w") as f:
    json.dump(sample, f, indent=2)

print(f"Saved {len(sample)} sample records")