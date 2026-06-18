roll_number = [45, 12, 89, 23, 67, 34, 90]
#search = 67

search = int(input("enter a value you want to search in the list:"))

found = False

for i in range(len(roll_number)):
    if roll_number[i] == search:
        print("found at index:", i)
        found = True
        break
if not found:
    print("not found")