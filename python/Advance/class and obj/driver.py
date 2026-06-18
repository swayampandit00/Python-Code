from car import Car

class Driver:
    min_age_for_driving = 18  # Static variable - minimum age for driving is 18 years
    
    def __init__(self):
        self.name = ""
        self.age = 0
        self.date_of_license = ""
    
    def is_allowed_to_drive(self):
        return self.age >= Driver.min_age_for_driving

def main():
    # myCar = Car()
    # myCar.addFuel(6)
    # myCar.drive()
    # myCar.drive()
    # myCar.drive()
    # myCar.addFuel(3)
    # myCar.drive()
    # print(myCar.getCurrentFuelLevel())
    
    swift = Car("Red")
    thar = Car()
    thar = None  # Setting to None - will be garbage collected
    # swift.addFuel(6)
    swift.start().drive()  # Method chaining
    print(swift.color)
    
    # myDriver = Driver()
    # myDriver.dateOfLicense = "1/Jan/2024"
    # print(minAgeForDriving)

if __name__ == "__main__":
    main()
