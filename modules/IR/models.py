from webmote_django.webmote.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.widgets import *

################
# IR Devices
################

class IR_Devices(Devices):
    brand = models.CharField(max_length=100, blank=True)
    deviceModelNumber = models.CharField(max_length=100, blank=True)
    remoteModelNumber = models.CharField(max_length=100, blank=True)
    transceiver = models.ForeignKey(Transceivers)
    class Meta:
        app_label = 'webmote'

class IR_DevicesForm(DevicesForm):
    brand = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. Sony, Panasonic, etc. (optional)'}))
    deviceModelNumber = forms.CharField(required=False, label='Device model number', widget=forms.TextInput(attrs={'placeholder': 'e.g. abc123 (optional)'}))
    remoteModelNumber = forms.CharField(required=False, label='Remote model number', widget=forms.TextInput(attrs={'placeholder': 'e.g. abc123 (optional)'}))
    transceiver = forms.ModelChoiceField(queryset=Transceivers.objects.filter(type='IR'))
    class Meta:
        model = IR_Devices
        app_label = 'webmote'

################
# IR Actions
################

class IR_Actions(Actions):
    code = models.CharField(max_length=300)
    class Meta:
        app_label = 'webmote'

    def recordAction(self):
        transceiver = self.getTransceiver()
        if transceiver:
            try:
                print '/dev/' + transceiver.usbPort
                ser = serial.Serial('/dev/' + transceiver.usbPort, 9600)
                message = "%04x" % transceiver.id + 'r'.encode("hex")
                ser.write(message)
                print message
                print 'Recording...'
                self.code = str(ser.readline())
                print 'Recorded Command Succesfully: ' + self.code
                return True
            except:
                print 'Failed to record'
                return False
        else:
            print 'Couldn\'t find transceiver for device'
            return False

    def runAction(self):
        transceiver = self.getTransceiver()
        if transceiver:
            try:
                ser = serial.Serial('/dev/' + transceiver.usbPort, 9600)
                message = "%04x" % transceiver.id + 'p'.encode("hex") + str(self.code)
                ser.write(message)
                print message
            except:
                print 'Failed to play'
                return False
        else:
            print 'Couldn\'t find transceiver for action'
            return False


class IR_ActionsForm(ActionsForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 1110211'}))
    class Meta:
        model = IR_Actions
        exclude = ('device',)
        app_label = 'webmote'


##################
# Import/Export Functions
##################

class UploadFileForm(forms.Form):
    device = forms.ModelChoiceField(queryset=IR_Devices.objects.all())
    file  = forms.FileField()
    class Meta:
        app_label = 'webmote'

##################
# Helper Functions
##################

