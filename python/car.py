class Car:
    def __init__(self, carColor=None, currPrice=None):
        # Static block equivalent (Python doesn't have static blocks, but we can use class variables)
        print("This is a Static Block")
        
        # Initialization block equivalent
        print("This is a Initialization Block")
        if carColor is None:
            self.color = "Black"
            self.price = 50000.0
        else:
            self.color = carColor
            self.price = currPrice

def main():
    swift = Car()

    if True:  # code block
        print("Code Block")

if __name__ == "__main__":
    main()
