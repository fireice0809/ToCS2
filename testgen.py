import random
import time

MAX = 18446744073709551615
random.seed(int(time.time()))

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
        return "[" + ",".join(test) + "]"
    elif (edge == 1):
        for i in range(0, size):
            test.append(numGen())
        test.sort()
        return "[" + ",".join(test) + "]"
    elif (edge == 2):
        for i in range(0, size):
            test.append(numGen())
        test.sort(reverse=True)
        return "[" + ",".join(test) + "]"
    elif (edge == 3):
        remain = size
        while(remain > 0):
            dupes = random.randint(1, min(3, remain))
            cur = numGen()
            for i in range(0, dupes):
                test.append(cur)
            remain -= dupes
        random.shuffle(test)
        return "[" + ",".join(test) + "]"

def testSuite():
    # testing
    print(testGen(0, 0))
    print(testGen(1, 0))
    print(testGen(10, 0))
    print(testGen(10, 1))
    print(testGen(10, 2))
    print(testGen(10, 3))
    print(testGen(100, 0))
    print(testGen(100, 1))
    print(testGen(100, 2))
    print(testGen(100, 3))

if __name__ == "__main__":
    testSuite()