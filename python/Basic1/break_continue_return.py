def show_message():
    print("Return example method executed.")
    return

def main():
    for i in range(1, 11):
        if i == 3:
            continue
        if i == 7:
            break
        print(i)

    show_message()

if __name__ == "__main__":
    main()
