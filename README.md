# Turing machine resembled as a TSV file and it's Python cource code

The required task: https://canvas.uts.edu.au/courses/40908/pages/specification-for-assessment-2?module_item_id=2854879  
TL;DR: Sort a list of hexadecimal words.

The Turing machine format: https://canvas.uts.edu.au/courses/40908/pages/turing-machine-specification-format?module_item_id=2800591  
Recap: A row of Turing machine transition consists of 5 sections delimited by the tab character (`\t` in Python):   
**Current state - Current symbol - Move - Next symbol - Next state** 
A Turing machine will have a bunch of those transition lines which (hopefully) covers all the possibilities.

## Requirements

Python 3.10 or newer is required.

```bash
python3 -m pip install -r requirements.txt
```

## Generate transition table as TSV
To generate the TSV file, run:  

```bash
python TSVgen.py > turing.tsv
```
(or python3, depends on which one works for you)

Note: In submission, turing.tsv is already generated

## Run and save newly generated test cases
To generate and run the test cases, run:  
```bash
python testgen.py
```

This overwrites the old `test_cases.txt` file. Since the generator uses the fixed seed `36`, the generated test cases remain the same on each fresh run. Then, go into the newly generated file and copy-paste the test case you want to test into the TM simulator, otherwise it already tested for these cases.

(IMPORTANT: Increase the Maximum continuous steps inside the TM Simulator for larger test cases)

Note: test_cases.txt also pre-generated in submission

## Final Update (2/11/2026):
- The machine now passed all the test cases, submission ready.
