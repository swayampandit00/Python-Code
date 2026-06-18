# Class definition
class Car:
    # Fields (instance variables)
    def __init__(self, brand, model, year):
        self.__brand = brand  # Private field (using name mangling)
        self.__model = model
        self.__year = year
    
    # Method to display car info
    def display_info(self):
        print("Brand: " + self.__brand)
        print("Model: " + self.__model)
        print("Year: " + str(self.__year))
    
    # Getter method
    def get_brand(self):
        return self.__brand

def main():
    # Creating an instance/object of the Car class
    myCar = Car("Toyota", "Camry", 2023)
    
    # Accessing the object using reference variable 'myCar'
    myCar.display_info()
    
    # Creating another instance
    anotherCar = Car("Honda", "Civic", 2022)
    anotherCar.display_info()
    
    # Using getter to access field
    print("My car brand: " + myCar.get_brand())

if __name__ == "__main__":
    main()
