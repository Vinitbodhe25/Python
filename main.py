# Online Polling and Voting System

candidates = {
    1: "Vinit",
    2: "Vedant",
    3: "Venkatesh"
}

votes = {
    1: 0,
    2: 0,
    3: 0
}

voters = set()

while True:
    print("\n===== ONLINE VOTING SYSTEM =====")
    print("1. Vote")
    print("2. Show Results")
    print("3. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        voter_id = input("Enter your Voter ID: ")

        if voter_id in voters:
            print("You have already voted!")

        else:
            print("\nCandidates:")
            for number, name in candidates.items():
                print(number, ".", name)

            vote = int(input("Enter candidate number: "))

            if vote in candidates:
                votes[vote] += 1
                voters.add(voter_id)
                print("Vote submitted successfully!")
            else:
                print("Invalid candidate number.")

    elif choice == 2:
        print("\n===== VOTING RESULTS =====")

        for number, name in candidates.items():
            print(name, ":", votes[number], "votes")

    elif choice == 3:
        print("Thank you for using the Online Voting System!")
        break

    else:
        print("Invalid choice!")
