def main():
    print("Welcome to Ticket Discount Calculator")
    age = int(input("Please enter your age: "))
    is_female = input("Are you a female? (true/false) ").lower() == "true"

    if age < 5:
        print("You got 75% discount")
    elif is_female:
        print("You got 50% discount")
    elif age > 60 and not is_female:
        print("You got 25% discount")
    else:
        print("You got no discount")

if __name__ == "__main__":
    main()

"""Welcome to Ticket Discount Calculator
Welcome to Ticket Discount Calculator
Please enter your age: 4
Are you a female? (true/false) true
You got 75% discount

Welcome to Ticket Discount Calculator
Please enter your age: 15
Are you a female? (true/false) true
You got 50% discount

Welcome to Ticket Discount Calculator
Please enter your age: 60
Are you a female? (true/false) false
You got no discount
"""
