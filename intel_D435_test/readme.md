# Reminder of using this program

### install dependency 
```shell 
pip3 install flask 
pip3 install numpy
pip3 install opencv-python 
```
also install the pyrealsense2 if you wanna run this appication or change to other alternative by modify the code. 

## enable the port access on your device 
In order to access the server in remote computer, you need to allow the public tcp access to the port in your device.

```shell
sudo ufw enable
sudo ufw allow 5000/tcp
````
