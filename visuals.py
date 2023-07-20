import PySimpleGUI as sg

# Sample data for the list
list_data = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10',
             'Item 11', 'Item 12', 'Item 13', 'Item 14', 'Item 15', 'Item 16', 'Item 17', 'Item 18', 'Item 19', 'Item 20']

# Define the layout with expandable elements
layout = [
    [sg.Text('Scrollable List Example', font=('Helvetica', 20), expand_x=True)],
    [sg.Listbox(values=list_data, size=(30, 10), enable_events=True,
                key='-LIST-', expand_x=True, expand_y=True)],
    [sg.Button('Submit', size=(10, 2))]
]

# Create the window with grab_anywhere option for resizing
window = sg.Window('Scrollable List', layout,
                   resizable=True, grab_anywhere=True)

# Event loop
while True:
    event, values = window.read()  # type: ignore
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Submit':
        selected_items = values['-LIST-']
        sg.popup(f'Selected item(s): {", ".join(selected_items)}')

# Close the window
window.close()
