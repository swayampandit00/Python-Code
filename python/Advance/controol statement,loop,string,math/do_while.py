def main():
    # print("Please enter your age: ")
    # age = int(input())
    # while age < 0 or age > 100:
    #     print("Please enter your age: ")
    #     age = int(input())
    
    while True:
        print("Please enter your age: ")
        age = int(input())
        if 0 <= age <= 100:
            break
    print("Your age is: " + str(age))

if __name__ == "__main__":
    main()
