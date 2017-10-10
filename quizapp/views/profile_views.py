from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,Http404
from quizapp.forms import UserForm
from django.contrib import messages
from django.contrib.auth.models import User
from quizapp.forms import ProfileForm
from quizapp.models import ProfileData, Uploads, Question

def profile(request):
	if request.user.is_authenticated():
		request.session['username']=request.user.username
		try:
			profiledata=get_object_or_404(ProfileData,user=request.user)
		except(Http404):
			return HttpResponseRedirect('./complete')
		
		try:
			uploads=get_object_or_404(Uploads,user=request.user)
		except(Http404):
			uploads=Uploads.objects.create(user=request.user)
		
		return HttpResponseRedirect('/quizapp/quiz')
	else:
		username=''
		if(request.method=="POST"):
			username=request.POST.get('username')
			password=request.POST.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					request.session['state']="Login Successful"
					request.session['username']=username
					login(request, user)
					try:
						profiledata=get_object_or_404(ProfileData,user=request.user)
					except(Http404):
						return HttpResponseRedirect('./complete')
					try:
						uploads=get_object_or_404(Uploads,user=request.user)
					except(Http404):
						return HttpResponseRedirect('/quizapp/quiz/')
					return HttpResponseRedirect('/quizapp/quiz/')
				else:
					request.session['state']="Your account is not active"
			else:
				messages.add_message(request,messages.ERROR,'Incorrect Login Credentials')
				return HttpResponseRedirect('/quizapp/welcome/')
		
		
		return HttpResponseRedirect('/quizapp/welcome/')

def profile_complete(request):
	if request.method=="POST":
		form=ProfileForm(request.POST)
		if form.is_valid():
			mquestion = Question.objects.order_by('id')[0]
			new_profile=ProfileData.objects.create(user=request.user,gender=request.POST['gender'],dob=request.POST['dob_year']+'-'+request.POST['dob_month']+'-'+request.POST['dob_day'],contact=request.POST['contact'],address=request.POST['address'],about=request.POST['about'],lastattempted=mquestion)
			return HttpResponseRedirect('/quizapp/welcome')	
		else:
			return render(request,'quizapp/complete.html',{'form':form})
	else:
		try:
			profiledata=get_object_or_404(ProfileData,user=request.user)
			return HttpResponseRedirect('/quizapp/welcome')
		except(Http404):
			form=ProfileForm()
			return render(request,'quizapp/complete.html',{'form':form})

def profile_complete_submit(request):
	if request.method=="POST":
		form=ProfileForm(request.POST)
		if form.is_valid():
			new_profile=ProfileData.objects.create(user=request.user,gender=request.POST['gender'],dob=form.dob,email=request.POST['email'],contact=request.POST['contact'],address=request.POST['address'],about=request.POST['about'])
			return HttpResponseRedirect('../../../welcome')	
		else:
			return 
			return HttpResponseRedirect('../../complete')
	else:
		return HttpResponseRedirect('/quizapp/profile')	

def profile_edit(request):
	if request.user.is_authenticated():
		profiledata=get_object_or_404(ProfileData,user=request.user)
		form=ProfileForm()
		return render(request,'quizapp/profile_edit.html',{'profile':profiledata,'form':form})
	else:
		return HttpResponseRedirect('/quizapp/welcome')

def profile_edit_submit(request):
	if request.method=="POST" and request.user.is_authenticated():
		try:
			profiledata=get_object_or_404(ProfileData,user=request.user)
			
			if request.POST['gender']!="":
				profiledata.gender=request.POST['gender']
			if request.POST['dob_day']!="1" or request.POST['dob_month']!="1" or request.POST['dob_year']!="1980":
				profiledata.dob=request.POST['dob_year']+'-'+request.POST['dob_month']+'-'+request.POST['dob_day']	
			#if request.POST['email']!="":
			#	profiledata.email=request.POST['email']
			if request.POST['contact']!="":
				profiledata.contact=request.POST['contact']
			if request.POST['address']!="":
				profiledata.address=request.POST['address']
			if request.POST['about']!="":
				profiledata.about=request.POST['about']
			
			profiledata.save()	
			messages.add_message(request,messages.SUCCESS,'Profile Successfully Updated')
			return HttpResponseRedirect("../../")
		except(Http404):
			return HttpResponseRedirect("/quizapp/welcome")
	else:
		return HttpResponseRedirect('/quizapp/welcome')

def password_change(request):
	if request.user.is_authenticated():
		return render(request,'quizapp/password.html',)
	else:
		return HttpResponseRedirect('/quizapp/welcome')
		
def password_change_submit(request):
	if(request.method=="POST") and request.user.is_authenticated():	
		try:
			if(request.POST['newpassword']!=request.POST['newpassword2']):
				messages.add_message(request,messages.ERROR,'Password and Confirm Password Don\'t Match ')
				return HttpResponseRedirect("../")
			user=authenticate(username=request.user.username,password=request.POST['oldpassword'])
			if user is not None:
				user.set_password(request.POST['newpassword'])
				user.save()
				login(request,user)
				return HttpResponseRedirect("../../../")
			else:
				messages.add_message(request,messages.ERROR,'Incorrect Password')
				return HttpResponseRedirect("../")
		except(Http404):
			return HttpResponseRedirect("/quizapp/welcome")

	else:
		return HttpResponseRedirect("/quizapp/profile")
