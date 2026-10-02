# Turing machine resembled as a TSV file and it's Python cource code

The required task: https://canvas.uts.edu.au/courses/40908/pages/specification-for-assessment-2?module_item_id=2854879  
TL;DR: Sort a list of 16-byte numbers in hexadecimal.


The Turing machine format: https://canvas.uts.edu.au/courses/40908/pages/turing-machine-specification-format?module_item_id=2800591  
Recap: A row of Turing machine transition consists of 5 sections delimited by the tab character (`\t` in Python):   
**Current state - Current symbol - Move - Next symbol - Next state**  (this has been changed compared to the v1 TM simulator)
A Turing machine will have a bunch of those transition lines which (hopefully) covers all the possibilities.


To generate the TSV file, run:  
`python TSVgen.py > turing.tsv`  
(or python3, depends on which one works for you)

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