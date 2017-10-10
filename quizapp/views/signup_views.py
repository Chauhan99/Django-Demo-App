from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from quizapp.forms import UserForm
from django.contrib import messages
from django.contrib.auth.models import User
from quizapp.forms import ProfileForm
# Create your views here.

def welcome(request):
	if request.user.is_authenticated():
		request.session['username']=request.user.username;
		return HttpResponseRedirect('../profile')
	elif request.method=="POST":
		signupform=UserForm(request.POST)
		if signupform.is_valid():
			new_user=User.objects.create_user(**signupform.cleaned_data)
			new_user.backend='django.contib.auth.backends.ModelBackend'
			messages.add_message(request,messages.SUCCESS,'Registration Successful !! Now Login using the credentials:')
			m=Uploads.objects.create(user=request.user)
			#m.save()
			return HttpResponseRedirect('../welcome')
		else:
			return render(request,'quizapp/welcome.html',{'form':signupform})	
 	else:
		signupform=UserForm()
		return render(request,'quizapp/welcome.html',{'form':signupform})
