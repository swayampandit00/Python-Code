def sum_two_numbers(first_num, second_num):
    print("First Number received: " + str(first_num))
    print("Second Number received: " + str(second_num))
    return first_num + second_num

def main():
    print(sum_two_numbers(4, 7))
    print(sum_two_numbers(5, 9))
    print(sum_two_numbers(-67, 67))

if __name__ == "__main__":
    main()
