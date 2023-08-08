import PySimpleGUI as sg

# Example expense data
expense_data = [
    ['Groceries', '$50'],
    ['Dinner', '$30'],
    ['Gas', '$40']
]

layout = [
    [sg.Text('Delete Expense', font=('Helvetica', 14), justification='center')],
    [sg.Text('Select an expense to delete:', justification='center')],
    [sg.Listbox(values=[f"{expense[0]} ({expense[1]})" for expense in expense_data],
                size=(30, 5),
                key='-EXPENSE-LIST-')],
    [sg.Button('Delete Expense'), sg.Button('Cancel')]
]

window = sg.Window('Delete Expense Popup', layout)

while True:
    event, values = window.read()  # type: ignore

    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == 'Delete Expense':
        selected_expense_index = values['-EXPENSE-LIST-'][0]
        if selected_expense_index is not None:
            del expense_data[selected_expense_index]
            sg.popup('Expense deleted successfully!',
                     auto_close=True, auto_close_duration=2)
        else:
            sg.popup('Please select an expense to delete!',
                     auto_close=True, auto_close_duration=2)

window.close()
