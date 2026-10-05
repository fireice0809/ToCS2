#!/usr/bin/env python3
"""Create a reproducible, diverse suite of valid hex-list inputs."""

import argparse
import csv
import json
import random
from pathlib import Path

HEX = "0123456789ABCDEF"
MIN_WORD = "0" * 16
MAX_WORD = "F" * 16
DEFAULT_SEED = 20261005
QUOTAS = {
    "empty": 1,
    "single": 40,
    "pair_ordered": 70,
    "pair_reversed": 70,
    "pair_equal": 45,
    "multi_sorted": 100,
    "multi_reversed": 100,
    "multi_random": 300,
    "duplicate_heavy": 120,
    "near_equal": 80,
    "long_list": 74,
}


def word(rng: random.Random) -> str:
    return "".join(rng.choices(HEX, k=16))


def distinct_words(rng: random.Random, count: int) -> list[str]:
    values = set()
    while len(values) < count:
        values.add(word(rng))
    return sorted(values)


def make_words(category: str, rng: random.Random, ordinal: int) -> list[str]:
    if category == "empty":
        return []
    if category == "single":
        return [([MIN_WORD, MAX_WORD, "0123456789ABCDEF"][ordinal]
                 if ordinal < 3 else word(rng))]
    if category == "pair_equal":
        value = MIN_WORD if ordinal == 0 else MAX_WORD if ordinal == 1 else word(rng)
        return [value, value]
    if category.startswith("pair_"):
        if ordinal == 0:
            values = [MIN_WORD, MAX_WORD]
        elif ordinal == 1:
            values = ["9" + "0" * 15, "A" + "0" * 15]
        elif ordinal == 2:
            values = ["0" * 15 + "9", "0" * 15 + "A"]
        else:
            values = distinct_words(rng, 2)
        return sorted(values, reverse=(category == "pair_reversed"))
    if category == "near_equal":
        prefix = "".join(rng.choices(HEX, k=15))
        size = rng.randint(3, 20)
        values = [prefix + rng.choice(HEX) for _ in range(size)]
        if len(set(values)) < 2:
            values[-1] = prefix + HEX[(HEX.index(values[-1][-1]) + 1) % 16]
        rng.shuffle(values)
        return values
    if category == "duplicate_heavy":
        size = rng.randint(3, 24)
        pool = distinct_words(rng, rng.randint(2, min(5, size)))
        values = [rng.choice(pool) for _ in range(size)]
        rng.shuffle(values)
        return values
    if category == "long_list":
        size = [30, 40, 60, 80][ordinal % 4]
        values = [word(rng) for _ in range(size)]
        if ordinal % 3 == 0:
            values.sort(reverse=True)
        return values
    values = distinct_words(rng, rng.randint(3, 20))
    if category == "multi_sorted":
        return sorted(values)
    if category == "multi_reversed":
        return sorted(values, reverse=True)
    if category == "multi_random":
        rng.shuffle(values)
        return values
    raise ValueError(f"Unknown category: {category}")


def generate(seed: int = DEFAULT_SEED) -> list[dict]:
    rng = random.Random(seed)
    cases = []
    seen = set()
    for category, quantity in QUOTAS.items():
        for ordinal in range(quantity):
            for _ in range(1000):
                words = make_words(category, rng, ordinal)
                tape = "[" + ",".join(words) + "]"
                if tape not in seen:
                    break
            else:
                raise RuntimeError(f"Could not find a unique case for {category}")
            seen.add(tape)
            cases.append({
                "id": f"T{len(cases) + 1:04d}",
                "category": category,
                "n_words": len(words),
                "input": tape,
                "expected": "[" + ",".join(sorted(words)) + "]",
            })
    assert len(cases) == 1000 and len(seen) == 1000
    return cases


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("test_cases_1000.jsonl"))
    parser.add_argument("--csv", type=Path, default=Path("test_cases_1000.csv"))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()
    cases = generate(args.seed)
    args.output.write_text(
        "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cases),
        encoding="utf-8",
    )
    with args.csv.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=["id", "category", "n_words", "input", "expected"])
        writer.writeheader()
        writer.writerows(cases)
    print(f"Wrote {len(cases)} distinct cases to {args.output} and {args.csv} (seed={args.seed}).")


if __name__ == "__main__":
    main()
