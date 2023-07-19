import PySimpleGUI as psg

layout = [[psg.Text("Hello, PySimpleGUI!")]]
window = psg.Window("Test Window", layout, finalize=True)

while True:
    event, values = window.read()
    if event == psg.WINDOW_CLOSED:
        break

window.close()
