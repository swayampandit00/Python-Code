def new_switch(day):
    day_str = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Holiday",
        7: "Holiday"
    }.get(day, "Invalid")
    print(day_str)

def old_switch(day):
    if day == 1:
        print("Monday")
    elif day == 2:
        print("Tuesday")
    elif day == 3:
        print("Wednesday")
    elif day == 4:
        print("Thursday")
    elif day == 5:
        print("Friday")
    elif day == 6 or day == 7:
        print("Holiday")
    else:
        print("Invalid day")

def main():
    print("Welcome to Day of the week detector\n")
    day = int(input("Enter your day in number: "))
    # old_switch(day)
    new_switch(day)

if __name__ == "__main__":
    main()
