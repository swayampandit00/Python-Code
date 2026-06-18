import math

def main():
    base = float(input("Enter base: "))

    perpendicular = float(input("Enter perpendicular: "))

    hypotenuse = math.sqrt(base * base + perpendicular * perpendicular)
    print("Hypotenuse is: " + str(hypotenuse))

if __name__ == "__main__":
    main()
