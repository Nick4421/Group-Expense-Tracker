from expense import expense as exp
from reimbursement import reimbursement
from member import member as mem
from member import get_indebt_owedmoney

# payer, payees, amount
expenses = [exp("exp 1", "Nick", ["Nick", "Porter", "Sashwat", "Leif"], 49.60),
            exp("exp 2", "Nick", ["Nick", "Sashwat", "Leif"], 32.48),
            exp("exp 3", "Sashwat", ["Nick", "Sashwat", "Leif"], 72),
            exp("exp 4", "Leif", ["Nick", "Sashwat", "Leif", "Porter"], 18),
            exp("exp 5", "Leif", ["Leif", "Porter"], 12)]
members = [mem("Nick"), mem("Porter"), mem("Sashwat"), mem("Leif")]
# expenses = []
# members = []


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


# Splits expense, returns members array with updated balances
def split_expense(members, payees, expense_amount):
    num_payees = len(payees)

    # Convert expense to cents
    expense_cents = int(expense_amount * 100)

    # Calculate amount per payee in cents
    amount_per_payee_cents = expense_cents // num_payees

    # Calculate the remaining balance in cents
    remaining_balance_cents = expense_cents - \
        (amount_per_payee_cents * num_payees)

    # Distribute remaining balance evenly
    payees_amounts = [amount_per_payee_cents / 100] * num_payees

    for i in range(remaining_balance_cents):
        payees_amounts[i] += 0.01
        payees_amounts[i] = round(payees_amounts[i], 2)

    iterator = 0
    for p in payees:
        members[find_member_from_name(
            p, members)].balance -= payees_amounts[iterator]
        iterator += 1

    return members


# Returns an array of expense objects
def add_expense(members, expenses):
    # Get who paid
    who_paid = "UNINITIALIZED"
    for member in members:
        who_paid = input("Did " + member.name +
                         " pay for the expense? (y or n) ")
        if who_paid == "y":
            who_paid = member.name
            break

    # Get amount
    while True:
        try:
            amount = float(input("How much was the expense? "))
            # Round to 2 decimal places
            amount = round(amount, 2)
            break
        except ValueError:
            print("Invalid input")

    # Get people who need to pay
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

    # Split balance evenly amongst payees
    split_expense(members, payees, amount)

    expense = exp("Expense Name", who_paid, payees, amount)
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


# members = get_members()
expenses = run_main_input_loop(members, expenses)
# members = distribute_expenses(members, expenses)
for x in members:
    print(x.name, x.balance)
print()
# Both arrays have member objects in them (member.name, member.balance)
in_debt, owed_money = get_indebt_owedmoney(members)
reimbursements = get_reimbursements()

for i in reimbursements:
    print(i.in_debt + " owes " + i.owed_money + " $" + str(i.amount))

###########################################


def split_bill(expense, num_payees):
    # Convert expense to cents
    expense_cents = int(expense * 100)

    # Calculate amount per payee in cents
    amount_per_payee_cents = expense_cents // num_payees

    # Calculate the remaining balance in cents
    remaining_balance_cents = expense_cents - \
        (amount_per_payee_cents * num_payees)

    # Distribute remaining balance evenly
    payees = [amount_per_payee_cents / 100] * num_payees

    for i in range(remaining_balance_cents):
        payees[i] += 0.01
        payees[i] = round(payees[i], 2)

    return payees


# test = split_bill(10, 3)

# for p in test:
#     print(p)
