roll_number = [45, 12, 89, 23, 67, 34, 90]
#search = 67



#step 1

roll_number.sort()

print("sorted list:", roll_number)

search = int(input("enter a value you want to search in the list:"))

low = 0
high  = len(roll_number) - 1
while low <= high:
    mid = (low + high) //2
    if roll_number[mid] == search:
        print("found at index:", mid)
        break

    elif search> roll_number[mid]:
        low = mid + 1

    else:
        high = mid - 1

else:
    print("not fount")