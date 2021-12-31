from flask import *
import os
from threading import Thread
import pyrealsense2 as rs
import numpy as np
import time
import cv2

# Device config
device_id = '819112071956'  # serial number of device D455
colorwidth = 1280
colorheight = 720
depthwidth = 1280
depthheight = 720
IRwidth = 1280
IRheight = 720
color_frequency = 15
depth_frequency = 15
IR_frequency = 15
i=0

#cv2 config 
font = cv2.FONT_HERSHEY_SIMPLEX

#Initialize the Flask
app = Flask(__name__)

#init camera
print("Start frame capture...")
print("Start video streamig")
pipeline = rs.pipeline()

# Configure streams
print ("Device:", device_id, " enabled!")
print("colorwidth: ", colorwidth)
print("colorheight: ", colorheight)
print("depthwidth: ", depthwidth)
print("depthheight: ", depthheight)
print("ir width: ", IRwidth)
print("ir height: ", IRheight)

colorizer = rs.colorizer()
config = rs.config()
config.enable_device(device_id)
config.enable_stream(rs.stream.infrared, 1, IRwidth, IRheight, rs.format.y8, IR_frequency)          # IR 1
config.enable_stream(rs.stream.infrared, 2, IRwidth, IRheight, rs.format.y8, IR_frequency)          # IR 2
config.enable_stream(rs.stream.color, colorwidth, colorheight, rs.format.bgr8, color_frequency)     # rgb
config.enable_stream(rs.stream.depth, depthwidth, depthheight, rs.format.z16, depth_frequency)      # depth

if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
    stream = pipeline.start(config)

align_to = rs.stream.color
align = rs.align(align_to)

def gen_frames():

    start_time = time.time()
    last_time = start_time
    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            frame_time = time.time() - last_time
            fps = 1 / frame_time
            print("fps: ", fps)
            
            # Align the depth frame to color frame
            aligned_frames = align.process(frames)
            ir_frame_1 = frames.get_infrared_frame(1)
            ir_frame_2  = frames.get_infrared_frame(2) 
            depth_frame = aligned_frames.get_depth_frame() 
            color_frame = aligned_frames.get_color_frame()
        
            # Convert images to numpy arrays
            ir_colormap_1 = np.asanyarray(colorizer.colorize(ir_frame_1).get_data())
            ir_colormap_2 = np.asanyarray(colorizer.colorize(ir_frame_2).get_data())
            depth_array = np.asanyarray(colorizer.colorize(depth_frame).get_data())
            color_array = np.asanyarray(colorizer.colorize(color_frame).get_data())
            cv2.putText(color_array, str(fps), (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
            img = np.hstack((color_array, depth_array))
            last_time = time.time()
            imgbytes = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + imgbytes + b'\r\n')  
                   # concat frame one by one and show result
    except rs.error as e:
        # Method calls agaisnt librealsense objects may throw exceptions of type pylibrs.error
        print("pylibrs.error was thrown when calling %s(%s):\n", (e.get_failed_function(), e.get_failed_args()))
        print("    %s\n", e.what())
        exit(1)
    except Exception as e:
        print(e)
        pass

    finally:
        # Stop streaming & exit 
        pipeline.stop()
        exit(0)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", Door = 0)
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/unlock", methods=["GET", "POST"])
def unlock():
    if request.method == "GET":
        return render_template("index.html", Door = 0)
    return render_template("index.html", Door = 0)


if __name__=="__main__":
    Ethernet_stream = Thread(target = app.run(host='0.0.0.0', port = 5000, debug=True, threaded=True))
    Ethernet_stream.start()