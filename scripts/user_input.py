def get_time_range():
    print("Choose your time frame")
    print("1: 1 Month")
    print("2: 6 Months")
    print("3: Multiple Years")
    choice = input("Choose 1, 2 or 3: ")
    print("\n--------------------------------------------------- \n")

    if choice == "1":
        return "short_term"
    elif choice == "2":
        return "medium_term"
    elif choice == "3":
        return "long_term"
    else:
        print("Invalid Choice. Try Again: ")
        return get_time_range()
