import math

def main():
    radius = float(input("Enter radius: "))

    circumference = 2 * math.pi * radius
    area = math.pi * radius * radius
    volume = (4.0 / 3.0) * math.pi * radius * radius * radius

    print("Circumference: " + str(circumference))
    print("Area: " + str(area))
    print("Volume of Sphere: " + str(volume))

if __name__ == "__main__":
    main()
