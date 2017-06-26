# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Secret
from django.db.models import Count

# Create your views here.

def index(request):
	return render(request, 'secret/index.html')

def register(request):
	result = User.objects.register(request.POST)
	if isinstance(result, int):
		#validation successful
		request.session['userid'] = result
		return redirect('/secrets')
	else:
		#unsuccessful, flash messages
		for error in result:
			messages.add_message(request, messages.ERROR, error)
	return redirect('/')

def login(request):
	try:
		result = User.objects.login(request.POST)
		if isinstance(result, int):
			#login successful
			request.session['userid'] = result
			return redirect('/secrets')
		else:
			#unsuccessful, flash messages
			for error in result:
				messages.add_message(request, messages.ERROR, error)
		return redirect('/')
	except:
		messages.add_message(request, messages.ERROR, 'User authentication failed')
		return redirect('/')

def secrets(request):
	if not 'userid' in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['userid'])
	context = {
		'userinfo' : user,
		'userlikes' : Secret.objects.filter(likes=user),
		'10recentsecrets': Secret.objects.all().order_by('-created_at')[:10],
		}
	return render(request, 'secret/home.html', context)

def secretsubmit(request):
	if not 'userid' in request.session:
		return redirect('/')
	if not 'secrettext' in request.POST:
		messages.add_message(request, messages.ERROR, 'Please submit a secret')
		return redirect('/secrets')
	user = User.objects.get(id=request.session['userid'])
	Secret.objects.create(secrettext=request.POST['secrettext'], user=user)
	return redirect('/secrets')

def likesecret(request, secretid):
	if not 'userid' in request.session:
		return redirect('/')
	this_user = User.objects.get(id=request.session['userid'])
	this_secret = Secret.objects.get(id=secretid)
	this_secret.likes.add(this_user)
	return redirect('/secrets')

def deletesecret(request, secretid):
	if not 'userid' in request.session:
		return redirect('/')
	this_secret = Secret.objects.get(id=secretid)
	this_secret.delete()
	return redirect('/secrets')

def popularsecrets(request):
	if not 'userid' in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['userid'])
	context ={
		'userinfo' : user,
		'userlikes' : Secret.objects.filter(likes=user.id),
		'popularsecrets' : Secret.objects.all().annotate(num=Count('likes')).order_by('-num'),
	}
	return render(request, 'secret/popular.html', context)

def mysecrets(request):
	if not 'userid' in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['userid'])
	context = {
		'userinfo' : user,
		'userlikes' : Secret.objects.filter(likes=user.id),
		'mysecrets': Secret.objects.all().filter(user=user.id).filter(likes=user.id).order_by('-created_at')
	}
	return render(request, 'secret/mysecrets.html', context)

def otherssecrets(request):
	if not 'userid' in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session['userid'])
	context = {
		'userinfo' : user,
		'userlikes' : Secret.objects.filter(likes=user.id),
		'otherssecrets': Secret.objects.exclude(user=user.id).exclude(likes=user.id).order_by('-created_at')
	}
	return render(request, 'secret/otherssecrets.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')