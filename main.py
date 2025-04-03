def menu():
    while True:
        print("Welcome user!")
        print("1. Option 1")
        print("2. Option 2")
        print("3. Option 3")
        print("4. Option 4")
        print("0. Exit")

        option = input("Please enter the coressponding number-")

        if option == "0":
            print("Exiting...")
            print("Goodbye!")
        elif option == "1":
            option1()
        elif option == "2":
            option2()
        elif option == "3":
            option3()
        elif option == "4":
            option4()
    
# def option1():
# def option2():
# def option3():
# def option4():