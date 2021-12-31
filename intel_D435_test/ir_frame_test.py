import pyrealsense2 as rs
import numpy as np
import time
import math
import cv2

# Device config
device_id = '819112071956'  # serial number of device D455
colorwidth = 1280
colorheight = 720
depthwidth = 1280
depthheight = 720
IRwidth = 1280
IRheight = 720
color_frequency = 6
depth_frequency = 6
IR_frequency = 6

if __name__ == '__main__' :
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

    config = rs.config()
    config.enable_device(device_id)
    config.enable_stream(rs.stream.infrared, 1, IRwidth, IRheight, rs.format.y8, IR_frequency)          # IR 1
    config.enable_stream(rs.stream.infrared, 2, IRwidth, IRheight, rs.format.y8, IR_frequency)          # IR 2
    config.enable_stream(rs.stream.color, colorwidth, colorheight, rs.format.bgr8, color_frequency)     # rgb
    config.enable_stream(rs.stream.depth, depthwidth, depthheight, rs.format.z16, depth_frequency)      # depth

    colorizer = rs.colorizer()
    stream = pipeline.start(config)
    #align_to = rs.stream.color
    #align = rs.align(align_to)

    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            
            # Align the depth frame to color frame
            #aligned_frames = align.process(frames)
            ir_frame_1 = frames.get_infrared_frame(1)
            ir_frame_2  = frames.get_infrared_frame(2) 
            depth_frame = frames.get_depth_frame() 
            color_frame = frames.get_color_frame()
        
            # Convert images to numpy arrays
            ir_colormap_1 = np.asanyarray(colorizer.colorize(ir_frame_1).get_data())
            ir_colormap_2 = np.asanyarray(colorizer.colorize(ir_frame_2).get_data())
            depth_array = np.asanyarray(colorizer.colorize(depth_frame).get_data())
            color_array = np.asanyarray(colorizer.colorize(color_frame).get_data())

            last_time = time.time()
            #images = np.hstack((depth_array, color_array))
            #images = np.hstack(( ir_colormap_1, ir_colormap_2))
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            #cv2.imshow('video', ir_colormap_1)
            cv2.imwrite("img/IR.jpg")
            time.sleep(1)
            # Press esc or 'q' to close the image window
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break

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
