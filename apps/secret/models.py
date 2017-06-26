# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from dateutil.relativedelta import relativedelta
import re, bcrypt, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	#register function
	def register(self, data):
		errors = []
		#check on first name alphabets only
		if not data['fname'].isalpha():
			errors.append('First name may only contain letters')
		
		#check on first name length
		if len(data['fname']) < 1:
			errors.append('First name must be longer than 1 character')
		
		#check on last name alphabets only
		if not data['lname'].isalpha():
			errors.append('Last name may only contain letters')
		
		#check on last name length
		if len(data['lname']) < 1:
			errors.append('Last name must be longer than 1 character')
		
		#check if email is input
		if len(data['email']) < 1:
			errors.append('Email required')
		
		#email format check
		if not EMAIL_REGEX.match(data['email']):
			errors.append('Email must be in valid format')
		
		#age check
		try:
			birthdate = datetime.datetime.strptime(data['bday'], '%Y-%m-%d')
			today = datetime.datetime.today()
			age = relativedelta(today, birthdate)
			if age.years < 18:
				errors.append('You must be 18 years or older to register')
		except:
			pass
		
		#password length check
		if len(data['password']) < 8:
			errors.append('Password must be 8 characters or longer')
		
		#password & password confirm check
		if data['password'] != data['confirm']:
			errors.append('Passwords must match') 
		
		#checking if passed error checks
		if len(errors) == 0:
			#using get to see if there are multiple users with said email
			#if .get() errors out, user with that email already exists.
			try:
				User.objects.get(email=data['email'])
				errors.append('User with that email already exists')
				return errors
			except: 
				user = User.objects.create(fname=data['fname'], lname=data['lname'], email=data['email'], birthday=data['bday'],password=bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()))
				return user.id
		else:
			return errors

	def login(self, data):
		errors = []
		if len(data['email']) < 1:
			errors.append('Email required')
		
		if not EMAIL_REGEX.match(data['email']):
			errors.append('Email must be in valid format')
		
		if len(data['password']) < 8:
			errors.append('Password must be 8 characters or longer')
		
		if len(errors) == 0:
			try:
				user = User.objects.get(email__iexact=data['email'])
				encrypted_pw = bcrypt.hashpw(data['password'].encode(), user.password.encode())
				if encrypted_pw == user.password.encode():
					return user.id
			except: 
				errors.append('User authentication failed')
				return errors
		else:
			return errors

class User(models.Model):
	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	birthday = models.DateField()
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	#to use UserManager
	objects = UserManager()

class Secret(models.Model):
	secrettext = models.TextField()
	user = models.ForeignKey(User, related_name="secret_posted")
	likes = models.ManyToManyField(User, related_name="secret_liked")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)