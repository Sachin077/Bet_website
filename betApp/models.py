from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
	user = models.OneToOneField(User)
	GENDERS = (
		('M', 'Male'),
		('F', 'Female'),
	)
	name = models.CharField(max_length=200)
	gender = models.CharField(max_length=1, choices=GENDERS)
	dob = models.DateField(null=True)
	email_id = models.EmailField(blank=True, null=True)
	phone = models.BigIntegerField(blank=True, null=True)

	def __unicode__(self):
		return str(self.name)	


class Customer(models.Model):
	user = models.OneToOneField(User)
	GENDERS = (
		('M', 'Male'),
		('F', 'Female'),
	)
	name = models.CharField(max_length=200)
	gender = models.CharField(max_length=1, choices=GENDERS)
	dob = models.DateField(null=True)
	email_id = models.EmailField(blank=True, null=True)
	phone = models.BigIntegerField(blank=True, null=True)
	balance = models.IntegerField(null=False)

	def __unicode__(self):
		return str(self.name)	

class Sport(models.Model):
	sport = models.CharField(max_length=100)

	def __unicode__(self):
		return str(self.sport)

class Team(models.Model):
	sport = models.ForeignKey(Sport)
	team_name = models.CharField(max_length=100)

	def __unicode__(self):
		return str(self.team_name)

class Game(models.Model):
	name = models.CharField(max_length=300)
	sport = models.ForeignKey(Sport, null=True)
	team1 = models.ForeignKey(Team, related_name="team1")
	team2 = models.ForeignKey(Team, related_name="team2")
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	active = models.BooleanField()

	def __unicode__(self):
		return str(self.name)	

class Bet(models.Model):
	Statuses = {
		('OPEN', 'OPEN'),
		('CLOSE', 'CLOSE'),
	}
	Choices = {
		('1', 'Choice 1'),
		('2', 'Choice 2'),
		('3', 'Choice 3')
	}
	name = models.CharField(max_length=200, null=True)
	game = models.ForeignKey(Game)
	player1 = models.ForeignKey(Customer, null=True, related_name="bet_player1")
	player2 = models.ForeignKey(Customer, null=True, related_name="bet_player2")
	player3 = models.ForeignKey(Customer, null=True, related_name="bet_player3")
	amount = models.IntegerField(null=False)
	status = models.CharField(max_length=5,default='CLOSE', choices=Statuses)
	winner = models.CharField(max_length=1, null=True, choices=Choices)

	def __unicode__(self):
		return str(self.name)	
