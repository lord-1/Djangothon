from django.views.generic import View
from django.http  import HttpResponse
from django.shortcuts import render
from .models import *
import time
import json
# Create your views here.

class test(View):
	def get(self, request):
		return HttpResponse("view1")
	
	def post(self, request):
		return HttpResponse('Sample response12')

class test2(View):

	def get(self, request):
		return HttpResponse("view 2")

	def post(self, request):
		return HttpResponse('Something')

class test3(View):

	def get(self, request):
		return HttpResponse("View 3")

	def post(self, request):
		return HttpResponse("something ")

class test4(View):

	def get(self, request):
		return HttpResponse("View 4")

	def post(self, request):
		return HttpResponse("something pver")

class test5(View):

	def get(self, request):
		return HttpResponse('view 5')

	def post(self, request):
		return HttpResponse('Somhthin ver')

class tree_api(View):

	def get(self, request):
		null = None
		return HttpResponse('tHis is resposne')
		return HttpResponse(json.dumps({'a':'b'}))

class CreateAdmin(View):

	def get(self, request):
		return HttpResponse("MNA")

	def post(self, request):

		admin_id = request.POST.get('admin_id', '')
		password = request.POST.get('password', '')
		new_admin_id = request.POST.get('new_admin_id', '')
		new_admin_pass = request.POST.get('new_admin_pass', '')
		new_admin_name = request.POST.get('new_admin_name', '')

		try:
			print "this is the admin id", admin_id
			admin_object = SuperAdmin.objects.get(admin_id = admin_id)
			#now we will delete the base admin objects
			admin_password = admin_object.admin_password
			md5 = hashlib.md5()
			md5.update(password)
			password = md5.hexdigest()
			print password, admin_password
			if password == admin_password:
				print "YES the passwords match"
			else:
				print "NO the passwords dont match"
			return HttpResponse("Cool we tried doing something")
		except Exception as e:
			return HttpResponse(str(e))
		return HttpResponse("MNA")
