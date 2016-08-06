from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
# from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

from betApp import views 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.user_login, name='login'),
    url(r'^register_user/', views.register_user, name='register_user'),
    url(r'^register_admin/', views.register_admin, name='register_admin'),
    url(r'^userinfo/', views.userinfo, name='userinfo'),
    url(r'^games/', views.games, name='games'),
    url(r'^sportlist/', views.sportlist, name='sportlist'),
    url(r'^teams/', views.get_teams, name='teams'),
    url(r'^create_game/', views.create_game, name='create_game'),
    url(r'^create_bet/', views.create_bet, name='create_bet'),
    url(r'^user_bets/', views.user_bets, name='user_bets'),
    url(r'^bet_winner/', views.bet_winner, name='bet_winner'),
    url(r'^edit_balance/', views.edit_balance, name='edit_balance'),
]
