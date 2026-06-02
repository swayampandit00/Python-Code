def main():
    myArr = [98, 2, 8, 65, 37]

    # Array Traversal
    index = 0
    while index < len(myArr):
        print(myArr[index])
        index += 1

    strArr = [None] * 4
    strArr[0] = "My String"

    newStrArr = ["first", "second", "third"]
    print("the array length is=", end="")
    print(len(newStrArr))

if __name__ == "__main__":
    main()
