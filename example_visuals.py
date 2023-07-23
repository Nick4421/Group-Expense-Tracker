import PySimpleGUI as sg

# Sample data for the list of names (you may replace this with your actual data)
names = ['John', 'Alice', 'Bob', 'Eve']

# Define the layout
layout = [
    [sg.Text('Expense Name:', size=(12, 1)),
     sg.Input(key='-EXPENSE-', size=(20, 1))],
    [sg.Text('Amount:', size=(12, 1)), sg.Input(key='-AMOUNT-', size=(20, 1))],
    [sg.Text('Select Names:', size=(12, 1)),
     sg.Column([
         [sg.Checkbox(name, key=f'-CHECKBOX-{name}-')] for name in names
     ])],
    [sg.Button('Submit'), sg.Button('Cancel')]
]

# Create the window
window = sg.Window('Expense Tracker', layout)

# Event loop
while True:
    event, values = window.read()  # type: ignore
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break
    elif event == 'Submit':
        # Get the entered expense name and amount
        expense_name = values['-EXPENSE-']
        amount = values['-AMOUNT-']

        # Get the selected names from checkboxes
        selected_names = [
            name for name in names if values[f'-CHECKBOX-{name}-']]

        # Process the entered data (you can add your logic here)

        # Print the entered data for demonstration purposes
        print(f'Expense Name: {expense_name}')
        print(f'Amount: {amount}')
        print(f'Selected Names: {selected_names}')

# Close the window
window.close()


# import PySimpleGUI as sg
# from expense import expense as exp

# expenses = [exp("exp 1", "Nick", ["Nick", "Porter", "Sashwat", "Leif"], 49.60),
#             exp("exp 2", "Nick", ["Nick", "Sashwat", "Leif"], 32.48),
#             exp("exp 3", "Sashwat", ["Nick", "Sashwat", "Leif"], 72),
#             exp("exp 4", "Leif", ["Nick", "Sashwat", "Leif", "Porter"], 18),
#             exp("exp 5", "Leif", ["Leif", "Porter"], 12)]

# # Sample data for the list
# list_data = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']
# members = ["Nick", "Sashwat", "Porter", "Leif"]


# def generate_expense_list(expenses):
#     exp_name_list = [
#         [sg.Text(exp.expense_name, font=('Helvetica', 18))] for exp in expenses
#     ]

#     exp_amount_list = [
#         [sg.Text(str(exp.amount), font=('Helvetica', 18))] for exp in expenses
#     ]

#     exp_payer_list = [
#         [sg.Text(exp.payer, font=('Helvetica', 18))] for exp in expenses
#     ]

#     expense_list_viewer = [
#         [sg.Column(exp_name_list, element_justification='center'),
#          sg.Column(exp_amount_list, element_justification='center'),
#          sg.Column(exp_payer_list, element_justification='center')]
#     ]
#     return expense_list_viewer


# right_box_menu = [
#     [sg.Button('Add Expense', size=(15, 2))],
#     [sg.Listbox(values=list_data, size=(35, 5), enable_events=True,
#                 key='-LIST2-', expand_y=True, expand_x=True, font=('Helvetica', 18))],
#     [sg.Text('Text 1', font=('Helvetica', 15)),
#      sg.Text('Text 2', font=('Helvetica', 15))]
# ]

# main_menu_layout = [
#     [sg.Column(generate_expense_list(expenses), scrollable=True, size=(400, 400), vertical_scroll_only=True,
#                expand_x=True, expand_y=True, key='-EXPENSE_LIST-'),
#      sg.VSeparator(),
#      sg.Column(right_box_menu, expand_y=True, expand_x=True, element_justification='center')]
# ]

# add_expense_layout = [
#     [sg.Text('Add Expense')],
#     [sg.Text('Expense Name:', size=(12, 1)),
#      sg.Input(key='-EXPENSE_NAME-', size=(20, 1))],

#     [sg.Text('Who Paid:', size=(12, 1)),
#      sg.Input(key='-WHO_PAID-', size=(20, 1))],

#     [sg.Text('Amount:', size=(12, 1)),
#      sg.Input(key='-AMOUNT-', size=(20, 1))],

#     [sg.Text('Select Names:', size=(12, 1)),
#      sg.Column([
#          [sg.Checkbox(mem, key=f'-PAYEE-{mem}-', default=True)] for mem in members
#      ])],

#     [sg.Button('Submit', key='-EXPENSE_SUBMIT_BTN-'),
#      sg.Button('Cancel', key='-EXPENSE_CANCEL_BTN-')]
# ]

# # Define the layout with the specified components
# layout = [
#     [sg.Text('Group Name', font=('Helvetica', 20), expand_x=True)],
#     [sg.Column(main_menu_layout, key='-MAIN_MENU-', expand_x=True, expand_y=True),
#      sg.Column(add_expense_layout, key='-ADD_EXPENSE-', visible=False)]
# ]

# # Create the resizable window
# window = sg.Window('Group Expense Tracker', layout, resizable=True)

# # Event loop
# while True:
#     event, values = window.read()  # type: ignore
#     if event == sg.WINDOW_CLOSED:
#         break
#     elif event == 'Add Expense':
#         window['-MAIN_MENU-'].update(visible=False)
#         window['-ADD_EXPENSE-'].update(visible=True)
#     elif event == '-EXPENSE_SUBMIT_BTN-':
#         # Add the expense to the expenses array
#         new_expense = exp(values['-EXPENSE_NAME-'],
#                           values['-WHO_PAID-'],
#                           [mem for mem in members if values[f'-PAYEE-{mem}-']],
#                           float(values['-AMOUNT-']))
#         expenses.append(new_expense)

#         # update the window so new expense shows
#         new_expense_list = generate_expense_list(expenses)
#         window['-EXPENSE_LIST-'].update(layout=new_expense_list)

#         # switch back to main window
#         window['-MAIN_MENU-'].update(visible=True)
#         window['-ADD_EXPENSE-'].update(visible=False)
#     elif event == '-EXPENSE_CANCEL_BTN-':
#         window['-MAIN_MENU-'].update(visible=True)
#         window['-ADD_EXPENSE-'].update(visible=False)

# # Close the window
# window.close()
