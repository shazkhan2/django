from django.shortcuts import render

def index(request):
    return render(request, 'users/index.html')

def login(request):
    pass

def logout(request):
    pass
def register(request):
    pass