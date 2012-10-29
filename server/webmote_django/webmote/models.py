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

    def __unicode__(self):
        return u'%s' % (self.name)

class DevicesForm(ModelForm):
    class Meta:
        model = Devices


#################
# Webmote Action
#################

class Actions(models.Model):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Devices, null=True)

    def getSubclassInstance(self):
        for actionType in Actions.__subclasses__():
            action = actionType.objects.filter(name=self.name, device=self.device)
            if len(action):
                return action[0]
        return False

    def runAction(self):
        return self.getSubclassInstance().runAction()

    def getTransceiver(self):
        transceiver = Transceivers.objects.filter(id=self.device.getSubclassInstance().transceiver.id)[0]
        return transceiver if transceiver else False

    def __unicode__(self):
        if self.device:
            return u'%s (%s)' % (self.name, self.device)
        else:
            action = self.getSubclassInstance()
            return u'%s (%s)' % (action.name, type(action).__name__)

class ActionsForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. On, Off, etc.'}))
    class Meta:
        model = Actions

################
# Transcievers
################

class Transceivers(models.Model):
    location = models.CharField(max_length=100)
    usbPort = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    class Meta:
        app_label = 'webmote'

    def assignID(self, reset = False):
        try:
            ser = serial.Serial('/dev/' + self.usbPort, 9600)
            if reset:
                ser.write("%04x" % self.id + 'a'.encode("hex") + "%04x" % 0)
                print 'Deleting Transceiver ' + str(self.id)
            else:
                ser.write("%04x" % 0 + 'a'.encode("hex") + "%04x" % self.id)
                print 'Assigned Tranceiver ID: ' + str(self.id)
        except Exception, exc:
            print str(exc)
        
    def delete(self, *args, **kwargs):
        self.assignID(True)
        super(Transceivers, self).delete(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (self.location)

class TransceiversForm(ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'e.g. Kitchen, Den, etc.'}))
    usbPort = forms.CharField(widget=forms.HiddenInput())
    type = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Transceivers
        app_label = 'webmote'

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
