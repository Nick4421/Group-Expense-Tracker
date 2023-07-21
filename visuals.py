import PySimpleGUI as sg

# Sample data for the list
list_data = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']

# Define the layout with the specified components
layout = [
    [sg.Text('Title of the Project', font=('Helvetica', 20))],
    [
        sg.Listbox(values=list_data, size=(30, 10),
                   enable_events=True, key='-LIST-'),
        sg.Column([
            [sg.Button('Button')],
            [sg.Text('Some Text')],
        ], expand_y=True, element_justification='center')
    ]
]

# Create the window
window = sg.Window('Project Layout', layout)

# Event loop
while True:
    event, values = window.read()  # type: ignore
    if event == sg.WINDOW_CLOSED:
        break

# Close the window
window.close()
