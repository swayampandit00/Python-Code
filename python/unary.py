def main():
    x = 5
    y = -x
    z = -y
    print(z)

    a = 5
    a = a + 1
    print(a)
    a += 1
    print(a)

    print("Watching increment")
    p = 5
    print(p)
    p += 1
    print(p)

    p += 1
    print(p)

    q = 10
    q -= 1
    print(q)

    print(q)
    q -= 1
    print(q)


""" Output:

5
6
7
Watching increment
5
6
7
7
9
9
9
8
"""
if __name__ == "__main__":
    main()
