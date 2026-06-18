def main():
    # print("before loop")
    # for i in range(1, 1000):
    #     if i == 101:
    #         break
    #     print(i)
    # print("Out of loop")
    
    print("before loop")
    for i in range(1, 10):
        if i == 5:
            continue
        print(i)
    print("Out of loop")

if __name__ == "__main__":
    main()
