from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import platform
from django.apps import apps
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta, time
from django.http import HttpResponseRedirect
from django.shortcuts import render
from calendar import monthrange
import cv2
from .forms import NameForm
def landing(request):
    print(request.user)
    if request.user.is_authenticated :
        return redirect('/home/')
    else:
        return render(request, 'vehicle/landing.html')

@login_required
def home(request):
    context = {
        'system': platform.system()
    }
    return render(request, 'vehicle/home.html', context)

def test(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    Log = apps.get_model('vehicle', 'Log')
    l = Log.objects.order_by('-pk').all()
    p = Log.objects.filter(datetime_out__isnull=True).count()
    context = {
        'logs': l,
        'records': len(l),
        'parked_in': p
    }
    return render(request, 'vehicle/test.html')

def history(request):
    tfilter = request.GET.get('filter', '')
    date_from= request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    has_custom =True

    disconnectCamera()

    today = datetime.now().date()
    if tfilter == '' or tfilter == 'today':
        tomorrow = today + timedelta(1)
        day_start = datetime.combine(today, time())
        day_end = datetime.combine(tomorrow, time())
    elif tfilter == 'week':
        day_start = today - timedelta(days=(today.weekday() + 1) % 7)
        day_end = day_start + timedelta(days=6)
    elif tfilter == 'month':
        day_start = today - timedelta(days=today.day - 1)
        day_end = today + timedelta(days=monthrange(today.year, today.month)[1] - today.day)
    else:
        has_custom = True
        tomorrow = today + timedelta(1)
        day_start = datetime.combine(today, time())
        day_end = datetime.combine(tomorrow, time())
        if len(date_from) > 0:
            day_start = datetime.strptime(date_from + ' 12:00AM', '%m/%d/%Y %I:%M%p')
        if len(date_to) > 0:
            day_end = datetime.strptime(date_to + ' 11:59PM', '%m/%d/%Y %I:%M%p')

    Log = apps.get_model('vehicle', 'Log')

    # date_queryset = Log.objects.filter(datetime_in__range=(date_from,date_to))
    # {'date_queryset': date_queryset}
    l = Log.objects.order_by('-pk').filter(datetime_in__gte=day_start, datetime_in__lte=day_end)

    context = {
        'page': 'history',
        'filter': tfilter,
        'logs': l,
        'day_start': day_start,
        'day_end': day_end,
        'has_custom': has_custom,
        'custom_date_from': date_from if date_from else today.strftime('%Y/%m/%d'),
        'custom_date_to': date_to if date_to else today.strftime('%Y/%m/%d'),
        'today': today
    }
    return render(request, 'vehicle/History.html', context)

def disconnectCamera():
    cam = cv2.VideoCapture(0)
    cam.release()
def signup(request):
    return render(request, 'vehicle/signup.html')

def reports(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    Log = apps.get_model('vehicle', 'Log')


    l = Log.objects.order_by('-pk').all()
    p = Log.objects.filter(datetime_out__isnull=True).count()
    context = {
        'logs': l,
        'records': len(l),
        'parked_in': p
    }
    return render(request, 'vehicle/reports.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)
            (request, user)
            redirect('home.html')
    else:
        form = UserCreationForm()
    return render(request, 'vehicle/signup.html', {'form': form})
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'reports.html', {'form': form})


