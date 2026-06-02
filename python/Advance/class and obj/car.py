class Car:
    no_of_cars_sold = 0  # Static variable - class level variable, common to all objects
    
    def __init__(self, color=None):
        # Instance Initialization Block equivalent
        Car.no_of_cars_sold += 1
        print("I am in Init Block")
        
        if color is None:
            # Default constructor equivalent
            self.__init__("Black")
            self.current_fuel_in_liters = 5
            return
        
        # Parameterized constructor
        self.no_of_wheels = 4
        self.color = color
        self.max_speed = 150
        self.current_fuel_in_liters = 2
        self.no_of_seats = 5
    
    def start(self):
        pop = 5  # Local variable - only used in this method
        if self.current_fuel_in_liters == 0:
            print(pop)
            print("Car is out if fuel, can not start")
        elif self.current_fuel_in_liters < 5:
            print("Car is in reserved mode, please refuel")
        else:
            print("Car is started.. bruhhhh.....")
        return self  # Return self for method chaining
    
    def drive(self):
        self.current_fuel_in_liters -= 1
        print("Car is driving")
    
    def add_fuel(self, current_fuel_in_liters):
        self.current_fuel_in_liters += current_fuel_in_liters
    
    def get_current_fuel_level(self):
        return self.current_fuel_in_liters
    
    def __str__(self):
        return "Car{" + \
                "noOfWheels=" + str(self.no_of_wheels) + \
                ", color='" + self.color + '\'' + \
                ", maxSpeed=" + str(self.max_speed) + \
                ", currentFuelInLiters=" + str(self.current_fuel_in_liters) + \
                ", noOfSeats=" + str(self.no_of_seats) + \
                '}'

# Static block equivalent (Python doesn't have static blocks, but we can initialize class variables)
print("I am in Static Block")
