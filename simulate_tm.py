#!/usr/bin/env python3
"""Validate and execute the assignment's five-column TSV Turing machines."""

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path

INPUT_RE = re.compile(r"\[(?:[0-9A-F]{16}(?:,[0-9A-F]{16})*)?\]\Z")
BLANK, INITIAL, ACCEPT, ERROR = "·", "⎆", "✔", "❗"
LEFT, RIGHT, HALT = "←", "→", "■"


@dataclass(frozen=True)
class Rule:
    move: str
    write: str | None
    next_state: str
    line: int


class TMTester:
    """Load a TSV machine once and reuse it for independent test runs."""

    def __init__(self, machine_path: str | Path):
        self.machine_path = Path(machine_path)
        self.rules = self._load_machine()

    def _load_machine(self) -> dict[tuple[str, str], Rule]:
        source = self.machine_path.read_text(encoding="utf-8-sig")
        if unicodedata.normalize("NFC", source) != source:
            raise ValueError("Machine file is not NFC-normalized")
        rules: dict[tuple[str, str], Rule] = {}
        kinds: dict[str, str] = {}
        if not source:
            raise ValueError("Empty machine file")
        for line_no, line in enumerate(source.splitlines(), start=1):
            cols = line.split("\t")
            if len(cols) != 5:
                raise ValueError(f"Line {line_no}: expected 5 tab-separated columns, found {len(cols)}")
            state, symbols_field, move, write_field, next_state = cols
            if not state or not symbols_field or not next_state:
                raise ValueError(f"Line {line_no}: missing state or current symbol")
            symbols = symbols_field.split(" ")
            if any(len(x) != 1 for x in symbols) or len(set(symbols)) != len(symbols):
                raise ValueError(f"Line {line_no}: current symbols must be distinct single characters")
            if len(write_field) > 1:
                raise ValueError(f"Line {line_no}: next symbol must be one character or empty")
            if move not in (LEFT, RIGHT, HALT):
                raise ValueError(f"Line {line_no}: invalid move {move!r}")
            if state in (ACCEPT, ERROR):
                raise ValueError(f"Line {line_no}: a halting state cannot have outgoing rules")
            if next_state in (INITIAL, ERROR):
                raise ValueError(f"Line {line_no}: cannot transition to {next_state}")
            if move != HALT and next_state == ACCEPT:
                raise ValueError(f"Line {line_no}: accepting state must be reached by halting")
            if move == HALT and next_state == INITIAL:
                raise ValueError(f"Line {line_no}: cannot halt in the initial state")
            kind = "halt" if move == HALT else "continue"
            if next_state in kinds and kinds[next_state] != kind:
                raise ValueError(f"Line {line_no}: state {next_state!r} is both halting and continuing")
            kinds[next_state] = kind
            rule = Rule(move, write_field or None, next_state, line_no)
            for symbol in symbols:
                key = (state, symbol)
                if key in rules:
                    raise ValueError(
                        f"Line {line_no}: overlapping rule for {key!r}; first on line {rules[key].line}"
                    )
                rules[key] = rule
        if not any(state == INITIAL for state, _ in rules):
            raise ValueError("No initial-state rule")
        for state, _ in rules:
            if kinds.get(state) == "halt":
                raise ValueError(f"Halting state {state!r} has outgoing rules")
        return rules

    def run_case(self, tape_input: str, expected: str, step_limit: int) -> dict:
        """Execute one input on a fresh tape and return its result."""
        if not INPUT_RE.fullmatch(tape_input):
            raise ValueError(f"Invalid promised input: {tape_input!r}")
        tape = {i: symbol for i, symbol in enumerate(tape_input)}
        head, state, steps = 0, INITIAL, 0
        history = deque(maxlen=8)
        status = "STEP_LIMIT"
        while steps < step_limit:
            read = tape.get(head, BLANK)
            rule = self.rules.get((state, read))
            if rule is None:
                status = "NO_RULE"
                break
            history.append(f"{steps}: ({state}, {read}, cell {head}) -> line {rule.line}")
            steps += 1  # Count and write happen on every action, even for an unchanged cell.
            written = rule.write if rule.write is not None else read
            if written == BLANK:
                tape.pop(head, None)
            else:
                tape[head] = written
            state = rule.next_state
            if rule.move == HALT:
                status = "HALTED"
                break
            next_head = head + (1 if rule.move == RIGHT else -1)
            if next_head < 0:
                state = ERROR
                status = "LEFT_BOUNDARY_ERROR"
                break
            head = next_head

        final_tape = "".join(tape.get(i, BLANK) for i in range(max(tape, default=-1) + 1))
        if status == "HALTED":
            if state != ACCEPT:
                status = "REJECTED"
            elif head != 0:
                status = "HEAD_NOT_ZERO"
            elif final_tape != expected:
                status = "WRONG_TAPE"
            else:
                status = "PASS"
        return {
            "status": status,
            "steps": steps,
            "writes": steps,
            "head": head,
            "state": state,
            "actual": final_tape,
            "last_actions": " | ".join(history),
        }

    def run_suite(
        self,
        cases_path: str | Path,
        results_path: str | Path = "test_results.csv",
        summary_path: str | Path = "test_summary.json",
        max_steps: int | None = None,
        limit_cases: int | None = None,
    ) -> dict:
        """Run JSONL cases, write the two reports, and return the summary.

        Failed cases are returned in the summary; only the command-line entry
        point turns test failures into a nonzero process exit code.
        """
        cases_path = Path(cases_path)
        results_path = Path(results_path)
        summary_path = Path(summary_path)
        cases = [json.loads(line) for line in cases_path.read_text(encoding="utf-8").splitlines()]
        if limit_cases is not None:
            cases = cases[:limit_cases]
        counts = Counter()
        category_counts = {}
        rows = []
        for case in cases:
            assert case["expected"] == "[" + ",".join(sorted(
                case["input"][1:-1].split(",") if case["n_words"] else []
            )) + "]", f"Incorrect oracle for {case['id']}"
            n = case["n_words"]
            cap = max_steps if max_steps is not None else 20_000 + 1_000 * n * n
            result = self.run_case(case["input"], case["expected"], cap)
            counts[result["status"]] += 1
            cat = category_counts.setdefault(case["category"], Counter())
            cat[result["status"]] += 1
            rows.append({**case, "step_limit": cap, **result})
        fields = ["id", "category", "n_words", "input", "expected", "status", "steps",
                  "writes", "step_limit", "head", "state", "actual", "last_actions"]
        with results_path.open("w", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        summary = {
            "machine": str(self.machine_path),
            "machine_expanded_transitions": len(self.rules),
            "tested": len(rows),
            "status_counts": dict(counts),
            "by_category": {key: dict(value) for key, value in category_counts.items()},
            "first_failures": [
                {k: row[k] for k in ("id", "category", "input", "expected", "status",
                                          "actual", "head", "state", "steps", "last_actions")}
                for row in rows if row["status"] != "PASS"
            ][:12],
        }
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--machine", type=Path, required=True, help="Five-column UTF-8 TSV machine")
    parser.add_argument("--cases", type=Path, default=Path("test_cases_1000.jsonl"))
    parser.add_argument("--results", type=Path, default=Path("test_results.csv"))
    parser.add_argument("--summary", type=Path, default=Path("test_summary.json"))
    parser.add_argument("--max-steps", type=int, help="Override per-case step limit")
    parser.add_argument("--limit-cases", type=int, help="Run the first N cases for a quick check")
    args = parser.parse_args()
    tester = TMTester(args.machine)
    summary = tester.run_suite(
        args.cases,
        results_path=args.results,
        summary_path=args.summary,
        max_steps=args.max_steps,
        limit_cases=args.limit_cases,
    )
    counts = summary["status_counts"]
    print(f"Expanded transitions: {summary['machine_expanded_transitions']}")
    print(f"Cases: {summary['tested']} | " + ", ".join(
        f"{key}: {value}" for key, value in sorted(counts.items())
    ))
    print(f"Results: {args.results} | Summary: {args.summary}")
    if counts.get("PASS", 0) != summary["tested"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
