from expense import expense as exp
from member import member as mem
from reimbursement import reimbursement as rm
from random import randint
from main import distribute_expense, get_reimbursements


def distribute_expense_test():
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


def settle_balances_test():
    payees_2 = ["Nick", "Sashwat"]
    payees_3 = ["Nick", "Sashwat", "Leif"]
    payees_4 = ["Nick", "Sashwat", "Leif", "Porter"]
    payees_5 = ["Nick", "Sashwat", "Leif", "Porter", "Henry"]
    payees_6 = ["Nick", "Sashwat", "Leif", "Porter", "Henry", "Frank"]
    all_payees = [payees_2, payees_3, payees_4, payees_5, payees_6]

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
        reimbursements = settle_balances(members)
        for r in reimbursements:
            print(f'{r.debtor} owes {r.creditor} {r.amount}')


settle_balances_test()
