from webmote_django.webmote.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.widgets import *

USB_PORT = '/dev/ttyUSB0'

################
# Transcievers
################

class IR_Transceivers(models.Model):
    location = models.CharField(max_length=100)
    class Meta:
        app_label = 'webmote'

    def assignID(self, reset = False):
        try:
            ser = serial.Serial(USB_PORT, 9600)
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
        super(IR_Transceivers, self).delete(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (self.location)

class IR_TransceiversForm(ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'e.g. Kitchen, Den, etc.'}))
    class Meta:
        model = IR_Transceivers
        app_label = 'webmote'

################
# IR Devices
################

class IR_Devices(Devices):
    brand = models.CharField(max_length=100, null=True)
    deviceModelNumber = models.CharField(max_length=100, null=True)
    remoteModelNumber = models.CharField(max_length=100, null=True)
    transceiver = models.ForeignKey(IR_Transceivers)
    class Meta:
        app_label = 'webmote'

class IR_DevicesForm(DevicesForm):
    brand = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. Sony, Panasonic, etc. (optional)'}))
    deviceModelNumber = forms.CharField(required=False, label='Device Model Number', widget=forms.TextInput(attrs={'placeholder': 'e.g. abc123 (optional)'}))
    remoteModelNumber = forms.CharField(required=False, label='Remote Model Number', widget=forms.TextInput(attrs={'placeholder': 'e.g. abc123 (optional)'}))
    transceiver = forms.ModelChoiceField(queryset=IR_Transceivers.objects.all())
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

    def getTransceiverID(self):
        transceiver = IR_Transceivers.objects.filter(location=self.device.getSubclassInstance().transceiver.location)
        return transceiver[0].id if transceiver else False

    def recordAction(self):
        transceiverID = self.getTransceiverID()
        if transceiverID:
            try:
                ser = serial.Serial(USB_PORT, 9600)
                message = "%04x" % transceiverID + 'r'.encode("hex")
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
        transceiverID = self.getTransceiverID()
        if transceiverID:
            try:
                ser = serial.Serial(USB_PORT, 9600)
                message = "%04x" % transceiverID + 'p'.encode("hex") + str(self.code)
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
# Helper Functions
##################

def sendTOTransceiver(id, command, data):
    print 'not implemented'

