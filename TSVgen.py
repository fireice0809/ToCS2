class TSVgen:

    alphabet = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    markedAlphabet = [")", "!", "@", "#", "$", "%", "^", "&", "*", "(", "a", "b", "c", "d", "e", "f"]
    start = ["[", ","]
    end = ["]", ","]
    mid = ","
    movement = ["→", "←", "⏹"]
    special_state = ["▶", "✔"]

    # fixed/changed the transition row format (now it conforms to the task)
    def print_state(self, cur_state: str, cur_symbol: str, move: str, next_symbol: str, next_state: str):
        print(cur_state + "\t" + cur_symbol + "\t" + move + "\t" + next_symbol + "\t" + next_state)

    def genTSV(self):
        # the start state
        self.print_state(self.special_state[0], " ".join(self.start), self.movement[0], "", "compare")

        # find the first unmarked byte of 1st number
        for i in range(0, len(self.alphabet)):
            self.print_state("compare", self.alphabet[i], self.movement[0], self.markedAlphabet[i], "compare_" + self.alphabet[i])
        self.print_state("compare", " ".join(self.markedAlphabet), self.movement[0], "", "")
        # 2 numbers are equal if no unmarked byte found
        self.print_state("compare", self.mid, self.movement[1], "", "equal")

        # move to middle comma
        for i in range(0, len(self.alphabet)):
            self.print_state("compare_" + self.alphabet[i], " ".join(self.alphabet), self.movement[0], "", "")
            self.print_state("compare_" + self.alphabet[i], self.mid, self.movement[0], "", "found_compare_" + self.alphabet[i])

        # find the first unmarked byte of 2nd number and give verdict(smaller/greater) if there is one
        for i in range(0, len(self.alphabet)):
            self.print_state("found_compare_" + self.alphabet[i], " ".join(self.markedAlphabet), self.movement[0], "", "")
            for j in range(0, i):
                self.print_state("found_compare_" + self.alphabet[i], self.alphabet[j], self.movement[1], self.markedAlphabet[j], "greater")
            self.print_state("found_compare_" + self.alphabet[i], self.alphabet[i], self.movement[1], self.markedAlphabet[i], "back")
            for j in range(i+1, len(self.alphabet)):
                self.print_state("found_compare_" + self.alphabet[i], self.alphabet[j], self.movement[1], self.markedAlphabet[j], "smaller")

        # if 2 bytes are equal, move completely back to start and try again
        self.print_state("back", self.mid, self.movement[1], "", "back2")
        self.print_state("back", " ".join(self.alphabet + self.markedAlphabet), self.movement[1], "", "")
        self.print_state("back2", " ".join(self.alphabet + self.markedAlphabet), self.movement[1], "", "")
        self.print_state("back2", " ".join(self.start), self.movement[0], "", "compare")

        # if 1st number is smaller, move completely back to start and prepare for restoring
        self.print_state("smaller", self.mid, self.movement[1], "", "smaller2")
        self.print_state("smaller", " ".join(self.markedAlphabet + self.alphabet), self.movement[1], "", "")
        self.print_state("smaller2", " ".join(self.markedAlphabet + self.alphabet), self.movement[1], "", "")
        self.print_state("smaller2", " ".join(self.start), self.movement[0], "", "restore")

        # if 1st number is greater, move completely back to start and prepare for restoring & swapping
        self.print_state("greater", self.mid, self.movement[1], "", "greater2")
        self.print_state("greater", " ".join(self.markedAlphabet + self.alphabet), self.movement[1], "", "")
        self.print_state("greater2", " ".join(self.markedAlphabet + self.alphabet), self.movement[1], "", "")
        self.print_state("greater2", " ".join(self.start), self.movement[0], "", "restore_swap")

        # is 2 numbers are equal, move completely back to start and prepare for restoring 
        self.print_state("equal", " ".join(self.alphabet + self.markedAlphabet), self.movement[1], "", "")
        self.print_state("equal", " ".join(self.start), self.movement[0], "", "restore")    

        # restoring the original input (no swap case)
        for i in range(0, len(self.alphabet)):
            self.print_state("restore", self.markedAlphabet[i], self.movement[0], self.alphabet[i], "")
        self.print_state("restore", " ".join(self.alphabet), self.movement[0], "", "")
        self.print_state("restore", self.mid, self.movement[0], "", "restore2")
        for i in range(0, len(self.alphabet)):
            self.print_state("restore2", self.markedAlphabet[i], self.movement[0], self.alphabet[i], "")
        self.print_state("restore2", " ".join(self.alphabet), self.movement[0], "", "")
        self.print_state("restore2", " ".join(self.end), self.movement[1], "", "end")

        # move pointer back to position 0 (no swap case)
        self.print_state("end", " ".join(self.alphabet), self.movement[1], "", "")
        self.print_state("end", self.mid, self.movement[1], "", "end2")
        self.print_state("end2", " ".join(self.alphabet), self.movement[1], "", "")
        self.print_state("end2", " ".join(self.start), self.movement[2], "", self.special_state[1])

        # restoring the original input (swap case)
        for i in range(0, len(self.alphabet)):
            self.print_state("restore_swap", self.markedAlphabet[i], self.movement[0], self.alphabet[i], "")
        self.print_state("restore_swap", " ".join(self.alphabet), self.movement[0], "", "")
        self.print_state("restore_swap", self.mid, self.movement[0], "", "restore_swap2")
        for i in range(0, len(self.alphabet)):
            self.print_state("restore_swap2", self.markedAlphabet[i], self.movement[0], self.alphabet[i], "")
        self.print_state("restore_swap2", " ".join(self.alphabet), self.movement[0], "", "")
        # exits and accept
        self.print_state("restore_swap2", " ".join(self.end), self.movement[1], "", "swap_prep")

        # move pointer back to position 0 (swap case)
        self.print_state("swap_prep", " ".join(self.alphabet), self.movement[1], "", "")
        self.print_state("swap_prep", self.mid, self.movement[1], "", "swap_prep2")
        self.print_state("swap_prep2", " ".join(self.alphabet), self.movement[1], "", "")
        # init the swap
        self.print_state("swap_prep2", " ".join(self.start), self.movement[0], "", "swap")

        # find the first unmarked byte of 1st number
        for i in range(0, len(self.alphabet)):
            self.print_state("swap", self.alphabet[i], self.movement[0], self.markedAlphabet[i], "swap_" + self.alphabet[i])
        self.print_state("swap", " ".join(self.markedAlphabet), self.movement[0], "", "")
        # if there is no more unmarked bytes, it means that the swap is done and the only thing left is restore the swapped numbers
        self.print_state("swap", self.mid, self.movement[1], "", "smaller2") 

        # move to middle comma
        for i in range(0, len(self.alphabet)):
            self.print_state("swap_" + self.alphabet[i], " ".join(self.alphabet), self.movement[0], "", "")
            self.print_state("swap_" + self.alphabet[i], self.mid, self.movement[0], "", "swap_found_" + self.alphabet[i])

        # find the first unmarked byte of 2nd number
        for i in range(0, len(self.alphabet)):
            self.print_state("swap_found_" + self.alphabet[i], " ".join(self.markedAlphabet), self.movement[0], "", "")
            for j in range(0, len(self.alphabet)):
                self.print_state("swap_found_" + self.alphabet[i], self.alphabet[j], self.movement[1], self.markedAlphabet[i], "swap_replace_" + self.alphabet[j])

        # move back to middle comma
        for i in range(0, len(self.alphabet)):
            self.print_state("swap_replace_" + self.alphabet[i], self.mid, self.movement[1], "", "swap_back_" + self.alphabet[i])
            self.print_state("swap_replace_" + self.alphabet[i], " ".join(self.markedAlphabet), self.movement[1], "", "")
        
        # find the matching byte of 1st number to swap
        for i in range(0, len(self.alphabet)):
            self.print_state("swap_back_" + self.alphabet[i], " ".join(self.alphabet), self.movement[1], "", "")
            self.print_state("swap_back_" + self.alphabet[i], " ".join(self.markedAlphabet), self.movement[1], self.markedAlphabet[i], "swap_back")

        # move back to pos0 and start the swap cycle again
        self.print_state("swap_back", " ".join(self.markedAlphabet), self.movement[1], "", "")
        self.print_state("swap_back", " ".join(self.start), self.movement[0], "", "swap")


if __name__ == "__main__":
    tsv = TSVgen()
    tsv.genTSV()