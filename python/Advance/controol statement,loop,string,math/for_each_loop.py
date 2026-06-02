def print_array_for_each(array):
    for name in array:
        print(name)

def print_array(array):
    for i in range(len(array)):
        print(array[i])

def main():
    array = ["Ram", "Shyam", "Mohan", "Sohan", "Sita", "Geeta"]
    # print_array(array)
    print_array_for_each(array)

if __name__ == "__main__":
    main()
