import PySimpleGUI as sg

# ----------- Create the 3 layouts this Window will display -----------
layout1 = [[sg.Text('Enter your name and email address to register')],
           [sg.Text('Name: '), sg.Input(key='-NAME-')],
           [sg.Text('Email Address: '), sg.Input(key='-EMAIL_ADDRESS-')]]

layout2 = [[sg.Text('Enter your vote:')],
           [sg.Radio('Trump', 'vote')],
           [sg.Radio('Biden', 'vote')]]

layout3 = [[sg.Text('Thanks for voting!')]]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [[sg.Column(layout1, key='-COL1-'),
           sg.Column(layout2, visible=False, key='-COL2-'),
           sg.Column(layout3, visible=False, key='-COL3-')],
          [sg.Button('Next'), sg.Button('Return to Start'), sg.Button('Exit')]]

window = sg.Window('Dynamic Window', layout)

layout = 1  # The currently visible layout
while True:
    event, values = window.read()  # type: ignore
    if event in (None, 'Exit'):
        break
    if event == 'Next':
        print(layout)
        window[f'-COL{layout}-'].update(visible=False)
        if layout < 3:
            layout += 1
            window[f'-COL{layout}-'].update(visible=True)
        else:
            window[f'-COL3-'].update(visible=True)
    elif event == 'Return to Start':
        window[f'-COL{layout}-'].update(visible=False)
        window[f'-COL1-'].update(visible=True)
        layout = 1
window.close()
