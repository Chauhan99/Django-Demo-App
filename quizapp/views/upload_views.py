from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,Http404
#from logapp.forms import UserForm
from django.contrib import messages
from django.contrib.auth.models import User
#from logapp.forms import ProfileForm,ImageUploadForm,Image2UploadForm
from quizapp.models import ProfileData,Uploads

def upload_cover(request):
	if request.method=="POST":
		if request.user.is_authenticated():
			form = ImageUploadForm(request.POST, request.FILES)
        		if form.is_valid():
        			try:
            				m = Uploads.objects.get(user=request.user)
     		       			m.cover = form.cleaned_data['image']
            				m.save()
					messages.add_message(request,messages.SUCCESS,"Cover Picture Successfully Updated")
            				return HttpResponseRedirect("../../../profile/")
           	 		except(Http404):
					m = Uploads.objects.create(user=request.user)
					m.cover= form.cleaned_data['image']
					m.save()
					messages.add_message(request,messages.SUCCESS,"Cover Picture Successfully Updated")
            				return HttpResponseRedirect("../../../profile")
			else:
				messages.add_message(request,messages.ERROR,"Invalid file type, Please upload an image")
				return HttpResponseRedirect("../../../profile")
		else:
			return HttpResponseRedirect("../../../welcome")
	else:
		return HttpResponseRedirect("../../../profile")

def upload_profile(request):
	if request.method=="POST":
		if request.user.is_authenticated():
			form = Image2UploadForm(request.POST, request.FILES)
        		if form.is_valid():
        			try:
            				m = Uploads.objects.get(user=request.user)
     		       			m.profile = form.cleaned_data['image2']
            				m.save()
					messages.add_message(request,messages.SUCCESS,"Profile Picture Successfully Updated")
            				return HttpResponseRedirect("../../../profile/")
           	 		except(Http404):
					m = Uploads.objects.create(user=request.user)
					m.cover= form.cleaned_data['image']
					m.save()
					messages.add_message(request,messages.SUCCESS,"Profile Picture Successfully Updated")
            				return HttpResponseRedirect("../../../profile")
			else:
				messages.add_message(request,message.ERROR,"Couldn't upload file now, Please try later")
				return HttpResponseRedirect("../../../profile")
		else:
			return HttpResponseRedirect("../../../welcome")
	else:
		return HttpResponseRedirect("../../../profile")


	
