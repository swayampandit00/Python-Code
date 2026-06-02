def is_found(arr, num):
    index = 0
    while index < len(arr):
        if arr[index] == num:
            return True
        index += 1
    return False

def main():
    arr = [3, 6, 8, 87, 65, 4, 68, 23, 9, 98, 34]
    print("Welcome to Array Searching\n")
    num = int(input("Enter the number you want to search: "))
    found = is_found(arr, num)
    if found:
        print("Your number was found in the array")
    else:
        print("Your number was not found in the array")

if __name__ == "__main__":
    main()
