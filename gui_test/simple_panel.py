import PySimpleGUI as gui
import os.path

file_list_column = [
    [
        gui.Text("Image Folder"),
        gui.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        gui.FolderBrowse(),
    ],
    [
        gui.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")
    ],
]

image_viewer_column = [
    [gui.Text("Choose an image from list on left:")],
    [gui.Text(size=(40, 1), key="-TOUT-")],
    [gui.Image(key="-IMAGE-")],
]

layout = [
    [
        gui.Column(file_list_column),
        gui.VSeperator(),
        gui.Column(image_viewer_column),
    ]
]

window = gui.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event  == "Exit" or  event == gui.WIN_CLOSED:
        break
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder,f))
            and f.lower().endswith((".png",".gif"))
        ]
        print(fnames)
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":
        try:
            print("Show file now")
            #for i in range(1,10000):
            #    gui.one_line_progress_meter('My Meter', i+1, 10000, 'key','Optional message')
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            print(filename)
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)
        except:
            pass
window.close()
exit(0)
