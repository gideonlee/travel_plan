from __future__ import unicode_literals
from django.db import models
import bcrypt
from datetime import datetime 



# Create your models here.
class UserManager(models.Manager):
	def validate_register(self, **k):
		errors = []
		if len(k['name']) < 3:
			errors.append('Name must be at least 3 characters long.')
		if len(k['username']) < 3:
			errors.append('Username must be at least 3 characters long.')
		if k['password'] != k['confirm_password']:
			errors.append('Passwords do not match.')
		if len(k['password']) < 8:
			errors.append('Password must be at least 8 characters long.')

		for error in errors:
			print error
		if errors: 
			return (False, errors)
		else:
			input_pw = k['password'].encode()
			hashed = bcrypt.hashpw(input_pw, bcrypt.gensalt())
			user = User.objects.create(name=k['name'], username=k['username'], password=hashed)
			return (True, user.id)

	def validate_login(self, **k):
		try:
			user = User.objects.get(username__iexact=k['username'])
			
			input_pw = k['password'].encode()
			hashed_pw = user.password.encode()

			if bcrypt.hashpw(input_pw, hashed_pw) == hashed_pw: 
				print '*'*50
				print user.id 
				return (True, user.id)
			else:
				return (False, 'Invalid Password')
		except:
			return (False, 'Invalid User/Login.')

class TravelManager(models.Manager):
	def validate_travel(self, **k):
		errors = []
		if len(k['destination']) < 1:
			errors.append('Destination cannot be blank.')
		if len(k['description']) < 1: 
			errors.append('You must enter a description.')
		if k['date_from'] == '':
			errors.append('You must enter a start date.')
		if k['date_to'] == '':
			errors.append('You must enter an end date.')

		if errors:
			return (False, errors)

		now = datetime.now()
		
		year = int(now.strftime('%Y'))
		month = int(now.strftime('%m'))
		day = int(now.strftime('%d'))

		df_year = int(k['date_from'][:4])
		df_month = int(k['date_from'][5:7])
		df_day = int(k['date_from'][8:10])

		dt_year = int(k['date_to'][:4])
		dt_month = int(k['date_to'][5:7])
		dt_day = int(k['date_to'][8:10])

		# 2016
		if year > df_year: 
			errors.append('It is the year '+str(year)+'. You must leave on a valid date.')

		if year == df_year:
			if month > df_month:
				errors.append('It is already month '+str(month)+'. You cannot leave on month '+str(df_month)+' without a time machine.')
		if year == df_year:
			if month == df_month:
				if day > df_day:
					errors.append('It is already day '+str(day)+' of the month. You cannot leave on day '+str(df_day)+' without a time machine.')

		if df_year > dt_year:
			errors.append('You cannot return before you leave.')

		if df_year == dt_year:
			if df_month > dt_month: 
				errors.append('You cannot return before you leave.')

		if df_year == dt_year:
			if df_month == dt_month:
				if df_day > dt_day:
					errors.append('You cannot return before you leave.')


		if errors:
			return (False, errors)
		else: 
			Travel.objects.create(destination=k['destination'], description=k['description'], date_from=k['date_from'], date_to=k['date_to'], user=k['user'])
			return (True, errors)
	def join_trip(self, **k):
		trip = Travel.objects.get(id=k['travel_id'])
		Travel.objects.create(destination=trip.destination, description=trip.description, date_from=trip.date_from, date_to=trip.date_to, user=k['user'])
		return 'Successfully Added Trip.'

class User(models.Model):
	name = models.CharField(max_length=45)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Travel(models.Model):
	destination = models.CharField(max_length=255)
	description = models.TextField(max_length=1000)
	user = models.ForeignKey(User, related_name='travelusers')
	date_from = models.DateField()
	date_to = models.DateField() 
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TravelManager()

