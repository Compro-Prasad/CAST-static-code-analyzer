from django.http import JsonResponse
import subprocess

def analyze(request):
    p = subprocess.Popen("ls", stdout=subprocess.PIPE, shell=True)
    print(p.communicate())
    return JsonResponse({ "test": 1})
