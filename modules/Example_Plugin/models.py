from webmote_django.webmote.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.widgets import *

#################
# Example Device
#################

class Example_Devices(Devices):
    brand = models.CharField(max_length=100, blank=True)
    class Meta:
        app_label = 'webmote'


class Example_DeviceForm(DevicesForm):
    brand = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. Sony, Panasonic, etc. (optional)'}))
    class Meta:
        model = Example_Devices
        app_label = 'webmote'


#################
# Example Action
#################

class Example_Actions(Actions):
    code = models.CharField(max_length=300)
    class Meta:
        app_label = 'webmote'

    def runAction(self):
        print 'Ran Action'

class Example_ActionsForm(ActionsForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 1110211'}))
    class Meta:
        model = Example_Actions
        app_label = 'webmote'
