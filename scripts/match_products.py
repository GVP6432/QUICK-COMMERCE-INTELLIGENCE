import json
import re
from collections import defaultdict

def normalize_name(name):
    """Strip marketing suffixes and normalize for fuzzy matching."""
    name = name.lower()
    name = re.sub(r'\|.*$', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'\b(pouch|tetra pack|fresh|pack)\b', '', name)
    name = re.sub(r'[^a-z0-9\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def normalize_size(size):
    """Extract just the number + unit, ignoring 'pack of' wording differences."""
    match = re.search(r'(\d+\.?\d*)\s*(ml|l|kg|g)', size.lower())
    if match:
        return f"{match.group(1)}{match.group(2)}"
    return size.lower().strip()


def build_normalized_dataset():
    blinkit_data = json.load(open("data/blinkit_full_run.json"))
    zepto_data = json.load(open("data/zepto_full_run.json"))
    all_data = blinkit_data + zepto_data

    for item in all_data:
        item["name_key"] = normalize_name(item["name"])
        item["size_key"] = normalize_size(item["size"])

    return all_data


def measure_overlap(data):
    groups = defaultdict(set)
    for item in data:
        key = (item["searched_category"], item["city"], item["name_key"], item["size_key"])
        groups[key].add(item["platform"])

    overlap_counts = defaultdict(int)
    for key, platforms in groups.items():
        overlap_counts[len(platforms)] += 1

    return overlap_counts


if __name__ == "__main__":
    tests = [
        ("Amul Cow Milk", "500 ml"),
        ("Amul Cow Fresh Milk | Pouch", "1 pack (500 ml)"),
        ("Amul Taaza Toned Milk", "500 ml"),
        ("Amul Taaza Toned Fresh Milk | Pouch", "1 pack (500 ml)"),
    ]
    for name, size in tests:
        print(f"{name!r:50} -> name_key={normalize_name(name)!r:30} size_key={normalize_size(size)!r}")

    print("\n--- Measuring real overlap across full dataset ---")
    data = build_normalized_dataset()
    overlap = measure_overlap(data)
    for platform_count, group_count in sorted(overlap.items()):
        print(f"  Matched across {platform_count} platform(s): {group_count} product groups")

    with open("data/normalized_combined.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nSaved normalized dataset: {len(data)} records")