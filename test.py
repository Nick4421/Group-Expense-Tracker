from expense import expense as exp
from member import member as mem
from random import randint


def find_member_from_name(name, members):
    count = 0
    for mem in members:
        if mem.name == name:
            return count
        else:
            count += 1
    raise Exception("member name not found")


def distribute_expense(expense, members):
    expense_cents = int(round(expense.amount*100, 2))
    num_payees = len(expense.payees)
    amount_per_payee_cents = expense_cents // num_payees

    # Remaining balance in cents
    remaining_balance_cents = expense_cents - \
        (amount_per_payee_cents * num_payees)

    # Distribute remaining balance evenly
    payees_amounts = [amount_per_payee_cents / 100] * num_payees

    for i in range(remaining_balance_cents):
        payees_amounts[i] += 0.01
        payees_amounts[i] = round(payees_amounts[i], 2)

    payee_amount_iterator = 0
    for payee_name in expense.payees:
        member_index = find_member_from_name(payee_name, members)
        members[member_index].balance -= payees_amounts[payee_amount_iterator]
        payee_amount_iterator += 1

    # print("Expense amount: " + str(expense.amount))
    # total = 0
    # for mem in members:
    #     print(mem.name, mem.balance)
    #     total += mem.balance
    # print("Balances added up: " + str(round(total, 2)))

    return members


payees_2 = ["Nick", "Sashwat"]
payees_3 = ["Nick", "Sashwat", "Leif"]
payees_4 = ["Nick", "Sashwat", "Leif", "Porter"]
payees_5 = ["Nick", "Sashwat", "Leif", "Porter", "Henry"]
payees_6 = ["Nick", "Sashwat", "Leif", "Porter", "Henry", "Frank"]
all_payees = [payees_2, payees_3, payees_4, payees_5, payees_6]

success_counter = 0
failure_counter = 0

for _ in range(1000):
    curr_payees = all_payees[randint(0, 4)]
    members = []
    for name in curr_payees:
        curr = mem(name)
        members.append(curr)

    amount = round((randint(7, 10000) / 100), 2)

    curr_expense = exp(expense_name="expense name",
                       payer="Nick",
                       payees=curr_payees,
                       amount=amount)

    members = distribute_expense(expense=curr_expense, members=members)

    total = 0
    for i in members:
        total += (-i.balance)

    curr_expense.amount = round(curr_expense.amount, 2)
    total = round(total, 2)

    if curr_expense.amount == total:
        success_counter += 1
    else:
        failure_counter += 1

print("Passed Tests:", success_counter)
print("Failed Tests:", failure_counter)
