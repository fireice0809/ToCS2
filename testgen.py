import random
import time
import subprocess
import json
import pandas as pd

MAX = 18446744073709551615
random.seed(67)

def numGen():
    # return a random number in 16-bit binary form
    num = random.randint(0, MAX)
    return (f"{num:016x}".upper())

def testGen(size: int, edge: int):
    # edge cases options:
    # 0 - ordinary random list
    # 1 - already sorted 
    # 2 - reverse sorted (large -> small)
    # 3 - with duplicates (almost guaranteed with size >= 5)

    test = []
    if (edge == 0):
        for i in range(0, size):
            test.append(numGen())
        un_sort = "[" + ",".join(test) + "]"

        test.sort(reverse=False)

        sorted = "[" + ",".join(test) + "]"
        return un_sort, sorted
    elif (edge == 1):
        for i in range(0, size):
            test.append(numGen())
        test.sort()
        sorted = "[" + ",".join(test) + "]"
        un_sort = sorted
        return sorted, un_sort  
    elif (edge == 2):
        for i in range(0, size):
            test.append(numGen())
        test.sort(reverse=True)
        un_sort = "[" + ",".join(test) + "]"

        test.sort(reverse=False)


        sorted = "[" + ",".join(test) + "]"
        return un_sort, sorted
    
    elif (edge == 3):
        remain = size
        while(remain > 0):
            dupes = random.randint(1, min(3, remain))
            cur = numGen()
            for i in range(0, dupes):
                test.append(cur)
            remain -= dupes
        random.shuffle(test)
        un_sort = "[" + ",".join(test) + "]"

        test.sort(reverse=False)

        sorted = "[" + ",".join(test) + "]"
        return un_sort, sorted
    elif (edge == 4):
        return "[]", "[]"
    return None

def execute_test(test_tape):
    result = subprocess.run(
        ["python3", "./runner","--machine","./turing.tsv","--max-steps","10000000","--json",test_tape,],
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)

    return data["finalTape"], data["steps"]


def run_test(test_case, expected_output):
    final_tape, time = execute_test(test_case)
    return final_tape == expected_output, time



def test_edge(df, edge, false_count, false_case, case_count):
    for size in range(100):
            for i in range(1): #Increase or decrease this to c
                case, ground_truth = testGen(size, edge)
                sucess, time = run_test(case, ground_truth)
                if sucess:
                    df.loc[len(df)] = {"Size": size, "Time": time}
                else:
                    false_count += 1
                    false_case.append(case_count)
                case_count +=1

def test_main():
        # testing
    false_count = 0
    false_case = []
    case_count = 0
    df = pd.DataFrame(columns=["Size", "Time"])

    test_edge(df, 0, false_count, false_case, case_count)
    test_edge(df, 1, false_count, false_case, case_count)
    test_edge(df, 2, false_count, false_case, case_count)
    test_edge(df, 3, false_count, false_case, case_count)

    return df, false_count, false_case
            

if __name__ == "__main__":
    df , false_count, false_case = test_main()
    print(df.head(5))
    print(false_count)

    df.to_csv("complexity.csv", index = False)