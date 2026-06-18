roll_number = [45, 12, 89, 23, 67, 34, 90,]
#search = 67



#step 1

roll_number.sort()

print("sorted list:", roll_number)
print("Enter the value you want to add:")
add = int(input())
roll_number.append(add)

roll_number.sort()
print("sorted list:", roll_number)
