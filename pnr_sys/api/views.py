from django.shortcuts import render
from django.http import JsonResponse
import cv2
from PIL import Image
import base64
from django.http import StreamingHttpResponse
import threading
from .models import Latest
import pytesseract
import os
import re
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

def get_image(request):
    cam = cv2.VideoCapture(0)
    plate_number = '--- ---'
    check = True
    img = ''

    if cam.isOpened():
        check, frame = cam.read()
        print(check)
        print(frame)

        img_cv = cv2.resize(frame, (400, 300))
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        success, img = cv2.imencode('.jpg', img_cv)
        img = Image.fromarray(img)
        img = base64.b64encode(img.tobytes())
        img = 'data:image/jpeg;base64,' + img.decode("utf-8")
    else:
        check = False

    cam.release()

    return JsonResponse({ 'check': check, 'img': img, 'plate': plate_number });

def check_captured(request):
    latest = Latest.objects.first()
    if latest == None:
        plate = ''
        status = False
    else:
        plate = latest.plate
        status = latest.status

    print(plate)
    print(status)

    return JsonResponse({'plate': plate, 'status': status });

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

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            gray = cv2.medianBlur(gray, 3)
            ptext = pytesseract.image_to_string(Image.fromarray(gray))
            # print(ptext)
            r = re.findall(r'[A-Z]+\s+[0-9]+', ptext)
            # print(r)
            # print(len(r))
            text = ''
            if len(r) > 0:
                text = r[0].replace(' ', '')

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
