from __future__ import unicode_literals
from django.db import models
from datetime import datetime

class UserManager(models.Manager):
    def register_validator(self, postdata):
        errors = {}
        if not postdata['first_name']:
            errors['first_name'] = 'Please enter your first name'
        elif len(postdata['first_name']) < 3:
            errors['first_name'] = 'Must be at least 3 characters'

        if not postdata['last_name']:
            errors['last_name'] = 'Please enter your last name'
        elif len(postdata['last_name']) < 3:
            errors['last_name'] = 'Must be at least 3 characters'

        if not postdata['username']:
            errors['username'] = 'Please enter a username'
        elif len(postdata['username']) < 3:
            errors['username'] = 'Must be at least 3 characters'

        if not postdata['password']:
            errors['password'] = 'Please enter a password'
        elif len(postdata['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if not postdata['confirm_password']:
            errors['confirm_password'] = 'Please confirm your password'
        elif postdata['confirm_password'] != postdata['password']:
            errors['confirm_password'] = 'Passwords do not match'
        
        return errors

class TripManager(models.Manager):
    def newtrip_validator(self, postdata):
        errors = {}
        if not postdata['newdest']:
            errors['newdest'] = 'Please enter a new destination'
        if not postdata['newdesc']:
            errors['newdesc'] = 'Please enter a new description'

        if not postdata['newfrom']:
            errors['newfrom'] = 'Please enter a new start date'
        elif datetime.strptime(postdata['newfrom'], '%Y-%m-%d') < datetime.now():
            errors['newfrom'] = 'Date must be in the future'

        if not postdata['newend']:
            errors['newend'] = 'Please enter a new end date'
        elif datetime.strptime(postdata['newend'], '%Y-%m-%d') < datetime.now():
            errors['newend'] = 'Date must be in the future'
        elif datetime.strptime(postdata['newend'], '%Y-%m-%d') < datetime.strptime(postdata['newfrom'], '%Y-%m-%d'):
            errors['newend'] = 'End date must be after the start date'
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    def __repr__(self):
        return "<User: {} {}>".format(self.first_name, self.last_name)

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    planner = models.ForeignKey(User, related_name="plannedtrips")
    joiners = models.ManyToManyField(User, related_name='joinedtrips')
    objects = TripManager()
    def __str__(self):
        return self.destination