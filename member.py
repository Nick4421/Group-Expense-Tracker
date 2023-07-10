class member:
    def __init__(self, name):
        self.name = name
        self.balance = 0


def get_indebt_owedmoney(members):
    in_debt = []
    owed_money = []
    for member in members:
        if member.balance > 0:
            owed_money.append(member)
        elif member.balance < 0:
            in_debt.append(member)
    return in_debt, owed_money
