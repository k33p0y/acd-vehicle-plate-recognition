from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
from django.apps import apps
from django.utils import timezone
from PIL import Image
from .models import Latest
import pytesseract
import threading
import cv2
import os
import re
import platform
import sys
from datetime import datetime, timedelta, time

if platform.system() == 'Linux':
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
if platform.system() == 'OS X' or platform.system() == 'Darwin':
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

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
    registered = False
    v_type = 'n/a'
    same_entry = False
    is_valid = True

    latest = Latest.objects.first()
    if latest != None:
        plate = latest.plate
        status = latest.status

    all_l = Latest.objects.all()
    if len(all_l) > 1:
        l1 = Latest.objects.first()
        l2 = Latest.objects.last()
        if l1.plate == l2.plate:
            same_entry = True
        else:
            l2.plate = l1.plate
            l2.status = l2.status
            l2.save()
    if len(all_l) == 1:
        l = Latest(plate=plate, status=status)
        l.save()
    
    Vehicle = apps.get_model('vehicle', 'Vehicle')
    all_v = Vehicle.objects.all()
    if len(all_v) > 0:
        v = Vehicle.objects.filter(plate=plate).exclude(owner__exact='').first()
        if v != None:
            registered = True

    if len(plate) == 7:
        v_type = 'car'
    if len(plate) == 8:
        v_type = 'motorcycle'
    if len(plate) == 12:
        v_type = 'motorcycle'
    if len(plate) == 16:
        v_type = 'car'

    if plate == '':
        plate = '--- ---'
        is_valid = False

    context = {
        'plate': plate,
        'status': status,
        'registered': registered,
        'v_type': v_type,
        'same_entry': same_entry,
        'is_valid': is_valid,
    }
    print(context)

    return JsonResponse(context)

@gzip.gzip_page
def live_feed(request):
    activate = request.GET.get('activate', False)
    print(activate)
    
    try:
        return StreamingHttpResponse(gen(VideoCamera(), activate),content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        e = sys.exc_info()
        print("aborted", e)

def gen(camera, activate):
        while True:
            frame = camera.get_frame(activate)
            yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()

    def get_frame(self, activate):
        (ret, image) = self.video.read()
        if activate and activate == 'true':
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
        text = r1[0].replace(' ', '-')
        text = text.replace('\n', '')
    else:
        r2 = re.findall(r'([\d]+-[\d]+)', ptext)
        # print(r2)
        # print(len(r2))
        if len(r2) > 0:
            text = r2[0].replace(' ', '-')
            text = text.replace('\n', '')

    if text != '' and len(text) >= 7:
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
    except:  # This is bad! replace it with proper handling
        # print(e)
        pass


# PARTIALS
@gzip.gzip_page
def inout_partial(request):
    latest = Latest.objects.first()
    if latest != None:
        plate = latest.plate
    else:
        plate = ''
    
    registered = False
    logged = False
    
    Vehicle = apps.get_model('vehicle', 'Vehicle')
    v = Vehicle.objects.filter(plate=plate).first()
    if v != None:
        registered = True
        Log = apps.get_model('vehicle', 'Log')
        l = Log.objects.filter(vehicle=v, datetime_out__isnull=True).last()
        if l != None:
            logged = True    

    context = {
        'plate': plate,
        'registered': registered,
        'logged': logged,
    }
    return render(request, 'api/inout-partial.html', context)

@gzip.gzip_page
def list_partial(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    Log = apps.get_model('vehicle', 'Log')
    l = Log.objects.order_by('-pk').filter(datetime_in__gte=today_start, datetime_in__lte=today_end)
    context = {
        'logs': l,
        'total': len(l)
    }
    return render(request, 'api/list-partial.html', context)

def park_inout(request):
    success = False
    flow = ''

    latest = Latest.objects.first()
    if latest != None:
        Vehicle = apps.get_model('vehicle', 'Vehicle')
        v = Vehicle.objects.filter(plate=latest.plate).first()
        if v == None:
            v_type = 'n/a'
            if len(latest.plate) == 7:
                v_type = 'car`'
            if len(latest.plate) == 8:
                v_type = 'motorcycle'
            if len(latest.plate) == 12:
                v_type = 'motorcycle'
            v = Vehicle(plate=latest.plate, v_type=v_type, guard=request.user)
            v.save()

        Log = apps.get_model('vehicle', 'Log')
        l = Log.objects.filter(vehicle=v, datetime_out__isnull=True).last()
        if l == None:
            l_in = Log(vehicle=v, guard=request.user, datetime_out=None)
            l_in.save()
            flow = 'in'
        else:
            l.datetime_out = timezone.now()
            l.save()
            flow = 'out'
        latest.plate = ''
        latest.save()
        success = True

    context = {
        'success': success,
        'flow': flow,
    }
    return JsonResponse(context)

def manual_input(request):
    plate = request.GET.get('plate', '')
    plate = plate.replace(' ', '-')

    l = Latest.objects.first()
    if l == None:
        l_new = Latest(plate=plate, status=True)
        l_new.save()
    else:
        l.plate = plate
        l.status = True
        l.save()

    context = {
        'success': True
    }
    return JsonResponse(context)