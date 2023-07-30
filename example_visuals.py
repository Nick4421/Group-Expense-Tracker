import PySimpleGUI as sg

# Define the layout of the GUI
layout = [
    [sg.Text("Select one option:")],
    [sg.Radio("Option 1", "radio_group", key="-OPTION1-")],
    [sg.Radio("Option 2", "radio_group", key="-OPTION2-")],
    [sg.Radio("Option 3", "radio_group", key="-OPTION3-")],
    [sg.Button("Submit", key="-SUBMIT-")],
]

# Create the window
window = sg.Window("Multiple Choice Bubbles", layout)

# Event loop
while True:
    event, values = window.read()  # type: ignore

    # Exit the loop if the window is closed
    if event == sg.WINDOW_CLOSED:
        break

    # Handle the button click event
    if event == "-SUBMIT-":
        # Retrieve the selected option
        selected_option = None
        if values["-OPTION1-"]:
            selected_option = "Option 1"
        elif values["-OPTION2-"]:
            selected_option = "Option 2"
        elif values["-OPTION3-"]:
            selected_option = "Option 3"

        # Show the selected option in a popup
        sg.popup(f"Selected Option: {selected_option}")

# Close the window when the loop ends
window.close()
