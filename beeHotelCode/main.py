from datetime import datetime
from picamera2 import Picamera2, Preview, MappedArray
from picamera2.outputs import FfmpegOutput
from picamera2.encoders import H264Encoder, Quality
import time
import libcamera
import cv2

def seconds_till_next_hour():
    n = datetime.now()
    return 60*(60-n.minute) + 60-n.second

def seconds_till_next_minute():
    n = datetime.now()
    return 60-n.second

def seconds_till_next_10minute():
    n = datetime.now()
    v = 60*10 - 60*(n.minute % 10) - n.second
    return v

def record():
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H_%M_%S")
    fmt = '.mp4'
    root = '/home/apis/Desktop/cameraOutput/beeHotel/'
  
    cam = Picamera2()
    preview_config = cam.create_video_configuration(lores={"size":(320,240)},display="lores",transform=libcamera.Transform(vflip=1,hflip=1))
    
    colour = (0, 255, 0)
    origin = (0, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.8
    thickness = 1
    #fTxt = open(root + filename + '.txt', 'w', encoding="utf-8")
    
    def apply_timestamp(request):
      timestamp = time.strftime("%Y-%m-%d %X")
      with MappedArray(request, "main") as m:
          cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
    
    cam.configure(preview_config)
    cam.pre_callback = apply_timestamp
    #cam.start_preview(True)
    cam.start()
#     try:
#         cam.stop_preview()
#         cam.start_preview(True)
#         time.sleep(60)
#         cam.start_preview(Preview.NULL)
#     except:
#         cam.start_preview(Preview.NULL)
#         print('preview error')
        
    while True:
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H_%M_%S")
        output = FfmpegOutput(root + filename + fmt)
        encoder = H264Encoder()
        quality = Quality.VERY_HIGH
        duration = seconds_till_next_10minute()
        print(duration)
        print(filename)
        cam.start_and_record_video(output, encoder, duration = duration,quality = quality)
    
    #cam.stop()
    #cam.stop_preview()
    #Txt.close

     
