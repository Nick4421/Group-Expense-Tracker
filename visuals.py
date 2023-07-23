import PySimpleGUI as sg
from expense import expense as exp

expenses = [exp("exp 1", "Nick", ["Nick", "Porter", "Sashwat", "Leif"], 49.60),
            exp("exp 2", "Nick", ["Nick", "Sashwat", "Leif"], 32.48),
            exp("exp 3", "Sashwat", ["Nick", "Sashwat", "Leif"], 72),
            exp("exp 4", "Leif", ["Nick", "Sashwat", "Leif", "Porter"], 18),
            exp("exp 5", "Leif", ["Leif", "Porter"], 12)]

# Sample data for the list
list_data = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']
members = ["Nick", "Sashwat", "Porter", "Leif"]
table_header = ['Expense Name', 'Payer', 'Amount']


def generate_table_rows(expenses):
    exp_list = [
        [exp.expense_name, exp.payer, exp.amount] for exp in expenses
    ]

    return exp_list


right_box_menu = [
    [sg.Button('Add Expense', size=(15, 2))],
    [sg.Listbox(values=list_data, size=(30, 5), enable_events=True,
                key='-LIST2-', expand_y=True, expand_x=True, font=('Helvetica', 18))],
    [sg.Text('Text 1', font=('Helvetica', 15)),
     sg.Text('Text 2', font=('Helvetica', 15))]
]

main_menu_layout = [
    [sg.Table(headings=table_header, values=generate_table_rows(expenses),
              justification='center', expand_x=True, expand_y=True, key='-EXPENSE_TABLE-',
              auto_size_columns=True, display_row_numbers=False, row_height=30,
              font=('Helvetica', 15)),
     sg.VSeparator(),
     sg.Column(right_box_menu, expand_y=True, expand_x=True, element_justification='center')]
]

add_expense_layout = [
    [sg.Text('Add Expense', font=('Helvetica', 15))],
    [sg.Text('Expense Name:', size=(12, 1)),
     sg.Input(key='-EXPENSE_NAME-', size=(20, 1), do_not_clear=False, expand_x=True)],

    [sg.Text('Who Paid:', size=(12, 1)),
     sg.Input(key='-WHO_PAID-', size=(20, 1), do_not_clear=False, expand_x=True)],

    [sg.Text('Amount:', size=(12, 1)),
     sg.Input(key='-AMOUNT-', size=(20, 1), do_not_clear=False, expand_x=True)],

    [sg.Text('Select Names:', size=(12, 1)),
     sg.Column([
         [sg.Checkbox(mem, key=f'-PAYEE-{mem}-', default=True)] for mem in members
     ])],

    [sg.Button('Submit', key='-EXPENSE_SUBMIT_BTN-'),
     sg.Button('Cancel', key='-EXPENSE_CANCEL_BTN-')]
]

# Define the layout with the specified components
layout = [
    [sg.Text('Group Name', font=('Helvetica', 20), expand_x=True)],
    [sg.Column(main_menu_layout, key='-MAIN_MENU-', expand_x=True, expand_y=True),
     sg.Column(add_expense_layout, key='-ADD_EXPENSE-', visible=False, expand_x=True, expand_y=True)]
]

# Create the resizable window
window = sg.Window('Group Expense Tracker', layout, resizable=True)

# Event loop
while True:
    event, values = window.read()  # type: ignore
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Add Expense':
        window['-MAIN_MENU-'].update(visible=False)
        window['-ADD_EXPENSE-'].update(visible=True)
    elif event == '-EXPENSE_SUBMIT_BTN-':
        # Add the expense to the expenses array
        new_expense = exp(values['-EXPENSE_NAME-'],
                          values['-WHO_PAID-'],
                          [mem for mem in members if values[f'-PAYEE-{mem}-']],
                          float(values['-AMOUNT-']))
        expenses = [new_expense] + expenses  # Add to front of array

        # update the window so new expense shows
        window['-EXPENSE_TABLE-'].update(values=generate_table_rows(expenses))

        # switch all checkboxes back to checked
        # TODO

        # switch back to main window
        window['-MAIN_MENU-'].update(visible=True)
        window['-ADD_EXPENSE-'].update(visible=False)
    elif event == '-EXPENSE_CANCEL_BTN-':
        window['-MAIN_MENU-'].update(visible=True)
        window['-ADD_EXPENSE-'].update(visible=False)

# Close the window
window.close()
