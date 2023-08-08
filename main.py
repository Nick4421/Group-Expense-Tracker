import PySimpleGUI as sg

from expense import expense as exp
from member import member as mem
from reimbursement import reimbursement as rm


def print_members(members):
    for m in members:
        print(m.name, m.balance)


def total_expense_amount(expenses):
    total = 0.0
    for expense in expenses:
        total += expense.amount
    total = round(total, 2)
    return f'Total Expense Amount: ${total}'


def my_balance(members):
    for member in members:
        if member.is_you:
            return f'My Balance: ${round(member.balance, 2)}'

    return 'Couldn\'t Find My Balance'


# Returns true if amount can be converted into a decimal
def is_valid_amount(amount_str):
    try:
        float(amount_str)
        return True
    except ValueError:
        return False


# Returns index of the member
def find_member_from_name(name, members):
    count = 0
    for member in members:
        # print(mem.name, name)
        if member.name == name:
            return count
        else:
            count += 1
    raise Exception("member name not found")


# Returns an array of reimbursement object
def get_reimbursements(members):
    # save the original member balances
    previous_balances = []
    for i in range(len(members)):
        previous_balances.append(members[i].balance)

    transactions = []
    positive_balances = [member for member in members if member.balance > 0]
    negative_balances = [member for member in members if member.balance < 0]

    for debtor in negative_balances:
        for creditor in positive_balances:
            amount_to_settle = min(abs(debtor.balance), creditor.balance)
            if amount_to_settle > 0:
                reim = rm(creditor.name, debtor.name,
                          round(amount_to_settle, 2))
                transactions.append(reim)
                debtor.balance += amount_to_settle
                creditor.balance -= amount_to_settle
                if debtor.balance == 0:
                    break

    # reset the original member balances
    for i in range(len(members)):
        members[i].balance = previous_balances[i]

    return transactions


# Returns an array to go in the table function
def generate_expense_table_rows(expenses):
    exp_list = [
        [exp.expense_name, exp.payer, f'$ {exp.amount}'] for exp in expenses
    ]
    return exp_list


# Returns an array to go in the table function
def generate_reimbursement_table_rows(reimbursements):
    reimburse_list = [
        [f'{r.debtor} owes {r.creditor}', f'$ {r.amount}'] for r in reimbursements
    ]
    return reimburse_list


# Returns members array with updated balances
def distribute_expense(expense, members):
    # Update payer balance
    payer_index = find_member_from_name(name=expense.payer, members=members)
    members[payer_index].balance += expense.amount

    # Distribute expense payment amongst payees
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

    # Round each members balance just to be safe
    for member in members:
        member.balance = round(member.balance, 2)

    return members


# writes all info to the init file
def save_info_to_file(members, expenses):
    output = open('init', 'w')

    output.write('DO NOT MODIFY\n')
    output.write('INIT FILE FOR GROUP EXPENSE TRACKER\n')

    for member in members:
        output.write('NEW MEMBER\n')
        output.write(f'{member.name}\n')
        output.write(f'{member.is_you}\n')

    for expense in expenses:
        output.write("NEW EXPENSE\n")
        output.write(f'{expense.expense_name}\n')
        output.write(f'{expense.payer}\n')
        output.write(f'{expense.amount}\n')
        output.write(f'{len(expense.payees)}\n')
        for payee in expense.payees:
            output.write(f'{payee}\n')

    output.close()


# Returns members, expenses
def read_info_from_file():
    members = []
    expenses = []

    file = open('init', 'r')
    line = file.readline().strip()

    while line:
        if line == 'NEW MEMBER':
            mem_name = file.readline().strip()
            mem_is_you = bool(file.readline().strip())
            curr_mem = mem(name=mem_name, is_you=mem_is_you)
            members.append(curr_mem)
        elif line == 'NEW EXPENSE':
            exp_payees = []
            exp_name = file.readline().strip()
            exp_payer = file.readline().strip()
            exp_amount = float(file.readline().strip())
            num_payees = int(file.readline().strip())
            for _ in range(num_payees):
                exp_payees.append(file.readline().strip())
            curr_exp = exp(expense_name=exp_name,
                           payer=exp_payer,
                           amount=exp_amount,
                           payees=exp_payees)
            expenses.append(curr_exp)

        line = file.readline().strip()

    file.close()

    # Set member balances
    for expense in expenses:
        members = distribute_expense(members=members, expense=expense)

    # print_members(members)
    return members, expenses


def get_expense_popup_text(expense):
    name = expense.expense_name
    amount = expense.amount
    payer = expense.payer
    payees = expense.payees
    final_string = f''
    final_string += f'Expense Name: {name}\n'
    final_string += f'Amount: ${amount}\n'
    final_string += f'Payer: {payer}\n'
    final_string += '\n'
    final_string += 'Payees:\n'
    for payee in payees:
        final_string += f'  - {payee}\n'
    final_string += '\n'
    final_string += 'Delete Expense?'
    return final_string


def update_window_new_expense(expenses, members, window):
    # zero member balances before redistributing all expenses
    for member in members:
        member.balance = 0.0

    # distribute expenses
    for expense in expenses:
        members = distribute_expense(expense=expense, members=members)

    # update window to show new reimbursements
    reimbursements = get_reimbursements(members)
    window['-REIMBURSEMENT_TABLE-'].update(
        values=generate_reimbursement_table_rows(reimbursements))

    # update my balance and total expense balance
    window['-MY_BALANCE-'].update(
        my_balance(members))  # type: ignore
    window['-TOTAL_EXPENSE_AMOUNT-'].update(
        total_expense_amount(expenses))  # type: ignore

    # update the window so new expense shows
    # something with this line here
    window['-EXPENSE_TABLE-'].update(
        values=generate_expense_table_rows(expenses))


def main():
    # expenses = [exp("exp 1", "Nick", ["Nick", "Porter", "Sashwat", "Leif"], 49.60),
    #             exp("exp 2", "Nick", ["Nick", "Sashwat", "Leif"], 32.48),
    #             exp("exp 3", "Sashwat", ["Nick", "Sashwat", "Leif"], 72),
    #             exp("exp 4", "Leif", [
    #                 "Nick", "Sashwat", "Leif", "Porter"], 18),
    #             exp("exp 5", "Leif", ["Leif", "Porter"], 12)]
    # members = [mem("Nick", True), mem("Porter", False),
    #            mem("Sashwat", False), mem("Leif", False)]
    # Initialize member balances from testing data
    # for exp1 in expenses:
    #     members = distribute_expense(exp1, members)

    members, expenses = read_info_from_file()
    reimbursements = get_reimbursements(members)

    expense_table_header = ['Expense Name', 'Payer', 'Amount']
    reimbursement_table_header = ['Debtor / Creditor', 'Amount']

    right_box_menu = [
        [sg.Button('Add Expense', size=(15, 1.5), font=('Helvetica', 15))],
        [sg.Table(headings=reimbursement_table_header,
                  values=generate_reimbursement_table_rows(reimbursements),
                  justification='center', expand_x=True, expand_y=True,
                  key='-REIMBURSEMENT_TABLE-',
                  auto_size_columns=True, display_row_numbers=False,
                  row_height=30, font=('Helvetica', 15))],
        [sg.Text(my_balance(members),
                 font=('Helvetica', 15), key='-MY_BALANCE-'),
         sg.VerticalSeparator(),
         sg.Text(total_expense_amount(expenses),
                 font=('Helvetica', 15), key='-TOTAL_EXPENSE_AMOUNT-')],
        [sg.Button('Save and Quit', size=(12, 1), font=('Helvetica', 13))]
    ]

    main_menu_layout = [
        [sg.Table(headings=expense_table_header,
                  values=generate_expense_table_rows(expenses),
                  justification='center', expand_x=True, expand_y=True,
                  key='-EXPENSE_TABLE-', auto_size_columns=True,
                  display_row_numbers=False, row_height=30,
                  font=('Helvetica', 15), enable_events=True),
         sg.VSeparator(),
         sg.Column(right_box_menu, expand_y=True, expand_x=True, element_justification='center')]
    ]

    add_expense_layout = [
        [sg.Text('Add Expense', font=('Helvetica', 15))],

        # Expense name
        [sg.Text('Expense Name:', size=(12, 1)),
         sg.Input(key='-EXPENSE_NAME-', size=(20, 1), do_not_clear=False, expand_x=True)],

        [sg.HorizontalSeparator()],

        # Who paid
        [sg.Text('Who Paid:', size=(12, 1)),
         sg.Column([
             [sg.Radio(member.name, "payee-radio-group",
                       key=f'-PAYER-RADIO-{member.name}-')] for member in members
         ])],

        [sg.HorizontalSeparator()],

        # Amount
        [sg.Text('Amount:', size=(12, 1)),
         sg.Input(key='-AMOUNT-', size=(20, 1), do_not_clear=False, expand_x=True)],

        [sg.HorizontalSeparator()],

        # Payee selection
        [sg.Text('Select Names:', size=(12, 1)),
         sg.Column([
             [sg.Checkbox(member.name,
                          key=f'-PAYEE-{member.name}-', default=True)] for member in members
         ])],

        [sg.HorizontalSeparator()],

        [sg.Button('Submit', key='-EXPENSE_SUBMIT_BTN-'),
         sg.Button('Cancel', key='-EXPENSE_CANCEL_BTN-')]
    ]

    layout = [
        [sg.Text('Group Name', font=('Helvetica', 25), expand_x=True)],
        [sg.Column(main_menu_layout, key='-MAIN_MENU-', expand_x=True, expand_y=True),
         sg.Column(add_expense_layout, key='-ADD_EXPENSE-', visible=False, expand_x=True, expand_y=True)]
    ]

    # Create the resizable window
    window = sg.Window('Group Expense Tracker', layout,
                       resizable=True, size=(1000, 600))

    # Event loop
    while True:
        event, values = window.read()  # type: ignore
        if event == sg.WINDOW_CLOSED or event == 'Save and Quit':
            break
        elif event == 'Add Expense':
            window['-MAIN_MENU-'].update(visible=False)
            window['-ADD_EXPENSE-'].update(visible=True)
        elif event == '-EXPENSE_SUBMIT_BTN-':
            amount_str = values['-AMOUNT-']

            # Get who paid
            who_paid = None
            for member in members:
                if values[f'-PAYER-RADIO-{member.name}-']:
                    who_paid = member.name

            if who_paid == None:
                # Check to make sure a selection was made
                sg.popup_error('Please select who paid for this expense.')

            elif not is_valid_amount(amount_str):
                # Checks that amount is actually a number
                sg.popup_error('Please enter a valid number for the amount.')

            else:
                # Get the amount for the expense
                new_amount = round(float(values['-AMOUNT-']), 2)

                # Get payees
                new_payees_arr = []
                for member in members:
                    if values[f'-PAYEE-{member.name}-']:
                        new_payees_arr.append(member.name)

                # Make the new expense
                new_expense = exp(values['-EXPENSE_NAME-'],
                                  who_paid,
                                  new_payees_arr,
                                  new_amount)
                expenses = [new_expense] + expenses  # Add to front of array

                update_window_new_expense(
                    expenses=expenses, members=members, window=window)

                # switch all checkboxes back to checked
                for member in members:
                    window[f'-PAYEE-{member.name}-'].update(True)

                # switch back to main window
                window['-MAIN_MENU-'].update(visible=True)
                window['-ADD_EXPENSE-'].update(visible=False)
        elif event == '-EXPENSE_CANCEL_BTN-':
            window['-MAIN_MENU-'].update(visible=True)
            window['-ADD_EXPENSE-'].update(visible=False)
        elif event == '-EXPENSE_TABLE-':
            if len(values[event]) != 0:
                expense_index = values[event][0]

                choice = sg.popup_yes_no(get_expense_popup_text(expenses[expense_index]),
                                         no_titlebar=True, font=('Helvetica', 13),
                                         background_color='black', grab_anywhere=True)
                if choice == 'Yes':
                    expenses.pop(expense_index)

                    update_window_new_expense(
                        expenses=expenses, members=members, window=window)

    # Close the window
    window.close()

    save_info_to_file(members=members, expenses=expenses)


if __name__ == "__main__":
    main()
