from django.shortcuts import render

def login_view(request):
    return render(request, "epp_app/login.html")

def register_view(request):
    return render(request, "epp_app/register.html")

def camera_view(request):
    return render(request, "epp_app/camera.html")