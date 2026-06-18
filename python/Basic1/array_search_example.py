def main():
    arr = [5, 15, 25, 35]
    target = 25
    found = False

    for num in arr:
        if num == target:
            found = True
            break

    print("Found" if found else "Not Found")

if __name__ == "__main__":
    main()
