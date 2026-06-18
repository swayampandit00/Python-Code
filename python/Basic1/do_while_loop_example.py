import random

def main():
    print("=== Advanced Do-While Loop Examples ===")
    
    # 1. Basic do-while loop
    print("\n--- Basic Do-While Loop ---")
    i = 1
    while True:
        print("Count: " + str(i))
        i += 1
        if i > 5:
            break
    
    # 2. Do-while for input validation
    print("\n--- Input Validation ---")
    while True:
        positive_number = int(input("Enter a positive number: "))
        if positive_number <= 0:
            print("Invalid! Please enter a positive number.")
        else:
            break
    print("Valid number entered: " + str(positive_number))
    
    # 3. Menu-driven program
    print("\n--- Menu-Driven Program ---")
    menu_running = True
    while menu_running:
        print("\n--- Menu ---")
        print("1. Say Hello")
        print("2. Say Goodbye")
        print("3. Exit")
        choice = int(input("Choose option: "))
        
        if choice == 1:
            print("Hello!")
        elif choice == 2:
            print("Goodbye!")
        elif choice == 3:
            print("Exiting...")
            menu_running = False
        else:
            print("Invalid choice!")
    
    # 4. Do-while for password validation
    print("\n--- Password Validation ---")
    correct_password = "java123"
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        entered_password = input("Enter password (attempt " + str(attempts + 1) + "/" + str(max_attempts) + "): ")
        attempts += 1
        
        if entered_password == correct_password:
            print("Access granted!")
            break
        elif attempts < max_attempts:
            print("Incorrect password. Try again.")
        else:
            print("Maximum attempts reached. Access denied.")
    
    # 5. Do-while for guessing game
    print("\n--- Number Guessing Game ---")
    secret_number = random.randint(1, 100)
    guess_attempts = 0
    
    while True:
        guess = int(input("Guess a number (1-100): "))
        guess_attempts += 1
        
        if guess < secret_number:
            print("Too low!")
        elif guess > secret_number:
            print("Too high!")
        else:
            print("Correct! You guessed it in " + str(guess_attempts) + " attempts!")
            break
    
    # 6. Do-while for calculator
    print("\n--- Simple Calculator ---")
    calc_running = True
    while calc_running:
        num1 = float(input("Enter first number (0 to exit): "))
        
        if num1 == 0:
            calc_running = False
            continue
        
        num2 = float(input("Enter second number: "))
        operation = input("Enter operation (+, -, *, /): ")
        
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 == 0:
                print("Cannot divide by zero!")
                continue
            result = num1 / num2
        else:
            print("Invalid operation!")
            continue
        
        print("Result: " + str(result))
    
    # 7. Do-while for number validation
    print("\n--- Range Validation ---")
    while True:
        range_number = int(input("Enter a number between 10 and 50: "))
        if range_number < 10 or range_number > 50:
            print("Number must be between 10 and 50!")
        else:
            break
    print("Valid number: " + str(range_number))

if __name__ == "__main__":
    main()
