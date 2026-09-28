# Turing machine resembled as a TSV file and it's Python cource code

The required task: https://canvas.uts.edu.au/courses/40908/pages/specification-for-assessment-2?module_item_id=2854879  
TL;DR: Sort a list of 16-byte numbers in hexadecimal.


The Turing machine format: https://canvas.uts.edu.au/courses/40908/pages/turing-machine-specification-format?module_item_id=2800591  
Recap: A row of Turing machine transition consists of 5 sections delimited by the tab character (`\t` in Python):   
**Current state - Current symbol - Next symbol - Next state - Move**  
A Turing machine will have a bunch of those transition lines which (hopefully) covers all the possibilities.


To generate the TSV file, run:  
`python TSVgen.py > turing.tsv`  
(or python3, depends on which one works for you)

## Current state:
- Can compare and swap TWO numbers ONLY.
- The supported input format is HARDCODED to `⊢[number],[number]⊣`
- The tape at the end will always be `⊢[smaller_number],[bigger_number]⊣`
- Guarantees the pointer (or whatever you call it) only moves between the `⊢` and `⊣`
- Currently HARDCODED to support those character: `0123456789abcdef`

TODO:
- Support the correct set of character: `0123456789ABCDEF`
- Handle more numbers 
    - Make the compare/swap operation supports more input format (preferably `[[number],[number]]`)
    - Add "in-between" states and transitions (Suppose it just completed compare/swap 1st and 2nd number, how to make it move to 2nd and 3rd (and so on) number?)
    - Output polishing (likely that the pre-polished output will be riddled with `⊢`, `⊣` and `[]` which is not what the task is looking for)
- Make the code more readable (Add comments or just stop being bad at coding)
- Add the final report