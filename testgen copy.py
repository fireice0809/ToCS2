import random
import pandas as pd
from pathlib import Path
from runner import Machine


MACHINE_PATH = "./turing.tsv"
machine = Machine.from_tsv(Path(MACHINE_PATH).read_text(encoding="utf-8"))

MAX = 18446744073709551615 # 16^16 - 1
random.seed(36)

SAVE_FILE = "test_cases.txt"


def num_gen():
    # return a random number in 16-digit hexadecimal form
    num = random.randint(0, MAX)
    return (f"{num:016x}".upper())

def test_gen(size: int, edge_case: int):
    # edge cases options:
    # 0 - ordinary random list
    # 1 - already sorted 
    # 2 - reverse sorted (large -> small)
    # 3 - with possible duplicates (almost guaranteed with size >= 5)
    # 4 - only empty list
    # 5 - shuffled largest and smallest
    # 6 - Only repeated string

    test = []
    if (edge_case == 0):
        for _ in range(size):
            test.append(num_gen())
        unsorted_tape = "[" + ",".join(test) + "]"

        test.sort(reverse=False)

        sorted_tape = "[" + ",".join(test) + "]"
        return unsorted_tape, sorted_tape
    
    elif (edge_case == 1):
        for _ in range(size):
            test.append(num_gen())
        test.sort()
        sorted_tape = "[" + ",".join(test) + "]"
        unsorted_tape = sorted_tape
        return unsorted_tape, sorted_tape
    
    elif (edge_case == 2):
        for _ in range(size):
            test.append(num_gen())
        test.sort(reverse=True)
        unsorted_tape = "[" + ",".join(test) + "]"

        test.sort(reverse=False)


        sorted_tape = "[" + ",".join(test) + "]"
        return unsorted_tape, sorted_tape
    
    elif (edge_case == 3):
        remain = size 
        while(remain > 0):
            duplicate = random.randint(1, min(3, remain))
            current = num_gen()
            for _ in range(duplicate):
                test.append(current)
            remain -= duplicate
        random.shuffle(test)
        unsorted_tape = "[" + ",".join(test) + "]"

        test.sort(reverse=False)

        sorted_tape = "[" + ",".join(test) + "]"
        return unsorted_tape, sorted_tape
    
    elif (edge_case == 4):
        return "[]", "[]"

    elif (edge_case == 5):
        remain = size
        while(remain > 0):
            if (remain % 2 == 0):
                current = "0000000000000000"
            else:
                current = "FFFFFFFFFFFFFFFF"
            test.append(current)
            remain -= 1
        random.shuffle(test)
        unsorted_tape = "[" + ",".join(test) + "]"
        test.sort(reverse=False)
        
        sorted_tape = "[" + ",".join(test) + "]"
        return unsorted_tape, sorted_tape

    elif (edge_case == 6):
        current = num_gen()
        for _ in range(size):
            test.append(current)
        sorted_tape = "[" + ",".join(test) + "]"
        return sorted_tape, sorted_tape
    
    return None

def clear_test_case():
    with open(SAVE_FILE, "w") as file:
        file.write("")

def save_case(test_case: str):
    with open(SAVE_FILE, "a") as file:
        file.write(test_case + "\n")


def execute_test(test_tape: str):
    save_case(test_tape)
    with machine.run(test_tape, max_steps= 0) as result: # no limit in step
        final_tape = "".join(result.iter_text_chunks())
        return final_tape, result.steps, result.head_position, result.status, result.final_state

def run_test(test_case: str, expected_output: str):
    final_tape, num_steps, final_position, status, final_state = execute_test(test_case)
    return final_tape == expected_output and final_position == 0 and status == "accepted" and final_state == "✔", num_steps

class Tester:
    def __init__(self):
        self.fail_count = 0
        self.fail_cases = []
        self.case_count = 0
        self.df = pd.DataFrame(columns=["tape_size", "num_steps"])

    def test(self, edge_case: int, test_range: int = 100, num_test: int = 1):
        for size in range(1, test_range):
            for _ in range(num_test):
                case, ground_truth = test_gen(size, edge_case)
                if edge_case == 4: # case 4 is empty list
                    tape_size = 2 # tape length 2 []
                else:
                    tape_size = 17*size + 1
                success, num_steps = run_test(case, ground_truth)
                if success:
                    self.df.loc[len(self.df)] = {"tape_size": tape_size, "num_steps": num_steps}
                else:
                    self.fail_count += 1
                    self.fail_cases.append(self.case_count)
                self.case_count +=1

    def run_test_suite(self):
        # testing
        clear_test_case()
        self.test(0, 50, 10) # random cases
        self.test(1, 50, 1) # already sorted
        self.test(2, 50, 1) # reversed
        self.test(3, 50, 1) # with possible duplications
        self.test(4, 2, 1) # only 1 empty-list case
        self.test(5, 50, 1) # shuffled largest and smallest
        self.test(6, 50, 1) # all the same elements
        return self.df, self.fail_cases, self.fail_count
            

if __name__ == "__main__":
    tester = Tester()
    df, fail_cases, fail_count = tester.run_test_suite()

    print(f"Number of failed cases: {fail_count}")
    if fail_count > 0:
        for case in fail_cases:
            print(f"Failed cases: {case}")

    df.to_csv("complexity.csv", index = False)
    print("Saved complexity analysis csv")