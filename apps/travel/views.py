from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User, Trip
from datetime import datetime
import bcrypt

def index(req):
    return redirect('/main')

def main(req):
    if 'logged_in' not in req.session:
        req.session['logged_in'] = False
    if 'justloggedout' in req.session and req.session['justloggedout'] == True:
        messages.success(req, "You've been successfully logged out", extra_tags='logout')
        req.session['justloggedout'] = False
    if 'badlogin' in req.session and req.session['badlogin'] == True:
        messages.error(req, "You must be logged in to enter this webpage", extra_tags='logout')
        req.session['badlogin'] = False
    return render(req,'travel/login.html')

def register(req):
    req.session['first_name'] = req.POST['first_name']
    req.session['last_name'] = req.POST['last_name']
    req.session['username'] = req.POST['username']
    errors = User.objects.register_validator(req.POST)
    if len(errors):
        for key,value in errors.items():
            messages.error(req, value, key)
        return redirect('/main')
    else:
        hash1 = bcrypt.hashpw(req.POST['password'].encode(), bcrypt.gensalt())
        newuser = User(first_name=req.POST['first_name'], last_name=req.POST['last_name'], username=req.POST['username'], password=hash1)
        newuser.save()
        req.session['user'] = newuser.first_name
        req.session['id'] = newuser.id
        req.session['logged_in'] = True
        return redirect('/travels')

def login(req):
    req.session['login_username'] = req.POST['login_username']
    result = User.objects.filter(username=req.POST['login_username'])

    if not req.POST['login_username'] or not req.POST['login_password']:
        messages.error(req, 'Please fill out all fields', extra_tags='login')
    elif len(result):
        if bcrypt.checkpw(req.POST['login_password'].encode(), result[0].password.encode()):
            req.session['user'] = result[0].first_name
            req.session['id'] = result[0].id
            req.session['logged_in'] = True
            return redirect('/travels')
        else:
            messages.error(req, 'You could not be logged in...', extra_tags='login')
    else:
        messages.error(req, 'You have not registered', extra_tags='login')
    return redirect('/main')

def dashboard(req):
    if 'logged_in' in req.session and req.session['logged_in'] == True:
        context = {
            'mytrips': Trip.objects.distinct().filter(planner__id=req.session['id']).order_by('start_date') | Trip.objects.distinct().filter(joiners__id=req.session['id']).order_by('start_date'),
            'othertrips': Trip.objects.exclude(planner__id=req.session['id']).order_by('start_date') & Trip.objects.exclude(joiners__id=req.session['id']),
            'myself': User.objects.get(id=req.session['id'])
        }
        return render(req, 'travel/dashboard.html', context)
    req.session.clear()
    req.session['badlogin'] = True
    return redirect('/main')

def destination(req, id):
    return render(req, 'travel/destination.html', context={'dest': Trip.objects.get(id=id)})

def join(req,id):
    Trip.objects.get(id=id).joiners.add(User.objects.get(id=req.session['id']))
    messages.success(req, 'Successfully joined a new trip!', extra_tags='joined')
    return redirect('/travels')

def add(req):
    return render(req, 'travel/addplan.html')

def addnew(req):
    req.session['newdest'] = req.POST['newdest']
    req.session['newdesc'] = req.POST['newdesc']
    req.session['newfrom'] = req.POST['newfrom']
    req.session['newend'] = req.POST['newend']
    errors = Trip.objects.newtrip_validator(req.POST)
    if len(errors):
        for key,value in errors.items():
            messages.error(req, value, key)
        return redirect('/travels/add')
    else:
        Trip.objects.create(planner=User.objects.get(id=req.session['id']), destination=req.POST['newdest'], desc=req.POST['newdesc'], start_date=req.POST['newfrom'], end_date=req.POST['newend'])
        req.session['newdest'] = ''
        req.session['newdesc'] = ''
        req.session['newfrom'] = ''
        req.session['newend'] = ''
        return redirect('/travels')

def logout(req):
    req.session.clear()
    req.session['justloggedout'] = True
    return redirect('/main')



