while True:
    print("!. Register")
    print("2. Login")
    print("3. Vote")
    print("4. View Results")
    print("5. Exit")
    choice = input("Enter your choice : ")
    if choice == '1':
        registre_user()
    elif choice == '2':
        login_user()
    elif choice == '3':
        voting_System.vote()
    elif choice == '4':
        voting_System.vies_results()
    elif choice == '5':
        print("Exiting the System....")
        break
    else:
        print("Invalid choice please try again.")