def main():
    print("Welcome to Driving License Portal")
    age = int(input("Please enter your age: "))

    if age >= 18:
        print("You are eligible to drive")
    else:
        print("you are not eligible to drive")

if __name__ == "__main__":
    main()

#output
"""Welcome to Driving License Portal
Please enter your age: 18
You are eligible to drive

Welcome to Driving License Portal
Please enter your age: 17
you are not eligible to drive """
