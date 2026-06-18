def main():
    a = 5
    x1 = int(input())
    a = a + x1
    a += x1

    print(a)
    x2 = int(input())
    a = a + x2
    print(a)
    x3 = int(input())
    a = a + x3
    print(a)
    x4 = int(input())
    a = a + x4
    print(a)

if __name__ == "__main__":
    main()
#output

"""2
9
3
12
4
16
6
22 """
