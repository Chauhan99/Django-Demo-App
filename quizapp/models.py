from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def contact_range(value):
	if value<10000000000 or value>9999999999:
		raise ValidationError("Enter a valid Contact Number")

def enroll_range(value):
	if value<10000000 or value>99999999:
		raise ValidationError("Enter a valid Enrollment Number")

class Question(models.Model):
	def __str__(self):
		return self.question_text
	question_text	= models.CharField(max_length=400)
	options 		= models.CharField(max_length=1000)		#comma separated options
	correct_option 	= models.IntegerField()
	#level = models.IntegerField()

class ProfileData(models.Model):	
	def __str__(self):
		return self.user.first_name+' '+self.user.last_name
	user = models.OneToOneField(User)
	gender = models.CharField(max_length=6,blank=False,choices=(('Male','Male'),('Female','Female')),default='Male')
	dob = models.DateField()
	contact = models.BigIntegerField()#validators=[contact_range])#min_value=1000000000,max_value=9999999999)
	address = models.CharField(max_length=200)
	about = models.CharField(max_length=300)
	highscore = models.IntegerField(default=-1)
	lastattempted = models.ForeignKey(Question)
	currentscore = models.IntegerField(default=-1)	#-1 not yet started
	status = models.IntegerField(default=-1)

class Uploads(models.Model):
	user=models.OneToOneField(User)
	profile=models.ImageField(upload_to='./profile/',default='/profile/default_profile.jpg')

class Leaderboard(models.Model):
	def __str__(self):
		return '#' + str(self.rank) + '-> ' + self.user.first_name
	rank			= models.IntegerField(default=-1)
	score 			= models.IntegerField()
	user 			= models.OneToOneField(User)
