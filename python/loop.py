def main():
    num = 1  # initialization
    while num <= 10:  # condition
        print(num)  # actual work
        num = num + 1  # updating the condition

    count = 500
    while count >= 200:
        print(count)
        count -= 1

    i = 0
    while i < 5:
        inp = int(input())
        print("Number is: " + str(inp))
        i += 1

if __name__ == "__main__":
    main()
