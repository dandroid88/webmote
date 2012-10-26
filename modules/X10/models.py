from webmote_django.webmote.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.widgets import *

USB_PORT = '/dev/ttyUSB1'

################
# Transcievers
################

class X10_Transceivers(models.Model):
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
        super(X10_Transceivers, self).delete(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (self.location)

class X10_TransceiversForm(ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'e.g. Kitchen, Den, etc.'}))
    class Meta:
        model = X10_Transceivers
        app_label = 'webmote'

#############
# X10 Devices
#############

# These values are directly from the 
# x10constants.h file from the arduino x10 library.
HOUSE_CODES = {
    'A': 'B0110',
    'B': 'B1110',
    'C': 'B0010',
    'D': 'B1010',
    'E': 'B0001',
    'F': 'B1001',
    'G': 'B0101',
    'H': 'B1101',
    'I': 'B0111',
    'J': 'B1111',
    'K': 'B0011',
    'L': 'B1011',
    'M': 'B0000',
    'N': 'B1000',
    'O': 'B0100',
    'P': 'B1100',
}

UNIT_CODES = {
    '1': 'B01100',
    '2': 'B11100',
    '3': 'B00100',
    '4': 'B10100',
    '5': 'B00010',
    '6': 'B10010',
    '7': 'B01010',
    '8': 'B11010',
    '9': 'B01110',
    '10': 'B11110',
    '11': 'B00110',
    '12': 'B10110',
    '13': 'B00000',
    '14': 'B10000',
    '15': 'B01000',
    '16': 'B11000',
}

COMMAND_CODES = {
    'ALL_UNITS_OFF': 'B00001',
    'ALL_LIGHTS_ON': 'B00011',
    'ON': 'B00101',
    'OFF': 'B00111',
    'DIM': 'B01001',
    'BRIGHT': 'B01011',
    'ALL_LIGHTS_OFF': 'B01101',
    'EXTENDED_CODE': 'B01111',
    'HAIL_REQUEST': 'B10001',
    'HAIL_ACKNOWLEDGE': 'B10011',
    'PRE_SET_DIM': 'B10101',
    'EXTENDED_DATA': 'B11001',
    'STATUS_ON': 'B11011',
    'STATUS_OFF': 'B11101',
    'STATUS_REQUEST': 'B11111',
}


class X10_Devices(Devices):
    house = models.CharField(max_length=1)
    unit = models.IntegerField()
    state = models.IntegerField(default=0)
    lastCommand = models.IntegerField(null=True)
    class Meta:
        app_label = 'webmote'

    def save(self, *args, **kwargs):
        super(X10_Devices, self).save(*args, **kwargs)
        for command in COMMAND_CODES:
            newCommand = X10_Actions(name=command, device=self, code=COMMAND_CODES[command])
            newCommand.save()

class X10_DevicesForm(DevicesForm):
    house = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A letter A-P'}))
    unit = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'A number 1-16'}))
    class Meta:
        model = X10_Devices
        exclude = ('state', 'lastCommand')
        app_label = 'webmote'

class X10_Actions(Actions):
    code = models.CharField(max_length=10)
    class Meta:
        app_label = 'webmote'

    def getTransceiverID(self):
        transceiver = X10_Transceivers.objects.filter(location=self.device.getSubclassInstance().transceiver.location)
        return transceiver[0].id if transceiver else False

    def runAction(self):
        transceiverID = self.getTransceiverID()
        if transceiverID:
            try:
                ser = serial.Serial(USB_PORT, 9600)
                message = "%04x" % transceiverID + 'p'.encode("hex")
                message = chr(int(HOUSE_CODES[device.house].replace('B', '0b0000'), 2)).encode("hex")
                message += chr(int(UNIT_CODES[str(device.unit)].replace('B', '0b000'), 2)).encode("hex")
                message += chr(int(COMMAND_CODES[self.name].replace('B', '0b000'), 2)).encode("hex")
                ser.write(message)
                print message
            except:
                print 'Failed to play'
                return False
        else:
            print 'Couldn\'t find transceiver for action'
            return False

#    def runAction(self):
#        device = self.device.getSubclassInstance()
#        try:
#            dev = USB_PORT
#            ser = serial.Serial(dev, 9600)
#            message = chr(int(HOUSE_CODES[device.house].replace('B', '0b0000'), 2))
#            message += chr(int(UNIT_CODES[str(device.unit)].replace('B', '0b000'), 2))
#            message += chr(int(COMMAND_CODES[self.name].replace('B', '0b000'), 2))
#            ser.write(message)
#            print 'Ran \'' + self.name + '\' on \'' + device.name + '\' (X10)'
#            return True
#        except:
#            print 'FAILED to run \'' + self.name + '\' on \'' + device.name + '\' (X10)'
#            return False



class X10_ActionsForm(ActionsForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 1110211'}))
    class Meta:
        model = X10_Actions
        exclude = ('state', 'device', 'code', 'lastCommand')
        app_label = 'webmote'

