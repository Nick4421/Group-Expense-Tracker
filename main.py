from expense import expense as exp
from reimbursement import reimbursement
from member import member as mem
from member import get_indebt_owedmoney

expenses = []
members = []


def get_members():
    all_members = []
    print("Who is in this group? (Enter one name at a time, enter 'q' to stop)")
    while True:
        name = input()
        if name == "q":
            if not all_members:
                # Empty array
                print("Must enter at least one name")
            else:
                break
        else:
            member = mem(name)
            all_members.append(member)

    return all_members


def add_expense():
    who_paid = "UNINITIALIZED"
    for member in members:
        who_paid = input("Did " + member.name +
                         " pay for the expense? (y or n) ")
        if who_paid == "y":
            who_paid = member.name
            break

    while True:
        try:
            amount = int(input("How much was the expense? "))
            # Round to 2 decimal places
            amount = round(amount, 2)
            break
        except ValueError:
            print("Invalid input")

    payees = []
    for member in members:
        needs_to_pay = input("Does " + member.name + " need to pay? (y or n) ")
        if needs_to_pay == "y":
            payees.append(member.name)
        elif needs_to_pay == "n":
            continue
        else:
            print("Unrecognized input. " + member.name +
                  " will not be added to payees.")

    if not payees:
        # No payees added
        payees.append("UNINITIALIZED")

    expense = exp(who_paid, payees, amount)
    expenses.append(expense)


members = get_members()
while True:
    choice = input("(e)xpense or (q)uit ")
    if choice == "e" or choice == "expense":
        add_expense()
    elif choice == "q" or choice == "quit":
        print("Quit")
        break
    else:
        print("Invalid choice")

in_debt, owed_money = get_indebt_owedmoney(members)

in_debt_index = 0
owed_money_index = 0

while in_debt_index < len(in_debt) and owed_money_index < len(owed_money):
    if owed_money[owed_money_index].balance > in_debt[in_debt_index].balance:
        pass
    elif owed_money[owed_money_index].balance < in_debt[in_debt_index].balance:
        pass
    elif owed_money[owed_money_index].balance == in_debt[in_debt_index].balance:
        pass
