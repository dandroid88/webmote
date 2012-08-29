from webmote_django.webmote.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

################
# IR Devices
################

################
# Transcievers
################

class Transceivers(models.Model):
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    class Meta:
        app_label = 'webmote'

    def assignID(self, reset = False):
        try:
            ser = serial.Serial('/dev/ttyUSB0', 9600)
            if reset:
                ser.write("%04x" % self.id + 'a'.encode("hex") + "%04x" % 0)
            else:
                ser.write("%04x" % 0 + 'a'.encode("hex") + "%04x" % self.id)
            print 'Assigned Tranceiver ID: ' + str(self.id)
        except Exception, exc:
            print str(exc)
        
    def delete(self, *args, **kwargs):
        self.assignID(True)
        print 'resetting transceiver'
        super(Transceivers, self).delete(*args, **kwargs)

class TransceiversForm(ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'e.g. Kitchen, Den, etc.'}))
    type = forms.CharField(widget=forms.TextInput(attrs={'readonly' : True}))
    class Meta:
        model = Transceivers
        exclude = ('trans_id',)
        app_label = 'webmote'
