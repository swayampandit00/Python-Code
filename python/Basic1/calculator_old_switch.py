def main():
    print("1.Add 2.Subtract 3.Multiply 4.Divide")
    ch = int(input())

    print("Enter two numbers: ")
    a = float(input())
    b = float(input())

    if ch == 1:
        print(a + b)
    elif ch == 2:
        print(a - b)
    elif ch == 3:
        print(a * b)
    elif ch == 4:
        if b != 0:
            print(a / b)
        else:
            print("Divide by zero")
    else:
        print("Invalid")

if __name__ == "__main__":
    main()
