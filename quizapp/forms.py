from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from quizapp.models import ProfileData, Uploads, Question, Leaderboard

class UserForm(ModelForm):
	class Meta:
		model= User
		fields=('username','first_name','last_name','password','email')
		widgets={'password':forms.PasswordInput()}

class ProfileForm(ModelForm):
	class Meta:
		model=ProfileData
		fields=('gender','dob','contact','address','about')
		widgets={'gender':forms.RadioSelect(),'dob':SelectDateWidget(years=range(1980,2000)),'about':forms.Textarea}
		
class ImageUploadForm(forms.Form):
	image=forms.ImageField()
