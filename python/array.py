def main():
    # myArr = [0] * 5
    # myArr[0] = 98
    # myArr[3] = 65
    # myArr[1] = 2
    # myArr[2] = 8
    # myArr[4] = 37
    myArr = [98, 2, 8, 65, 37]
    # index = 2

    # print(myArr[0])
    # print(myArr[1])
    # print(myArr[index])
    # print(myArr[3])
    # print(myArr[4])
    # Array Traversal
    index = 0
    while index < len(myArr):
        print(myArr[index])
        index += 1

    strArr = [None] * 4
    strArr[0] = "My String"

    newStrArr = ["first", "second", "third"]
    print(len(newStrArr))

if __name__ == "__main__":
    main()
