from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def login_view(request):
	print('доошло')
	return HttpResponse('', status=400)
