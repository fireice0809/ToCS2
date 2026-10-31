# Turing machine resembled as a TSV file and it's Python cource code

The required task: https://canvas.uts.edu.au/courses/40908/pages/specification-for-assessment-2?module_item_id=2854879  
TL;DR: Sort a list of 8-bytes numbers in hexadecimal.

The Turing machine format: https://canvas.uts.edu.au/courses/40908/pages/turing-machine-specification-format?module_item_id=2800591  
Recap: A row of Turing machine transition consists of 5 sections delimited by the tab character (`\t` in Python):   
**Current state - Current symbol - Move - Next symbol - Next state** 
A Turing machine will have a bunch of those transition lines which (hopefully) covers all the possibilities.

## Generate transition table as TSV
To generate the TSV file, run:  
`python TSVgen.py > turing.tsv`  
(or python3, depends on which one works for you)

## Run and save new generated test_case
To generate and run test case (and replace old test case), run:  
`rm -r ./test_case.txt`
`python testgen.py`  
then go into the newly generated file and copy-paste the test case you want to test into the TM simulator 
(IMPORTANT: Increase the Maximum continuous steps inside the TM Simulator for larger test cases)

## Current state (Update 27/10/2026):
- Can fully sort a list of 8-byte numbers 
- Now also have a fully customizable test generator 

## TODO:
- Add the final report