import PySimpleGUI as gui
import cv2
import time

gui.theme("LightGrey1")
progress = False
lock = True
bar = 0
cam = ['1920 x 1080', '1280 x 720','960 x 720', '640 x 480']

def LEDIndicator(key=None, radius=30):
    return gui.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 25, fill_color=color, line_color=color)

file_list_column = [
    [gui.Image(filename = "/home/samsonchau/python_script/script/gui_test/ASTRI_Logo.png",size = (360,120))],
    [gui.Text("Smart Lock System", font='FreeSerif 36', text_color='dark blue',size=(16, 2), key="txt")],
    [gui.Text("Door Locked!", size=(20, 2), font='FreeSerif 18', text_color='dark blue', key='msg')],
    [gui.Button('unlock'), gui.Button('lock'), gui.Button('detect')],
    [gui.Text('Door State', text_color='dark blue'), LEDIndicator('led')]
]

image_viewer_column = [
    [gui.Text("Camera: ", text_color='dark blue')],
    [gui.Image(filename="", key="image", size = (1920,1080))],
    [gui.ProgressBar(10000, orientation='h', size=(20, 20), key='progressbar'),],
    [gui.Text("FPS: ", text_color='dark blue'), gui.Text("", text_color='dark blue', key='fps')],
    [gui.Text("width: ", text_color='dark blue'), gui.Text("640", text_color='dark blue', key='v_width')],
    [gui.Text("height: ", text_color='dark blue'), gui.Text("480", text_color='dark blue', key='v_height')],
    [gui.Text("channel: ", text_color='dark blue'), gui.Text("3", text_color='dark blue', key='v_channel')],
    [gui.Text("video format: ", text_color='dark blue'), gui.Combo(values=cam , key = 'spec'), gui.Button('set')],
]
layout = [
    [gui.Column(file_list_column),gui.VSeperator(),gui.Column(image_viewer_column),]
]

window = gui.Window("HPST", layout)
progress_bar = window['progressbar']


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)


start = time.time()
last = start

while True:
    event, values = window.read(timeout = 40)
    if event == 'Exit' or event == gui.WIN_CLOSED:
        break
    
    try: 
        ret, frame = cap.read()
        seconds = time.time() - last
        last = time.time()
        fps = fps  = 1 / seconds
        #print(fps)
        #image = cv2.resize(frame, (int(frame.shape[1] * .35), int(frame.shape[0] * .35)))
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['image'].update(data=imgbytes)
        window['fps'].update(str(fps))
        window['v_height'].update(str(frame.shape[0]))
        window['v_width'].update(str(frame.shape[1]))
        window['v_channel'].update(str(frame.shape[2]))
        
    except:
        print("error in runing video stream.")
        pass

    if event == 'detect':
        window['msg'].update("People is detected")

    if event == 'unlock':
        progress = True
        
    if event == 'lock':
        progress = False
        lock = True 
        window['msg'].update("Door is locked!")

    if event == 'set':
        format = values['spec']
        if format == '1920 x 1080':
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            cap.set(cv2.CAP_PROP_FPS, 6)
        if format == '1280 x 720' :
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv2.CAP_PROP_FPS, 30)
        if format == '960 x 720' :
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv2.CAP_PROP_FPS, 30)
        if format == '640 x 480' :
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 60)
    
    if progress:
        if bar <10000 and lock == True:
            progress_bar.UpdateBar(bar)
            bar += 100
        else:
            lock = False
            bar = 0
            progress_bar.UpdateBar(0)
            window['msg'].update("Door is open!")
            progress = False
    else:
        bar = 0
        progress_bar.UpdateBar(0)

    SetLED(window, 'led', 'green' if not lock else 'red')
    
window.close()
exit(0)