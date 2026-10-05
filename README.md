# Turing machine resembled as a TSV file and it's Python cource code

The required task: https://canvas.uts.edu.au/courses/40908/pages/specification-for-assessment-2?module_item_id=2854879  
TL;DR: Sort a list of 16-byte numbers in hexadecimal.


The Turing machine format: https://canvas.uts.edu.au/courses/40908/pages/turing-machine-specification-format?module_item_id=2800591  
Recap: A row of Turing machine transition consists of 5 sections delimited by the tab character (`\t` in Python):   
**Current state - Current symbol - Move - Next symbol - Next state**  (this has been changed compared to the v1 TM simulator)
A Turing machine will have a bunch of those transition lines which (hopefully) covers all the possibilities.


`python TSVgen.py` prints the machine's transitions. To save them directly
as a UTF-8 file without shell redirection, run this Python snippet from the
repository folder:

```python
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from TSVgen import TSVgen

output = StringIO()
with redirect_stdout(output):
    TSVgen().genTSV()
Path("turing_generated.tsv").write_text(output.getvalue(), encoding="utf-8")
```

## Testing

Use Python 3.10 or newer; no extra packages are required. Run these commands
from the repository folder:

```bash
python generate_test_cases.py
python simulate_tm.py --machine turing_generated.tsv --cases test_cases_1000.jsonl
```

`generate_test_cases.py` creates 1,000 distinct valid inputs and expected sorted
outputs in `test_cases_1000.jsonl` and `test_cases_1000.csv`, using a fixed seed
for reproducibility. Generate `turing_generated.tsv` using the snippet above.
`simulate_tm.py` executes that machine on each input and checks the complete
final tape, acceptance in `✔`, and head position at cell 0. It writes detailed
results to `test_results.csv` and totals to `test_summary.json`.

Add `--limit-cases 20` to the simulator command for a quick check of the first
20 cases. These commands overwrite their generated output files.

The tester can also be imported and reused from Python:

```python
from simulate_tm import TMTester

tester = TMTester("turing_generated.tsv")
result = tester.run_case("[]", "[]", step_limit=1000)
print(result["status"])  # PASS
summary = tester.run_suite("test_cases_1000.jsonl")
```

`run_case()` returns one result without writing files. `run_suite()` writes
the CSV and JSON reports and returns the summary; their paths can be changed
with `results_path` and `summary_path`. Each case starts on a fresh tape.

## Current state (Update 2/10/2026):
- Now supports the correct character set `0123456789ABCDEF`.
- Can compare and swap TWO numbers ONLY with the smaller/equal number always be the first number in the output
- The supported input format is `[number,number]`, `[number,number,`, `,number,number]` and `,number,number,`.
- Guarantees the pointer only moves between the endpoints and the endpoints symbol will not change.
- The pointer always move back to position 0 before accepts and exit (for future convenience).


## TODO:
- Handle more numbers 
    - Add "in-between" states and transitions (Suppose it just completed compare/swap 1st and 2nd number, how to make it move to 2nd and 3rd (and so on) number?)
    - Output polishing (likely that the pre-polished output will be riddled with `⊢`, `⊣` and `[]` which is not what the task is looking for)
- Make the code more readable (Add comments or just stop being bad at coding)
- Add the final report
