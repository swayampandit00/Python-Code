import math

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def main():
    print("=== Advanced For Loop Examples ===")
    
    # 1. Basic for loop
    print("\n--- Basic For Loop ---")
    for i in range(1, 6):
        print("Count: " + str(i))
    
    # 2. Reverse for loop
    print("\n--- Reverse For Loop ---")
    for i in range(10, 0, -1):
        print(str(i) + " ", end="")
    print()
    
    # 3. For loop with step
    print("\n--- For Loop with Step ---")
    for i in range(0, 21, 2):
        print(str(i) + " ", end="")
    print()
    
    # 4. Enhanced for-each loop with array
    print("\n--- Enhanced For-Each Loop ---")
    numbers = [10, 20, 30, 40, 50]
    total = 0
    for num in numbers:
        print("Number: " + str(num))
        total += num
    print("Sum: " + str(total))
    
    # 5. Nested for loop (multiplication table)
    print("\n--- Nested For Loop (Multiplication Table) ---")
    for i in range(1, 6):
        for j in range(1, 6):
            print("%4d" % (i * j), end="")
        print()
    
    # 6. Labeled loop with break
    print("\n--- Labeled Loop with Break ---")
    for i in range(1, 4):
        for j in range(1, 4):
            if i == 2 and j == 2:
                print("Breaking at i=" + str(i) + ", j=" + str(j))
                break
            print("i=" + str(i) + ", j=" + str(j))
        if i == 2 and j == 2:
            break
    
    # 7. Loop with continue
    print("\n--- Loop with Continue ---")
    for i in range(1, 11):
        if i % 2 == 0:
            continue  # Skip even numbers
        print(str(i) + " ", end="")
    print()
    
    # 8. Pattern printing (triangle)
    print("\n--- Pattern Printing ---")
    for i in range(1, 6):
        for j in range(1, i + 1):
            print("* ", end="")
        print()
    
    # 9. Finding prime numbers
    print("\n--- Prime Numbers (1-50) ---")
    for i in range(2, 51):
        if is_prime(i):
            print(str(i) + " ", end="")
    print()
    
    # 10. Fibonacci series
    print("\n--- Fibonacci Series (First 10) ---")
    n = 10
    first = 0
    second = 1
    print(str(first) + " " + str(second) + " ", end="")
    for i in range(2, n):
        next_num = first + second
        print(str(next_num) + " ", end="")
        first = second
        second = next_num
    print()

if __name__ == "__main__":
    main()
