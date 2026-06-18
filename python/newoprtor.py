"""
Python 'new' Operator Examples

In Python, objects are created without a 'new' keyword.
The 'new' operator in Java is used to:
1. Create new objects (instantiate classes)
2. Create new arrays
3. Create new string objects
"""

# Class definition for demonstrating object creation
class Student:
    # Fields
    def __init__(self, name, age, grade):
        self.__name = name
        self.__age = age
        self.__grade = grade
    
    # Method to display student info
    def display_info(self):
        print("Name: " + self.__name)
        print("Age: " + str(self.__age))
        print("Grade: " + self.__grade)
    
    # Getter methods
    def get_name(self):
        return self.__name
    
    def get_age(self):
        return self.__age

def print_description():
    print("\n=== How object creation works in Python ===")
    print("Syntax: object = ClassName(parameters)")
    print("Steps:")
    print("1. Python allocates memory for the object")
    print("2. Calls __init__ to initialize the object")
    print("3. Returns a reference to the newly created object")

def main():
    print("=== Python Object Creation Examples ===\n")
    
    # Example 1: Creating objects (no 'new' keyword needed)
    print("--- Example 1: Creating Objects ---")
    
    # Creating instances of Student class
    student1 = Student("John", 20, "A")
    student2 = Student("Alice", 22, "B+")
    
    # Accessing object methods
    student1.display_info()
    print()
    student2.display_info()
    
    # Example 2: Creating lists (Python's equivalent to arrays)
    print("\n--- Example 2: Creating Lists ---")
    
    # List of primitive type
    numbers = [0] * 5
    numbers[0] = 10
    numbers[1] = 20
    numbers[2] = 30
    numbers[3] = 40
    numbers[4] = 50
    
    print("Integer list: ", end="")
    for i in range(len(numbers)):
        print(str(numbers[i]) + " ", end="")
    print()
    
    # List of objects
    students = [None] * 3
    students[0] = Student("Bob", 19, "A-")
    students[1] = Student("Charlie", 21, "B")
    students[2] = Student("Diana", 20, "A")
    
    print("\nStudent list:")
    for i in range(len(students)):
        print("Student " + str(i + 1) + ": " + students[i].get_name() + 
              ", Age: " + str(students[i].get_age()))
    
    # Example 3: Creating String objects
    print("\n--- Example 3: Creating Strings ---")
    
    # String using string literal
    str1 = "Hello"
    
    # String (Python doesn't need 'new' for strings)
    str2 = "World"
    
    print("String literal: " + str1)
    print("String: " + str2)
    
    # Example 4: Dynamic list creation
    print("\n--- Example 4: Dynamic List Size ---")
    
    size = 5
    prices = [0.0] * size
    prices[0] = 19.99
    prices[1] = 29.99
    prices[2] = 39.99
    prices[3] = 49.99
    prices[4] = 59.99
    
    print("Dynamic list: ", end="")
    for price in prices:
        print(str(price) + " ", end="")
    print()
    
    # Summary
    print("\n=== Summary ===")
    print("In Python, object creation is simpler:")
    print("1. Instantiate classes (create objects) without 'new'")
    print("2. Create lists with specified size")
    print_description()

if __name__ == "__main__":
    main()
