class TSVgen:

    def __init__(self):
        self.alphabet = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        self.markedAlphabet = [")", "!", "@", "#", "$", "%", "^", "&", "*", "(", "a", "b", "c", "d", "e", "f"]
        self.start_compare = ["[", ","]
        self.end_compare = ["]", ","]
        self.START = "["
        self.END = "]"
        self.MID = ","
        self.LEFT = "←"
        self.RIGHT = "→"
        self.HALT = "■"
        # movement = ["→", "←", "⏹"]
        self.special_state = ["⎆", "✔"]
        self.blank = "·"

    # helper function
    def join_list(self, *args):
        all = set()
        for arg in args:
            all.update(arg)
        return list(all)


    # fixed/changed the transition row format (now it conforms to the task)
    def print_state(self, cur_state: str, cur_symbol: str, move: str, next_symbol: str, next_state: str):
        if next_state == "":
            next_state = cur_state
        print(cur_state + "\t" + cur_symbol + "\t" + move + "\t" + next_symbol + "\t" + next_state)

    def genTSV(self):
        # the start state
        self.print_state(self.special_state[0], self.START, self.RIGHT, "", "compare")

        #edge case []
        self.print_state("compare", self.END, self.LEFT, "", "return_base")

        # find the first unmarked byte of 1st number
        for i in range(len(self.alphabet)):
            self.print_state("compare", self.alphabet[i], self.RIGHT, self.markedAlphabet[i], "compare_" + self.alphabet[i])
        self.print_state("compare", " ".join(self.markedAlphabet), self.RIGHT, "", "")
        # 2 numbers are equal if no unmarked byte found
        self.print_state("compare", self.MID, self.LEFT, "", "equal")

        # move to middle comma
        for i in range(len(self.alphabet)):
            self.print_state("compare_" + self.alphabet[i], " ".join(self.alphabet), self.RIGHT, "", "")
            self.print_state("compare_" + self.alphabet[i], self.MID, self.RIGHT, "", "found_compare_" + self.alphabet[i])

            # TODO: if reach to the end ] -> change the the last comma to be ] and then back track implementation
            self.print_state("compare_" + self.alphabet[i], self.END, self.LEFT, "", "backtrack1")

    
        # find the first unmarked byte of 2nd number and give verdict(smaller/greater) if there is one
        for i in range(len(self.alphabet)):
            self.print_state("found_compare_" + self.alphabet[i], " ".join(self.markedAlphabet), self.RIGHT, "", "")
            for j in range(i):
                self.print_state("found_compare_" + self.alphabet[i], self.alphabet[j], self.LEFT, self.markedAlphabet[j], "greater")
            self.print_state("found_compare_" + self.alphabet[i], self.alphabet[i], self.LEFT, self.markedAlphabet[i], "back")
            for j in range(i+1, len(self.alphabet)):
                self.print_state("found_compare_" + self.alphabet[i], self.alphabet[j], self.LEFT, self.markedAlphabet[j], "smaller")

        # if 2 bytes are equal, move completely back to start and try again
        self.print_state("back", self.MID, self.LEFT, "", "back2")
        self.print_state("back", " ".join(self.alphabet + self.markedAlphabet), self.LEFT, "", "")
        self.print_state("back2", " ".join(self.alphabet + self.markedAlphabet), self.LEFT, "", "")
        self.print_state("back2", " ".join(self.start_compare), self.RIGHT, "", "compare")

        # if 1st number is smaller, move completely back to start and prepare for restoring
        self.print_state("smaller", self.MID, self.LEFT, "", "smaller2")
        self.print_state("smaller", " ".join(self.markedAlphabet + self.alphabet), self.LEFT, "", "")
        self.print_state("smaller2", " ".join(self.markedAlphabet + self.alphabet), self.LEFT, "", "")
        self.print_state("smaller2", " ".join(self.start_compare), self.RIGHT, "", "restore")

        # if 1st number is greater, move completely back to start and prepare for restoring & swapping
        self.print_state("greater", self.MID, self.LEFT, "", "greater2")
        self.print_state("greater", " ".join(self.markedAlphabet + self.alphabet), self.LEFT, "", "")
        self.print_state("greater2", " ".join(self.markedAlphabet + self.alphabet), self.LEFT, "", "")
        self.print_state("greater2", " ".join(self.start_compare), self.RIGHT, "", "restore_swap")

        # is 2 numbers are equal, move completely back to start and prepare for restoring 
        self.print_state("equal", " ".join(self.alphabet + self.markedAlphabet), self.LEFT, "", "")
        self.print_state("equal", " ".join(self.start_compare), self.RIGHT, "", "restore")    

        # restoring the original input (no swap case)
        for i in range(len(self.alphabet)):
            self.print_state("restore", self.markedAlphabet[i], self.RIGHT, self.alphabet[i], "")
        self.print_state("restore", " ".join(self.alphabet), self.RIGHT, "", "")
        self.print_state("restore", self.MID, self.RIGHT, "", "restore2")
        for i in range(len(self.alphabet)):
            self.print_state("restore2", self.markedAlphabet[i], self.RIGHT, self.alphabet[i], "")
        self.print_state("restore2", " ".join(self.alphabet), self.RIGHT, "", "")
        self.print_state("restore2", self.MID, self.LEFT, "", "advance")
        self.print_state("restore2", self.END, self.LEFT, "", "backtrack1")

        # TODO: get back to the current number and start to compare again
        
        self.print_state("advance", " ".join(self.alphabet), self.LEFT, "", "advance")
        self.print_state("advance", self.MID, self.RIGHT, "", "compare") # start compare again

        # # move pointer back to position 0 (no swap case)
        # self.print_state("end", " ".join(self.alphabet), self.LEFT, "", "")
        # self.print_state("end", self.MID, self.LEFT, "", "end2")
        # self.print_state("end2", " ".join(self.alphabet), self.LEFT, "", "")
        # self.print_state("end2", " ".join(self.start_compare), self.HALT, "", self.special_state[1])

        # restoring the original input (swap case)
        for i in range(len(self.alphabet)):
            self.print_state("restore_swap", self.markedAlphabet[i], self.RIGHT, self.alphabet[i], "")
        self.print_state("restore_swap", " ".join(self.alphabet), self.RIGHT, "", "")
        self.print_state("restore_swap", self.MID, self.RIGHT, "", "restore_swap2")
        for i in range(len(self.alphabet)):
            self.print_state("restore_swap2", self.markedAlphabet[i], self.RIGHT, self.alphabet[i], "")
        self.print_state("restore_swap2", " ".join(self.alphabet), self.RIGHT, "", "")
        # exits and accept
        self.print_state("restore_swap2", " ".join(self.end_compare), self.LEFT, "", "swap_prep")

        # move pointer back to position 0 (swap case)
        self.print_state("swap_prep", " ".join(self.alphabet), self.LEFT, "", "")
        self.print_state("swap_prep", self.MID, self.LEFT, "", "swap_prep2")
        self.print_state("swap_prep2", " ".join(self.alphabet), self.LEFT, "", "")
        # init the swap
        self.print_state("swap_prep2", " ".join(self.start_compare), self.RIGHT, "", "swap")

        # find the first unmarked byte of 1st number
        for i in range(len(self.alphabet)):
            self.print_state("swap", self.alphabet[i], self.RIGHT, self.markedAlphabet[i], "swap_" + self.alphabet[i])
        self.print_state("swap", " ".join(self.markedAlphabet), self.RIGHT, "", "")
        # if there is no more unmarked bytes, it means that the swap is done and the only thing left is restore the swapped numbers
        self.print_state("swap", self.MID, self.LEFT, "", "smaller2") 

        # move to middle comma
        for i in range(len(self.alphabet)):
            self.print_state("swap_" + self.alphabet[i], " ".join(self.alphabet), self.RIGHT, "", "")
            self.print_state("swap_" + self.alphabet[i], self.MID, self.RIGHT, "", "swap_found_" + self.alphabet[i])

        # find the first unmarked byte of 2nd number
        for i in range(len(self.alphabet)):
            self.print_state("swap_found_" + self.alphabet[i], " ".join(self.markedAlphabet), self.RIGHT, "", "")
            for j in range(len(self.alphabet)):
                self.print_state("swap_found_" + self.alphabet[i], self.alphabet[j], self.LEFT, self.markedAlphabet[i], "swap_replace_" + self.alphabet[j])

        # move back to middle comma
        for i in range(len(self.alphabet)):
            self.print_state("swap_replace_" + self.alphabet[i], self.MID, self.LEFT, "", "swap_back_" + self.alphabet[i])
            self.print_state("swap_replace_" + self.alphabet[i], " ".join(self.markedAlphabet), self.LEFT, "", "")
        
        # find the matching byte of 1st number to swap
        for i in range(len(self.alphabet)):
            self.print_state("swap_back_" + self.alphabet[i], " ".join(self.alphabet), self.LEFT, "", "")
            self.print_state("swap_back_" + self.alphabet[i], " ".join(self.markedAlphabet), self.LEFT, self.markedAlphabet[i], "swap_back")

        # move back to pos0 and start the swap cycle again
        self.print_state("swap_back", " ".join(self.markedAlphabet), self.LEFT, "", "")
        self.print_state("swap_back", " ".join(self.start_compare), self.RIGHT, "", "swap")


        # backtrack implementation

        self.print_state("backtrack1" , self.MID, self.LEFT, self.END, "backtrack2") # see a comma 
        self.print_state("backtrack1" , self.START, self.RIGHT, "", "clean_up") # only 1 element left, fully sorted eg [0001]0002]0003]

        self.print_state("backtrack1" , " ".join(self.alphabet), self.LEFT, "", "backtrack1")
        #If there still scratchmark, implement restore (in case of 1 element only)
        for i in range(len(self.alphabet)):
            self.print_state("backtrack1" , self.markedAlphabet[i], self.LEFT, self.alphabet[i], "backtrack1")
        


        self.print_state("backtrack2" , " ".join(self.join_list(self.alphabet,self.markedAlphabet,self.MID)), self.LEFT, "", "backtrack2") 
        self.print_state("backtrack2" , self.START, self.RIGHT, "", "compare")  # reach the start AND not ran n time

        #clearn up: change all ] -> comman except last 1
        self.print_state("clean_up" ," ".join(self.alphabet), self.RIGHT, "", "clean_up")
        self.print_state("clean_up" , self.END, self.RIGHT, ",", "clean_up")
        self.print_state("clean_up" , self.blank, self.LEFT, "", "clean_up_last")
        self.print_state("clean_up_last" , ",", self.LEFT, self.END, "return_base") # return to 0 and halt, everything sorted, accepted

        self.print_state("return_base" , " ".join(self.join_list(self.markedAlphabet,self.alphabet,self.end_compare)), self.LEFT, "", "return_base")
        self.print_state("return_base" , self.START, self.HALT, "", self.special_state[1]) #Reach index 0, halt and accept


if __name__ == "__main__":
    tsv = TSVgen()
    tsv.genTSV()