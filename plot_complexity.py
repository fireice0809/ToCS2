import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    data = pd.read_csv("complexity.csv")
    plt.scatter(data["Size"], data["num_steps"],s = 20, color = "green", alpha=0.8)
    plt.xlabel("Input size")
    plt.ylabel("Number of steps")
    plt.title("Turing machine complexity")
    plt.grid(alpha=0.2)
    plt.savefig("complexity.png", dpi=1000)
    plt.show()


if __name__ == "__main__":
    main()
