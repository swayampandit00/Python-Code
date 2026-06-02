def main():
    print("Welcome to number checker\n")
    num1 = int(input("Please enter your first number: "))
    num2 = int(input("Now, enter the second number: "))

    # greater_number = num1
    # if num1 > num2:
    #     greater_number = num1
    # else:
    #     greater_number = num2
    greater_number = num1 if num1 > num2 else num2
    print(str(greater_number) + " is the greatest number")

if __name__ == "__main__":
    main()
