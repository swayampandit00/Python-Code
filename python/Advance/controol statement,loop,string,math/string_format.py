def main():
    name = "Sandeep"
    marks = 45765
    print("Hello " + name + ", your marks are: " + str(marks))

    print("Hello %-10s, your marks are: %05d" % (name, marks))

if __name__ == "__main__":
    main()
