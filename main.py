from expense import expense as exp


expenses = []


def add_expense():
    whoPaid = input("Who paid for the expense?")
    while True:
        try:
            amount = int(input("How much was the expense?"))
            break
        except ValueError:
            print("Invalid input")

    payees = []
    payees_active = True
    while payees_active:
        payee = input("Who needs to pay?(Enter only one name)")
        payees.append(payee)
        go_again = input("Add another name? (y or n)")
        if go_again == "n":
            payees_active = False
        elif go_again != "y":
            print("Unrecognized input")
            go_again = input("Add another name? (y or n)")

    expense = exp(whoPaid, payees, amount)
    expenses.append(expense)


# inst = exp("Nick", ["Nick", "Jack", "Max", "Zack"], 40)
# inst.print_expense()


active = True
while active:
    choice = input("(e)xpense or (q)uit ")
    if choice == "e" or choice == "expense":
        add_expense()
    elif choice == "q" or choice == "quit":
        print("Quit")
        active = False
    else:
        print("Invalid choice")

for i in expenses:
    i.print_expense()
