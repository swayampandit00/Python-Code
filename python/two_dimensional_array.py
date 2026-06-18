def main():
    myArr = [[0] * 3 for _ in range(2)]
    myArr[0][0] = 9

    arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(len(arr[0]))

    # Traversal
    i = 0
    while i < len(arr):
        j = 0
        while j < len(arr[i]):
            print(str(arr[i][j]) + " ", end="")
            j += 1
        print()
        i += 1

if __name__ == "__main__":
    main()
