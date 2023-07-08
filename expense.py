class expense:
    def __init__(self, payer, payees, amount):
        self.payer = payer
        self.payees = payees
        self.amount = amount

    def print_expense(self):
        print(self.payer + " Payed.")
        print("$" + str(self.amount) + " is the amount.")
        print(", ".join(self.payees) + " are in debt.")
