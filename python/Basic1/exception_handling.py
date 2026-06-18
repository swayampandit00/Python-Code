def main():
    try:
        a = 10 // 0
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()
