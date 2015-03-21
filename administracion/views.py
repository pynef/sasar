from django.shortcuts import render

def home(request):
	return render(request,'frontend/index.html')

def apertura(req):
    return render(req, 'backend/apertura.html')