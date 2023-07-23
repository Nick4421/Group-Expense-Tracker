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

exp_name_list = [
    [sg.Text(exp.expense_name, font=('Helvetica', 18))] for exp in expenses
]

exp_amount_list = [
    [sg.Text(str(exp.amount), font=('Helvetica', 18))] for exp in expenses
]

exp_payer_list = [
    [sg.Text(exp.payer, font=('Helvetica', 18))] for exp in expenses
]

expense_list_viewer = [
    [sg.Column(exp_name_list, element_justification='center'),
     sg.Column(exp_amount_list, element_justification='center'),
     sg.Column(exp_payer_list, element_justification='center')]
]

right_box_menu = [
    [sg.Button('Add Expense', size=(15, 2))],
    [sg.Listbox(values=list_data, size=(35, 5), enable_events=True,
                key='-LIST2-', expand_y=True, expand_x=True, font=('Helvetica', 18))],
    [sg.Text('Text 1', font=('Helvetica', 15)),
     sg.Text('Text 2', font=('Helvetica', 15))],
]

main_menu_layout = [
    [sg.Column(expense_list_viewer, scrollable=True, size=(400, 400), vertical_scroll_only=True,
               expand_x=True, expand_y=True),
     sg.VSeparator(),
     sg.Column(right_box_menu, expand_y=True, expand_x=True, element_justification='center')]
]

add_expense_layout = [
    [sg.Text('Add Expense')],
    [sg.Text('Expense Name:', size=(12, 1)),
     sg.Input(key='-EXPENSE_NAME-', size=(20, 1))],
    [sg.Text('Amount:', size=(12, 1)),
     sg.Input(key='-AMOUNT-', size=(20, 1))],
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
     sg.Column(add_expense_layout, key='-ADD_EXPENSE-', visible=False)]
]

# Create the resizable window
window = sg.Window('Group Expense Tracker', layout, resizable=True)

# Event loop
while True:
    event, values = window.read()  # type: ignore
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Add Expense':
        window['-MAIN_MENU-'].update(visible=False)
        window['-ADD_EXPENSE-'].update(visible=True)
    if event == '-EXPENSE_SUBMIT_BTN-':
        print(values['-EXPENSE_NAME-'],
              values['-AMOUNT-'],
              )
        selected_names = [mem for mem in members if values[f'-PAYEE-{mem}-']]
        print(selected_names)

# Close the window
window.close()
