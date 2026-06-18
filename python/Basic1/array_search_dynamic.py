def main():
    arr = [5, 15, 25, 35, 40, 45, 50, 55, 60]
    target = int(input("enter your number you want to search them : "))
    found = False

    for num in arr:
        if num == target:
            found = True
            break

    print("Found" if found else "Not Found")

if __name__ == "__main__":
    main()
