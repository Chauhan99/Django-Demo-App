from django.shortcuts import render,get_object_or_404,render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.contrib import messages
from quizapp.models import Leaderboard,ProfileData,Question
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def fetch_leaderboard(request):
	mleaderboard=Leaderboard.objects.all()
	mleaderboard=mleaderboard.order_by('-score')
	msize=len(mleaderboard)
	for i in range(0,msize):
		mleaderboard[i].rank=i+1
		mleaderboard[i].save()
	return render_to_response('quizapp/leaderboard.html',{'mleaderboard':mleaderboard},context_instance=RequestContext(request))	

def fetch_profiledata(request):
	if request.user.is_authenticated():
		try:
			mprofiledata=get_object_or_404(ProfileData,user=request.user)
			return render_to_response('quizapp/loadprofile.html',{'mprofiledata':mprofiledata},context_instance=RequestContext(request))
		except(Http404):
			return HttpResponseRedirect('/quizapp/profile')
	else:
		return HttpResponseRedirect('/quizapp/welcome')
	
def update_Leaderboard(muser,mscore):
	mleaderboard=Leaderboard.objects.all()
	mleaderboard=mleaderboard.order_by('-score')
	msize=len(mleaderboard)
	
	for i in range(0,msize):
		if(mleaderboard[i].user==muser):
			if(mleaderboard[i].score<mscore):
				mleaderboard[i].score=mscore
				mleaderboard[i].save()
				mleaderboard=Leaderboard.objects.all()
				mleaderboard=mleaderboard.order_by('-score')
				for i in range(0,msize):
					mleaderboard[i].rank=i+1
					mleaderboard[i].save()
				return mleaderboard

	mplayer=Leaderboard.objects.create(rank=1,score=mscore,user=muser)
	mplayer.save()
	mleaderboard=Leaderboard.objects.all()
	mleaderboard=mleaderboard.order_by('-score')
	msize=len(mleaderboard)
	for i in range(0,msize):
		mleaderboard[i].rank=i+1
		mleaderboard[i].save()
	if(msize>5):
		mleaderboard[5].delete
	return mleaderboard
	
def fetch_quiz(request):
	if request.user.is_authenticated():
		
		mprofiledata=get_object_or_404(ProfileData,user=request.user)
		mquestion=mprofiledata.lastattempted	
		mquestion.option_set=mquestion.options.split(',')	
		mquestion.currentscore=mprofiledata.currentscore

		if mprofiledata.status==-1:	#quiz not started return the normal response
			if request.method=="POST":	#load first question
				try:
					mquestion=get_object_or_404(Question,pk=mprofiledata.lastattempted.id)
				except(Http404):
					mquestion = Question.objects.order_by('id')[0];

				mprofiledata.status=1	#Quiz started
				mquestion.option_set=mquestion.options.split(',')
				mquestion.currentscore=0
				mprofiledata.currentscore=0;
				mprofiledata.save()
				return render_to_response('quizapp/loadquizarena.html',{'mquestion':mquestion},context_instance=RequestContext(request))
			else:	#open link when not started	-> default
				return render_to_response('quizapp/loadquizarena.html',context_instance=RequestContext(request))
		
		elif mprofiledata.status==1:	#quiz running ,check the answer and load next question
			if request.method=="POST":
				if 'selected' not in request.POST:	#No option selected
					messages.add_message(request,messages.ERROR,'Please select an option')
					return render_to_response('quizapp/loadquizarena.html',{'mquestion':mquestion},context_instance=RequestContext(request))
				
				else:	#Check the option	
					if(mprofiledata.lastattempted.correct_option==int(request.POST['selected'])):#Correct
						messages.add_message(request,messages.SUCCESS,'Correct Answer !!')
						mprofiledata.currentscore=mprofiledata.currentscore+1;
						mprofiledata.save()
						try:	#Loading next question
							mquestion=get_object_or_404(Question,pk=mprofiledata.lastattempted.id+1)
							mquestion.option_set = mquestion.options.split(',')
							mquestion.currentscore=mprofiledata.currentscore
							mprofiledata.lastattempted=mquestion
							mquestion.option_set=mquestion.options.split(',')
							mprofiledata.save()
							return render_to_response('quizapp/loadquizarena.html',{'mquestion':mquestion},context_instance=RequestContext(request))
						except(Http404):	#All questions done
							messages.add_message(request,messages.ERROR,'We are falling short of questions, we are adding more questions to database . Your final score is '+str(mprofiledata.currentscore))
							if(mprofiledata.highscore<mprofiledata.currentscore):
								mprofiledata.highscore=mprofiledata.currentscore
								mleaderboard=update_Leaderboard(request.user,mprofiledata.currentscore)
							mprofiledata.currentscore=-1
							mprofiledata.status=-1
							mprofiledata.save()
							return render_to_response('quizapp/loadquizarena.html',context_instance=RequestContext(request))
							return HttpResponseRedirect('/quizapp/quiz/')	#Reload the page
					else:	#Incorrect answer
						messages.add_message(request,messages.ERROR,'Sorry Incorrect answer :( Your score is '+str(int(mprofiledata.currentscore)))
						if(mprofiledata.highscore<mprofiledata.currentscore):
							mprofiledata.highscore=mprofiledata.currentscore
							mleaderboard=update_Leaderboard(request.user,mprofiledata.currentscore)
						mprofiledata.currentscore=-1
						mprofiledata.status=-1
						mprofiledata.save()
						return render_to_response('quizapp/loadquizarena.html',context_instance=RequestContext(request))
						return HttpResponseRedirect('/quizapp/quiz/')	#Reload the page
			else:	#random refresh on the question page
				render_to_response('quizapp/loadquizarena.html',{'mquestion':mquestion},context_instance=RequestContext(request))

def quiz(request):
	return render(request,'quizapp/quiz.html',)