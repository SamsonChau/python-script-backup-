import pyrealsense2 as rs
import numpy as np
import time
import cv2

print("Start frame capture...\r\n")
# Device config
device_id = '819112071956'  # serial number of device D455
colorwidth = 640
colorheight = 480
depthwidth = 640
depthheight = 480
fps = 30
i=0
print("Press 's' to capture the frame and 'q' to exit the program\r\n")

try:
    # Configure streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(device_id)

    print ("Device:", device_id, " enabled! \r\n")
    print("colorwidth: ", colorwidth)
    print("colorheight: ", colorheight)
    print("depthwidth: ", depthwidth)
    print("depthheight: ", depthheight)

    config.enable_stream(rs.stream.depth, depthwidth, depthheight, rs.format.z16, fps)  # depth
    config.enable_stream(rs.stream.color, colorwidth, colorheight, rs.format.bgr8, fps) # rgb

    print("Start video streamig\r\n")
    stream = pipeline.start(config)
    depth_sensor = stream.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    print("Depth device: ",depth_sensor)
    print("Depth Scale is: " , depth_scale)
    
    align_to = rs.stream.color
    align = rs.align(align_to)
    
    frame_count = 0
    start_time = time.time()

    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        frame_time = time.time() - start_time
        frame_count += 1

        # Align the depth frame to color frame
        aligned_frames = align.process(frames) 
        depth_frame = aligned_frames.get_depth_frame() 
        color_frame = aligned_frames.get_color_frame()
        infrared_frame = aligned_frames.get_infrared_frame()  
        print(depth_frame.get_distance(int(depthwidth/2), int(depthheight/2)))

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        IR_array = np.asanyarray(infrared_frame.get_data())

        # Apply colormap on depth image 
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)\

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))
        images = depth_colormap

        cv2.imwrite("img/rgb%d.jpg"% i, color_image)
        cv2.imwrite("img/dep%d.png"% i, depth_image)
        
        print("colored image %d.jpg have been saved"%i)
        i += 1
        # Press 's' to save image
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            pass
        # Press esc or 'q' to close the image window
        elif key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

except rs.error as e:
    # Method calls agaisnt librealsense objects may throw exceptions of type pylibrs.error
    #print("pylibrs.error was thrown when calling %s(%s):\n", % (e.get_failed_function(), e.get_failed_args()))
    print("    %s\n", e.what())
    exit(1)
except Exception as e:
    print(e)
    pass

finally:
    # Stop streaming & exit 
    pipeline.stop()
    exit(0)
