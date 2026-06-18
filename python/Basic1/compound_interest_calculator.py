import math

def main():
    P = float(input("Enter Principal: "))

    R = float(input("Enter Rate (%): "))

    T = float(input("Enter Time (years): "))

    N = int(input("Enter Compounds per year: "))

    r = R / 100.0
    A = P * math.pow(1 + (r / N), N * T)
    CI = A - P

    print("Final Amount: " + str(A))
    print("Compound Interest: " + str(CI))

if __name__ == "__main__":
    main()
