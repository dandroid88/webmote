from django.db import models
from django.forms import ModelForm
from django import forms
from django.forms.widgets import *
from django.contrib.auth.models import User
from webmote_django.settings import MODULES_DIR
import serial, sys, os, glob, time, imp
import struct

################
# Webmote Device
################

class Devices(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def getSubclassInstance(self):
        for deviceType in Devices.__subclasses__():
            device = deviceType.objects.filter(name=self.name)
            if len(device):
                return device[0]
        return False

class DevicesForm(ModelForm):
    class Meta:
        model = Devices


#################
# Webmote Action
#################

class Actions(models.Model):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Devices)

    def getSubclassInstance(self):
        for actionType in Actions.__subclasses__():
            action = actionType.objects.filter(name=self.name, device=self.device)
            if len(action):
                return action[0]
        return False

    def runAction(self):
        return self.getSubclassInstance().runAction()

class ActionsForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. On, Off, etc.'}))
    class Meta:
        model = Actions

#################
# Users Info
#################

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserPermissions(models.Model):
    user = models.ForeignKey(User)
    device = models.ForeignKey(Devices)
    #action ???

########################
# Load Modules models.py
########################
sys.path.append(os.path.abspath(MODULES_DIR))
for dirName in os.listdir(MODULES_DIR):
    try:
        __import__(dirName + '.models')
        print 'Loading ' + dirName + ' plugin (models).'
    except:
        print 'Failed to load ' + dirName + ' plugin (models).'
del sys.path[-1]