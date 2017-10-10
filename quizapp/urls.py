from django.conf.urls import patterns,url
from quizapp import views

urlpatterns=patterns(
'',
url(r'^leaderboard/',views.fetch_leaderboard),
url(r'^loadprofile/',views.fetch_profiledata),
url(r'^loadquiz/',views.fetch_quiz),
url(r'^quiz/',views.quiz),
url(r'^welcome/$',views.welcome),
url(r'^profile/$',views.profile),
url(r'^profile/complete/$',views.profile_complete),
url(r'^profile/complete/submit/$',views.profile_complete),
url(r'^logout/$',views.log_out),
)
