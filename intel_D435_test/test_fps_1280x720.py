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
color_frequency = 15
depth_frequency = 15
IR_frequency = 15
i=0

if __name__ == '__main__' :
    print("Start frame capture...")
    print("Start video streamig")
    points = rs.points()
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
    config.enable_stream(rs.stream.depth, depthwidth, depthheight, rs.format.z16, depth_frequency)  # depth
    config.enable_stream(rs.stream.color, colorwidth, colorheight, rs.format.bgr8, color_frequency) # rgb
    config.enable_stream(rs.stream.infrared, 1, IRwidth, IRheight, rs.format.y8, IR_frequency)         # IR
    stream = pipeline.start(config)

    align_to = rs.stream.color
    align = rs.align(align_to)

    start_time = time.time()
    last_time = start_time
    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            frame_time = time.time() - last_time
            print("fps: ", 1 / frame_time)
            

            # Align the depth frame to color frame
            aligned_frames = align.process(frames) 
            depth_frame = aligned_frames.get_depth_frame() 
            color_frame = aligned_frames.get_color_frame()
            infrared_frame = aligned_frames.first(rs.stream.infrared)
            
            # Convert images to numpy arrays
            depth_array = np.asanyarray(depth_frame.get_data())
            color_array = np.asanyarray(color_frame.get_data())
            IR_array = np.asanyarray(infrared_frame.get_data())
            
            # Apply colormap on depth image 
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_array, alpha=0.01), cv2.COLORMAP_JET)
            # Stack both images horizontally
            depth_color_images = np.hstack((color_array, depth_colormap))
            #depth_color_images = depth_colormap

            last_time = time.time()
            #video = np.concatenate((color_array,depth_color_images,IR_array), axis=1)
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('video', IR_array)
            #cv2.imshow('depth_raw', depth_frame)
            #cv2.imshow('depth_color', depth_colormap)
            #cv2.imshow('color_raw', color_frame)
            
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
