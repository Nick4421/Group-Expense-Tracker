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
