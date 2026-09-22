from django.shortcuts import render

def camera_view(request):
    return render(request, "epp_app/camera.html")
