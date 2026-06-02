def main():
    i = 1
    while i <= 100:
        print(str(i) + " ", end="")
        i += 1
    print()

    for j in range(1, 101, 2):
        print(str(j) + " ", end="")

if __name__ == "__main__":
    main()
