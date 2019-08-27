from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.apps import apps
from PIL import Image
from .models import Latest
import pytesseract
import threading
import base64
import cv2
import os
import re

pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

def check_captured(request):
    plate = ''
    status = False
    registerd = False

    latest = Latest.objects.first()
    if latest != None:
        plate = latest.plate
        status = latest.status
    
    MVehicle = apps.get_model('vehicle', 'Vehicle')
    v = MVehicle.objects.filter(plate=plate).first()
    print(v)
    if v != None:
        registerd = True

    context = {
        'plate': plate,
        'status': status,
        'registerd': registerd
    }
    print(context)

    return JsonResponse(context);

def live_feed(request):
    class VideoCamera(object):
        def __init__(self):
            self.video = cv2.VideoCapture(0)
            (self.grabbed, self.frame) = self.video.read()
            threading.Thread(target=self.update, args=()).start()

        def __del__(self):
            self.video.release()

        def get_frame(self):
            image = self.frame

            gray = image
            # RESIZING
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            # gray = cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            # gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
            # COLOR
            gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
            # TRESHHOLD
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
            # BLUR
            gray = cv2.medianBlur(gray, 3)
            # gray = cv2.bilateralFilter(gray,9,75,75)
            
            ptext = pytesseract.image_to_string(Image.fromarray(gray))
            print(ptext)
            r1 = re.findall(r'([A-Z]+\s+[\d]+)', ptext)
            # print(r1)
            # print(len(r1))
            text = ''
            if len(r1) > 0:
                text = r1[0].replace(' ', '')
                text = text.replace('\n', '')
            else:
                r2 = re.findall(r'([\d]+-[\d]+)', ptext)
                # print(r2)
                # print(len(r2))
                if len(r2) > 0:
                    text = r2[0].replace(' ', '')
                    text = text.replace('\n', '')

            ret, jpeg = cv2.imencode('.jpg', image)

            if text != '':
                latest = Latest.objects.first()
                if latest == None:
                    l = Latest(plate=text, status=True)
                    l.save()
                else:
                    latest.plate = text
                    latest.status = True
                    latest.save()

            return jpeg.tobytes()

        def update(self):
            while True:
                (self.grabbed, self.frame) = self.video.read()


    cam = VideoCamera()


    def gen(camera):
        while True:
            frame = cam.get_frame()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
