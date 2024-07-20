import os
import shutil
#import json
import PySimpleGUI as sg # type: ignore

sg.theme('DarkGrey 15')
#sg.theme('PythonPlus')

def item_row(item_num):

    row = [sg.pin(sg.Col([[sg.B("DEL", button_color='black on #FF8C00', border_width=0, k=('-DEL-', item_num), tooltip='Delete this item'),
          sg.Text(f'File {item_num}:'), sg.FileBrowse(key=f'-FILE{item_num}-'),
          sg.Text(f'File {item_num}:'), sg.FileBrowse(key=f'-FILE{item_num}-'),
          sg.T(f'Key {item_num}')]], k=('-ROW-', item_num)))]
    return row

def make_window():

    
    layout = [  [sg.Text('This is some text :)', font='_ 15')],
              [sg.HorizontalSeparator()],
              [sg.Col([item_row(0)], k='-SAVELOCATION-')],
              [sg.T('ADD MORE', enable_events=True, k='Add Item', tooltip='Add Another Item')],
              [sg.HorizontalSeparator()],
              [sg.Button("Compare and Copy", border_width=0, button_color='black on #CAFF70')],
              [sg.Button('Exit', border_width=0, button_color='black on red')] 
            ]
    right_click_menu = [[''], ['Add Item', 'About']]

    window = sg.Window('Save Game Comparison Tool', layout, right_click_menu=right_click_menu, use_default_focus=False, font='_ 15', metadata=0)

    return window


def compare_and_copy_files():
    window = make_window()
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Add Item':
            window.metadata += 1
            window.extend_layout(window['-SAVELOCATION-'], [item_row(window.metadata)])
        elif event == 'About':
            sg.popup("Version 0.1 from https://github.com/AWKatz", keep_on_top=True, non_blocking=True)
        elif event[0] == '-DEL-':
            window[('-ROW-', event[1])].update(visible=False)
        
        # Compares the user selected files
        elif event == "Compare and Copy":
            for i in range(window.metadata + 1):
                file1_path = values.get(f"-FILE{i}-")
                file2_path = values.get(f"-FILE{i}-")

                if file1_path and file2_path:
                    try:
                        time1 = os.path.getmtime(file1_path)
                        time2 = os.path.getmtime(file2_path)

                        if time1 > time2:
                            shutil.copy2(file1_path, file2_path)
                            sg.popup(f"{file1_path} is newer. Copied to {file2_path}")
                        elif time2 > time1:
                            shutil.copy2(file2_path, file1_path)
                            sg.popup(f"{file2_path} is newer. Copied to {file1_path}")
                        else:
                            sg.popup("Files are in sync, both files have the same modification time.")
                    except FileNotFoundError:
                        sg.popup(f"Files not found for row {i}. Check the paths and try again.")

    window.close()

# Call the function
compare_and_copy_files()