import os
import sys
from random import randint
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import time

OUTPUT_DIR = "./output"
RESULT_FILE = "./output/result.csv"
sys.set_int_max_str_digits(100000)  # increasing limit bcs large numbers


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n - 1):
        f0, f1 = f1, f0 + f1
    return f1


def func1(array: list):
    with ProcessPoolExecutor() as executor:
        for num, fib_res in zip(array, executor.map(fib, array)):
            with open(f"{OUTPUT_DIR}/temp/{num}.txt", "w") as file:
                file.write(str(fib_res))


def open_files(filepath: str):
    with open(f"./{OUTPUT_DIR}/temp/{filepath}", "r") as f:
        return f.read()


def func2(output_dir: str):
    files = os.listdir(f"./{OUTPUT_DIR}/temp")
    nums = []
    with ThreadPoolExecutor() as executor:
        future_file = {executor.submit(open_files, file): file[:-4] for file in files}
        for future in as_completed(future_file):
            nums.append(
                (
                    future_file[future],
                    future.result(),
                )
            )

    with open(RESULT_FILE, "w") as f:
        for pair in nums:
            f.write(f"{pair[0]},{pair[1]}\n")


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(OUTPUT_DIR + "/temp"):
        os.makedirs(OUTPUT_DIR + "/temp")

    func1(array=[randint(1000, 100000) for _ in range(1000)])
    func2(output_dir=OUTPUT_DIR)
