from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
# from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from betApp.models import *
# from events.models import/ EventNew
from django.contrib import auth
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect,Http404,HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import difflib
from betApp.forms import *
import json
from django.http import JsonResponse
import requests

# Create your views here.

@csrf_exempt
def user_login(request):
	email = request.POST['email']
	password = request.POST['password']
	u = User.objects.get(email=email)
	username = u.username
	user = authenticate(username=username, password=password)
	if user:
		login(request, user)
	customer_ob = Customer.objects.filter(user=u)
	admin_ob = Admin.objects.filter(user=u)
	if customer_ob:
		return HttpResponse("Customer login Successful")
	if admin_ob:
		return HttpResponse("Admin login Successful")
	else:
		return HttpResponse("login failed")


@csrf_exempt
def register_user(request):
	name = request.POST['name']
	#dob = request.POST['dob']
	gender = request.POST['gender']
	phone = request.POST['phone']
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	user = User.objects.create_user(username=username, email=email,password=password)
	user = authenticate(username=username, password=password)
	login(request, user)
	customer = Customer(user=user, name=name, phone=phone, balance=0, email_id=email, gender=gender)
	customer.save()
	return HttpResponse("registration Successful")


@csrf_exempt
def register_admin(request):
	name = request.POST['name']
	#dob = request.POST['dob']
	gender = request.POST['gender']
	phone = request.POST['phone']
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	user = User.objects.create_user(username=username, email=email,password=password)
	user = authenticate(username=username, password=password)
	login(request, user)
	admin_ob = Admin(user=user, name=name, phone=phone, email_id=email, gender=gender)
	admin_ob.save()
	return HttpResponse("registration Successful")


@csrf_exempt
def userinfo(request):
	email = request.GET['email']
	customer = Customer.objects.get(email_id=email)
	return JsonResponse({'name': customer.name,
						 'gender': customer.gender,
						 'email_id': customer.email_id,
						 'phone': customer.phone,
						 'balance': customer.balance})


@csrf_exempt
def games(request):
	games = Game.objects.all()
	gamelist = []
	game = {}
	for g in games:
		game['game_id'] = g.id
		game['name'] = g.name
		game['team_1_id'] = g.team1.team_name
		game['team_2_id'] = g.team2.team_name
		game['start_time'] = str(g.startTime)
		game['end_time'] = str(g.endTime)
		gamelist.append(game)
		game = {}
	json_gamelist = json.dumps(gamelist) 
	return HttpResponse(json_gamelist, content_type ="application/json")

@csrf_exempt
def sportlist(request):
	sports = Sport.objects.all()
	sportlist = []
	for s in sports:
		sportlist.append(s.sport)
	json_sportlist = json.dumps(sportlist) 
	return HttpResponse(json_sportlist, content_type ="application/json")

@csrf_exempt
def get_teams(request):
	sport_id = request.GET['sport_id']
	sport = Sport.objects.get(id=sport_id)
	teams = Team.objects.filter(sport=sport)
	teamlist = []
	for t in teams:
		teamlist.append(t.team_name)
	json_teamlist = json.dumps(teamlist) 
	return HttpResponse(json_teamlist, content_type ="application/json")


@csrf_exempt
def create_game(request):
	userid = request.POST['email']
	name = request.POST['name']
	team1id = request.POST['team1_id']
	team2id = request.POST['team2_id']
	start_time = request.POST['start_time']
	end_time = request.POST['end_time']
	user = User.objects.get(email=userid)
	team1 = Team.objects.get(id=team1id)
	team2 = Team.objects.get(id=team2id)
	if user.is_staff:
		game = Game()
		game.owner = user
		game.name = name
		game.team1 = team1
		game.team2 = team2
		game.sport = team1.sport
		game.startTime = start_time
		game.endTime = end_time
		game.active = True
		game.save()
		return HttpResponse("game created successfully")
	else:
		return HttpResponse("Permission denied")


@csrf_exempt
def create_bet(request):
	userid = request.POST['email']
	gameid = request.POST['game_id']
	amount = request.POST['amount']
	choice = request.POST['choice']
	user = Customer.objects.get(email_id=userid)
	game = Game.objects.get(id=gameid)
	if choice=='1':
		bet = Bet(game=game, player1=user, amount=amount, status='OPEN')
	if choice=='2':
		bet = Bet(game=game, player2=user, amount=amount, status='OPEN')
	else:
		bet = Bet(game=game, player3=user, amount=amount, status='OPEN')
	bet.save()
	return HttpResponse("Bet created successfully")


@csrf_exempt
def user_bets(request):
	userid = request.POST['email']
	choice = request.POST['choice']
	betid = request.POST['bet_id']
	user = Customer.objects.get(email_id=userid)
	bet = Bet.objects.get(id=betid)
	if choice=='1':
		bet.player1 = user
	if choice=='2':
		bet.player2 = user
	else:
		bet.player3 = user

	bet.save()
	return HttpResponse("successfully edited bet")

@csrf_exempt
def bet_winner(request):
	betid = request.GET['bet_id']
	bet = Bet.objects.get(id=betid)
	if bet.winner:
		return HttpResponse(bet.winner)
	else:
		return HttpResponse("Winner not yet announced. Bet status is " + str(bet.status))

@csrf_exempt
def edit_balance(request):
	userid = request.POST['email']
	amount = request.POST['amount']
	user = Customer.objects.get(email_id=userid)
	user.balance += int(amount)
	if user.balance > 0:
		user.save()
		return HttpResponse("User balance is now " + str(user.balance))
	else:
		return HttpResponse("Not enough balance")