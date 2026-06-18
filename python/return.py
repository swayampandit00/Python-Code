def read_number():
    number = int(input("Please enter the number: "))
    return number

def greet():
    print("Welcome to Calculator\n")

def main():
    greet()
    first = read_number()
    second = read_number()

    sum_result = first + second
    print("Sum of the numbers is: " + str(sum_result))

if __name__ == "__main__":
    main()
