from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User, Travel

# Create your views here.
def index(request):
	# User.objects.all().delete()
	return render(request, 'travel/index.html')

def register(request):
	result = User.objects.validate_register(name=request.POST['name'], username=request.POST['username'], password=request.POST['password'], confirm_password=request.POST['confirm_password'])
	if result[0]:
		request.session['user_id'] = result[1]
		return redirect(reverse('travel:dashboard'))		
	else: 
		for error in result[1]:
			messages.error(request, error)
		return redirect(reverse('travel:index'))

def login(request):
	result = User.objects.validate_login(username=request.POST['username'], password=request.POST['password'])
	if result[0]:
		request.session['user_id'] = result[1]
		return redirect(reverse('travel:dashboard'))
	else:
		messages.error(request, result[1])
		return redirect(reverse('travel:index'))

def dashboard(request):
	try: 
		user = User.objects.get(id=request.session['user_id'])
		trips = Travel.objects.filter(user=user)
		all_trips = Travel.objects.exclude(user=user)

		other_trips = []
		for dest in all_trips:
			found = False
			for trip in trips:
				if trip.destination == dest.destination:  
					found = True
			if not found:
				other_trips.append(dest)

		context = {
			'user': user,
			'trips': trips,
			'other_trips': other_trips,
		}
		return render(request, 'travel/dashboard.html', context)
	except:
		return redirect(reverse('travel:index'))	

def logout(request):
	request.session.clear()
	return redirect(reverse('travel:index'))

def add(request):
	return render(request, 'travel/add.html')

def process_add(request):
	user = User.objects.get(id=request.session['user_id'])
	result = Travel.objects.validate_travel(destination=request.POST['destination'], description=request.POST['description'], user=user, date_from=request.POST['date_from'], date_to=request.POST['date_to'])
	if result[0]:
		return redirect(reverse('travel:dashboard'))
	else: 
		for error in result[1]:
			messages.error(request, error)
	return redirect(reverse('travel:add'))

def show(request, id):
	trip = Travel.objects.get(id=id)
	trip_creator = Travel.objects.filter(destination=trip.destination).order_by('created_at').distinct()

	all_users = Travel.objects.filter(destination=trip.destination)

	users = []
	current = User.objects.get(id=request.session['user_id'])
	users.append(current)

	for user in all_users:
		found = False
		for i in users:
			if i.name == user.user.name:
				found = True
		if not found:
			users.append(user.user)
	users.pop(0)

	context = {
		'trip': trip_creator[0],
		'users': users,
	}
	return render(request, 'travel/show.html', context)

def process_join(request, travel_id):
	user = User.objects.get(id=request.session['user_id'])
	result = Travel.objects.join_trip(travel_id=travel_id, user=user)
	messages.success(request, result)
	return redirect(reverse('travel:dashboard'))