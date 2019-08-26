from django.shortcuts import render
from django.http import JsonResponse
import cv2
from PIL import Image
import base64

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
