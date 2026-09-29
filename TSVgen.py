import sys
from enum import Enum

import pandas as pd  # to export TSV later


class Move(Enum):
    LEFT = "←"
    RIGHT = "→"
    HALT = "⏹"


class TuringTSV:
    def __init__(self):
        self.df = pd.DataFrame(
            columns=[
                "current_state",
                "current_symbol",
                "next_symbol",
                "next_state",
                "move",
            ]
        )

    def add_rule(self, current_state, current_symbol, move, next_symbol, next_state):
        """add an entry to tsv

        Args:
            current_state (str): current state
            current_symbol (char): current symbol
            move (enum): left, right or halt
            next_symbol (char): write to the tape
            next_state (str): next state
        """
        try:
            move = move.value
        except:  # noqa: E722
            print("Not valid movement")
            sys.exit(1)

        ambigous = (
            (self.df["current_state"] == current_state)
            & (self.df["current_symbol"] == current_symbol)
        ).any()
        if ambigous:
            print(f"WARNING: OVERRIDING RECORD {current_state},{current_symbol}")
            # remove the old record
            self.df = self.df[
                ~(
                    (self.df["current_state"] == current_state)
                    & (self.df["current_symbol"] == current_symbol)
                )
            ].reset_index(drop=True)

        self.df.loc[len(self.df)] = [
            current_state,
            current_symbol,
            next_symbol,
            next_state,
            move,
        ]

    def export_tsv(self):

        print("Exporting...")
        self.df.to_csv("Turing.tsv", sep="\t", index=False)
        print("Done!")


alphabet = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
]
markedAlphabet = [
    ")",
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
]

the_alphabet_pile = ""
for i in range(0, 16):
    the_alphabet_pile += alphabet[i]
    the_alphabet_pile += " "
the_alphabet_pile = the_alphabet_pile[:-1]

the_marked_pile = ""
for i in range(0, 16):
    the_marked_pile += markedAlphabet[i]
    the_marked_pile += " "
the_marked_pile = the_marked_pile[:-1]

the_pile = ""
for i in range(0, 16):
    the_pile += alphabet[i]
    the_pile += " "
    the_pile += markedAlphabet[i]
    the_pile += " "
the_pile = the_pile[:-1]
# start state
print("▶\t⊢\t\tcompare\t→")
# compare part 1 (find the first digit inside 1st number & reaching the comma)
for i in range(0, 16):
    print(
        "compare\t"
        + alphabet[i]
        + "\t"
        + markedAlphabet[i]
        + "\tcompare_"
        + alphabet[i]
        + "\t→"
    )
    print("compare_" + alphabet[i] + "\t,\t\t" + "found_compare_" + alphabet[i] + "\t→")

for i in range(0, 16):
    print("compare_" + alphabet[i] + "\t" + the_alphabet_pile + "\t\t\t→")

print("compare\t" + the_marked_pile + "\t\t\t→")
# equal numbers (restore and done)
print("compare\t,\t\tequal_restore\t←")


print("equal_restore\t" + the_pile + " ,\t\t\t←")
print("equal_restore\t⊢\t\trestore\t→")
# start restoring & halt (for less/equal)
print("restore\t,\t\t\t→")
for i in range(0, 16):
    print(
        "restore\t"
        + alphabet[i]
        + " "
        + markedAlphabet[i]
        + "\t"
        + alphabet[i]
        + "\t\t→"
    )

print("swap_restore\t,\t\t\t→")
for i in range(0, 16):
    print(
        "swap_restore\t"
        + alphabet[i]
        + " "
        + markedAlphabet[i]
        + "\t"
        + alphabet[i]
        + "\t\t→"
    )

print("restore\t⊣\t\t✔\t⏹")
print("swap_restore\t⊣\t\tswap_prep\t←")
print("swap_prep\t" + the_pile + " ,\t\t\t←")
print("swap_prep\t⊢\t\tswap\t→")


# the grand comparison

for i in range(0, 16):
    print("found_compare_" + alphabet[i] + "\t" + the_marked_pile + "\t\t\t→")
    for j in range(0, i):
        print(
            "found_compare_"
            + alphabet[i]
            + "\t"
            + alphabet[j]
            + "\t"
            + markedAlphabet[j]
            + "\tgreater_restore\t←"
        )
    print(
        "found_compare_"
        + alphabet[i]
        + "\t"
        + alphabet[i]
        + "\t"
        + markedAlphabet[i]
        + "\tback\t←"
    )
    for j in range(i + 1, 16):
        print(
            "found_compare_"
            + alphabet[i]
            + "\t"
            + alphabet[j]
            + "\t"
            + markedAlphabet[j]
            + "\tless_restore\t←"
        )

# move back to start
print("less_restore\t" + the_pile + " ,\t\t\t←")
print("less_restore\t⊢\t\trestore\t→")
print("back\t" + the_pile + " ,\t\t\t←")
print("back\t⊢\t\tcompare\t→")
print("greater_restore\t" + the_pile + " ,\t\t\t←")
print("greater_restore\t⊢\t\tswap_restore\t→")

# the swap
print("swap\t⊣\t\tequal_restore\t←")

print("swap\t" + the_marked_pile + " ,\t\t\t→")
for i in range(0, 16):
    print(
        "swap\t"
        + alphabet[i]
        + "\t"
        + markedAlphabet[i]
        + "\tswap_found_"
        + alphabet[i]
        + "\t→"
    )


for i in range(0, 16):
    print("swap_found_" + alphabet[i] + "\t" + the_alphabet_pile + "\t\t\t→")
    print("swap_found_" + alphabet[i] + "\t,\t\tswap_catch_" + alphabet[i] + "\t→")

for i in range(0, 16):
    print("swap_catch_" + alphabet[i] + "\t" + the_marked_pile + "\t\t\t→")
    for j in range(0, 16):
        print(
            "swap_catch_"
            + alphabet[i]
            + "\t"
            + alphabet[j]
            + "\t"
            + markedAlphabet[i]
            + "\t"
            + "swap_mark_"
            + alphabet[j]
            + "\t←"
        )

for i in range(0, 16):
    print("swap_mark_" + alphabet[i] + "\t" + the_marked_pile + "\t\t\t←")
    print("swap_mark_" + alphabet[i] + "\t,\t\tswap_trace_" + alphabet[i] + "\t←")

for i in range(0, 16):
    print("swap_trace_" + alphabet[i] + "\t" + the_alphabet_pile + "\t\t\t←")
    print(
        "swap_trace_"
        + alphabet[i]
        + "\t"
        + the_marked_pile
        + "\t"
        + markedAlphabet[i]
        + "\tswap_prep"
        + "\t←"
    )
