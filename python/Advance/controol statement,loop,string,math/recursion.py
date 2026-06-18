def factorial(num):
    print("Function called for: " + str(num))
    if num == 1:
        return 1
    return num * factorial(num - 1)

def factorial_iterative(num):
    result = 1
    for i in range(1, num + 1):
        result *= i
    return result

def main():
    print("Welcome to Factorial generator\n")
    num = int(input("Please enter your number: "))
    fact = factorial(num)
    print("Factorial of your number is: " + str(fact))

if __name__ == "__main__":
    main()
