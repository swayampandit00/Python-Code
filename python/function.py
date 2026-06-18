def print_third_pattern():
    print("        *")
    print("      * *")
    print("    * * *")
    print("  * * * *")
    print("* * * * *")

def print_second_pattern():
    print("* * * * *")
    print("* * * *")
    print("* * *")
    print("* *")
    print("*")

def print_first_pattern():
    rows = 0
    while rows < 5:
        print("*", end="")
        i = 0
        while i < rows:
            print(" *", end="")
            i += 1
        print()
        rows += 1

def greet_user():
    print("Good Morning from KGCoding")

def main():
    # print("In main method")
    # greet_user()
    # print("Method calling complete")
    # greet_user()

    print_first_pattern()
    # print_second_pattern()
    # print_third_pattern()

if __name__ == "__main__":
    main()
