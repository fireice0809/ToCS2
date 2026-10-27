import matplotlib.pyplot as plt
import pandas as pd


def main():
    data = pd.read_csv("complexity.csv")

    plt.scatter(data["Size"], data["Time"], alpha=0.6)
    plt.xlabel("Input size")
    plt.ylabel("Number of steps")
    plt.title("Turing machine complexity")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("complexity.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
