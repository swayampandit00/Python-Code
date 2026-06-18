class Car:
    def __init__(self, no_of_wheels, no_of_doors, max_speed, name, model_number, company):
        self.no_of_wheels = no_of_wheels
        self.no_of_doors = no_of_doors
        self.max_speed = max_speed
        self.name = name
        self.model_number = model_number
        self.company = company
    
    def __str__(self):
        return "Car{" + \
                "noOfWheels=" + str(self.no_of_wheels) + \
                ", noOfDoors=" + str(self.no_of_doors) + \
                ", maxSpeed=" + str(self.max_speed) + \
                ", name='" + self.name + '\'' + \
                ", modelNumber='" + self.model_number + '\'' + \
                ", company='" + self.company + '\'' + \
                '}'

def main():
    swift = Car(4, 4, 120, "Swift", "SW876", "Maruti")
    print(swift)

if __name__ == "__main__":
    main()
