from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import platform

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
    return render(request, 'vehicle/test.html')
