def main():
    is_male = True
    name = "Bob"

    print("before if")
    if is_male:
        print("Mr." + name)
    else:
        print("Ms." + name)
    print("after if")

    is_senior_citizen = False
    is_an_adult = True

    if is_senior_citizen:
        print("Hello Senior Citizen")
    elif is_an_adult:
        print("Hello Adult")
    else:
        print("Hello Child")

if __name__ == "__main__":
    main()

"""
before if
Mr.Bob
after if
Hello Adult
"""
