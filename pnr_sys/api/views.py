from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
from django.apps import apps
from PIL import Image
from .models import Latest
import pytesseract
import threading
import cv2
import os
import re
import platform
import sys

if platform.system() == 'Linux':
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
if platform.system() == 'OS X' or platform.system() == 'Darwin':
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

def sample_image(request):

    return ''

def check_camera(request):
    cam = cv2.VideoCapture(0)

    i = 0
    while True:
        check, frame = cam.read()
        print(frame)

        cv2.imshow('Testing Camera...', frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break

        i += 1

    cam.release()
    cv2.destroyAllWindows()

    return JsonResponse({'status': True, 'time_frame': i})

def check_captured(request):
    print(platform.system())
    plate = ''
    status = False
    registerd = False
    v_type = 'na'

    latest = Latest.objects.first()
    if latest != None:
        plate = latest.plate
        status = latest.status
    
    MVehicle = apps.get_model('vehicle', 'Vehicle')
    all_v = MVehicle.objects.all()
    if len(all_v) > 0:
        v = MVehicle.objects.filter(plate=plate).first()
        print(v)
        if v != None:
            registerd = True

    if len(plate) == 7:
        v_type = 'car'
    if len(plate) == 8:
        v_type = 'motorcycle'
    if len(plate) == 12:
        v_type = 'motorcycle'

    if plate == '':
        plate = '--- ---'

    context = {
        'plate': plate,
        'status': status,
        'registerd': registerd,
        'v_type': v_type
    }
    print(context)

    return JsonResponse(context)

@gzip.gzip_page
def live_feed(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        e = sys.exc_info()
        print("aborted", e)

def gen(camera):
        while True:
            frame = camera.get_frame()
            yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        (ret, image) = self.video.read()
        gray = extract_text(image)
        (ret, jpeg) = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

def extract_text(frame):
    gray = frame
    # RESIZING
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # gray = cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    # gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    # COLOR
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    # TRESHHOLD
    gray = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
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
        text = r1[0].replace(' ', '-')
        text = text.replace('\n', '')
    else:
        r2 = re.findall(r'([\d]+-[\d]+)', ptext)
        # print(r2)
        # print(len(r2))
        if len(r2) > 0:
            text = r2[0].replace(' ', '-')
            text = text.replace('\n', '')

    if text != '':
        latest = Latest.objects.first()
        if latest == None:
            l = Latest(plate=text, status=True)
            l.save()
        else:
            latest.plate = text
            latest.status = True
            latest.save()

    return gray

@gzip.gzip_page
def live_feed_old(request):
    class VideoCameraOld():
        def __init__(self):
            self.video = cv2.VideoCapture(0)
            (self.grabbed, self.frame) = self.video.read()
            threading.Thread(target=self.update, args=()).start()

        def __del__(self):
            self.video.release()

        def get_frame(self):
            image = self.frame

            gray = extract_text(image)

            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

        def update(self):
            while True:
                (self.grabbed, self.frame) = self.video.read()


    # Needed To Initialize Camera
    cam = VideoCameraOld()


    def genold(camera):
        while True:
            frame = camera.get_frame()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                
    try:
        return StreamingHttpResponse(genold(VideoCameraOld()), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:  # This is bad! replace it with proper handling
        print(e)
        # pass
    