from django.contrib import admin
from django.contrib.auth.models import User
from quizapp.models import Leaderboard,ProfileData,Question
admin.site.register(ProfileData)
admin.site.register(Leaderboard)
admin.site.register(Question)
# Register your models here.
