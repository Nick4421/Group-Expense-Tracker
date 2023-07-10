from expense import expense as exp
from reimbursement import reimbursement
from member import member as mem
from member import get_indebt_owedmoney

# payer, payees, amount
# expenses = [exp("Nick", ["Frank", "Henry"], 50), exp("Frank", ["Nick"], 10)]
# members = [mem("Nick", 28.85), mem("Porter", -24.39),
#            mem("Sashwat", 18.77), mem("Leif", -23.23)]
expenses = []
members = []


# Returns an array of member objects
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


# Returns an array of expense objects
def add_expense(members, expenses):
    who_paid = "UNINITIALIZED"
    for member in members:
        who_paid = input("Did " + member.name +
                         " pay for the expense? (y or n) ")
        if who_paid == "y":
            who_paid = member.name
            break

    while True:
        try:
            amount = float(input("How much was the expense? "))
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
    return expenses


# Returns an array of reimbursement objects
def get_reimbursements():
    in_debt_index = 0
    owed_money_index = 0
    reimbursements = []
    while in_debt_index < len(in_debt) and owed_money_index < len(owed_money):
        curr_owed_money = owed_money[owed_money_index]
        curr_in_debt = in_debt[in_debt_index]

        if abs(curr_owed_money.balance) > abs(curr_in_debt.balance):
            # subtract in_debt.balance from owed_money.balance
            curr_owed_money.balance += curr_in_debt.balance
            # add reimbursement to the reimbursement array
            rm = reimbursement(curr_owed_money.name,
                               curr_in_debt.name, abs(curr_in_debt.balance))
            reimbursements.append(rm)
            # set the in_debt.balance to 0
            curr_in_debt.balance = 0
            # add one to the in_debt_index variable
            in_debt_index += 1

        elif abs(curr_owed_money.balance) < abs(curr_in_debt.balance):
            # subtract owed_money.balance from in_debt.balance
            curr_in_debt.balance += curr_owed_money.balance
            # add reimbursement to the reimbursement array
            rm = reimbursement(curr_owed_money.name,
                               curr_in_debt.name, abs(curr_owed_money.balance))
            reimbursements.append(rm)
            # set the owed_money.balance to 0
            curr_owed_money.balance = 0
            # add one to the owed_money_index variable
            owed_money_index += 1

        elif abs(curr_owed_money.balance) == abs(curr_in_debt.balance):
            # add reimbursement to array
            rm = reimbursement(curr_owed_money.name,
                               curr_in_debt.name, abs(curr_owed_money.balance))
            reimbursements.append(rm)
            # set both balances to 0
            curr_owed_money.balance = 0
            curr_in_debt.balance = 0
            # add one to both indices
            owed_money_index += 1
            in_debt_index += 1

    for re in reimbursements:
        # round down to 2 decimals
        re.amount *= 100
        re.amount //= 1
        re.amount /= 100

    return reimbursements


# Returns the expenses array
def run_main_input_loop(members, expenses):
    while True:
        choice = input("(e)xpense or (q)uit ")
        if choice == "e" or choice == "expense":
            expenses = add_expense(members, expenses)
        elif choice == "q" or choice == "quit":
            print("Quit")
            break
        else:
            print("Invalid choice")
    return expenses


# Returns the index in the members array that the person with the given name is in
# Raises an error if name not found
def find_member_from_name(name, members):
    count = 0
    for mem in members:
        if mem.name == name:
            return count
        else:
            count += 1
    raise Exception("member name not found")


# Distributes expenses evenly across payees
# Returns a members array with updated balances
def distribute_expenses(members, expenses):
    for exp in expenses:
        num_payees = len(exp.payees)
        amount_per_person = exp.amount / num_payees
        # Round down to 2 decimal places
        amount_per_person *= 100
        amount_per_person //= 1
        amount_per_person /= 100

        # Add expense amount to the payers balance
        payer_index = find_member_from_name(exp.payer, members)
        members[payer_index].balance += exp.amount

        # Remove equal amounts from payees balances
        payee_total = 0
        for payee in exp.payees:
            payee_index = find_member_from_name(payee, members)
            members[payee_index].balance -= amount_per_person
            payee_total += amount_per_person

        # Compensate for any rounding errors
        curr_payee_index = 0
        while exp.amount != payee_total:
            # Add one cent to different payees until the rounding error is gone
            # Since we always round down, any error will always be less than the final amount
            curr_payee = exp.payees[curr_payee_index]
            members[find_member_from_name(curr_payee, members)].balance += 0.01
            curr_payee_index += 1
    return members


members = get_members()
expenses = run_main_input_loop(members, expenses)
members = distribute_expenses(members, expenses)

# Both arrays have member objects in them (member.name, member.balance)
in_debt, owed_money = get_indebt_owedmoney(members)
reimbursements = get_reimbursements()

for i in reimbursements:
    print(i.in_debt + " owes " + i.owed_money + " $" + str(i.amount))
