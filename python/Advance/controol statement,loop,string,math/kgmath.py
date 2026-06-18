import math
import random

def main():
    print(abs(-99))
    print(math.ceil(5.07))
    print(math.floor(5.07))
    print(round(5.57))
    print(math.pi)

    for i in range(10):
        random_num = round(random.random() * 100)
        print(random_num)

if __name__ == "__main__":
    main()
