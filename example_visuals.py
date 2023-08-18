import PySimpleGUI as sg
from expense_group import expense_group as eg
from expense import expense as exp
from member import member as mem

expenses1 = [exp("exp 1", "Nick", ["Nick", "Porter", "Sashwat", "Leif"], 49.60),
             exp("exp 2", "Nick", ["Nick", "Sashwat", "Leif"], 32.48),
             exp("exp 3", "Sashwat", ["Nick", "Sashwat", "Leif"], 72),
             exp("exp 4", "Leif", ["Nick", "Sashwat", "Leif", "Porter"], 18),
             exp("exp 5", "Leif", ["Leif", "Porter"], 12)]

members1 = [mem("Nick", True), mem("Porter", False),
            mem("Sashwat", False), mem("Leif", False)]

expenses2 = [exp("exp 1", "Nick", ["Nick", "Porter", "Sashwat", "Leif"], 49.60),
             exp("exp 2", "Nick", ["Nick", "Sashwat", "Leif"], 32.48),
             exp("exp 3", "Sashwat", ["Nick", "Sashwat", "Leif"], 72),
             exp("exp 4", "Leif", ["Nick", "Sashwat", "Leif", "Porter"], 18),
             exp("exp 5", "Leif", ["Leif", "Porter"], 12)]

members2 = [mem("Nick", True), mem("Porter", False),
            mem("Sashwat", False), mem("Leif", False)]

groups = (eg(group_name="group 1", members=members1, expenses=expenses1),
          eg(group_name="group 2", members=members2, expenses=expenses2))

header = ['Group Name', 'Members']


def generate_groups_rows(groups):
    num_groups = len(groups)
    final_rows = []
    all_members_names = []

    for group in groups:
        member_names = []
        for member in group.members:
            member_names.append(member.name)
        all_members_names.append(', '.join(member_names))

    for i in range(num_groups):
        final_rows.append(
            [groups[i].group_name, all_members_names[i]]
        )

    return final_rows


group_layout = [
    [sg.Table(headings=header, values=generate_groups_rows(groups),
              justification='center', expand_x=True, expand_y=True,
              key='-GROUP_TABLE-', auto_size_columns=True,
              display_row_numbers=False, row_height=30,
              font=('Helvetica', 15), enable_events=True)]
]

layout = [
    [sg.Column(group_layout, expand_x=True, expand_y=True)]
]

window = sg.Window('group expenses example', layout,
                   resizable=True, size=(1000, 600))

while True:
    event, values = window.read()  # type: ignore

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()
