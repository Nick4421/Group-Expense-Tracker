import PySimpleGUI as sg

# Sample data for the list
list_data = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']

main_menu_layout = [
    [sg.Listbox(values=list_data, size=(55, 25), enable_events=True,
                key='-LIST-', expand_y=True, expand_x=True, font=('Helvetica', 18)),
     sg.VSeparator(),
     sg.Column([
         [sg.Button('Add Expense', size=(15, 2))],
         [sg.Listbox(values=list_data, size=(35, 5), enable_events=True,
                     key='-LIST2-', expand_y=True, expand_x=True, font=('Helvetica', 18))],
         [sg.Text('Text 1', font=('Helvetica', 15)),
             sg.Text('Text 2', font=('Helvetica', 15))],
     ], expand_y=True, expand_x=True, element_justification='center')]
]

add_expense_layout = [[sg.Text('Add Expense')]]

# Define the layout with the specified components
layout = [
    [sg.Text('Group Name', font=('Helvetica', 20), expand_x=True)],
    [sg.Column(main_menu_layout, key='-MAIN_MENU-'),
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

# Close the window
window.close()
