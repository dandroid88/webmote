from webmote_django.webmote.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.widgets import *
import jsonrpclib as jsonrpc

#############
# XBMC Device
#############

class XBMC_Devices(Devices):
    ip = models.CharField(max_length=15)
    port = models.CharField(max_length=5)
    username = models.CharField(max_length=50)
    #plaintext for now
    password = models.CharField(max_length=50)
    class Meta:
        app_label = 'webmote'

    def serverAddress(self):
        serverAddress = 'http://'
        if self.username:
            serverAddress += self.username
            if self.password:
                serverAddress += ':' + self.password
            serverAddress += '@'
        return serverAddress + self.ip + ':' + self.port + '/jsonrpc'      

    def getActions(self):
        server = jsonrpc.Server(self.serverAddress())
        return server.JSONRPC.Introspect()
    
    def getInputActions(self):
        inputActions = []
        for action in self.getActions()['methods']:
            if 'Input' in action:
                inputActions.append(action)
        return inputActions

    def saveInputActions(self):
        inputActions = self.getInputActions()
        for action in inputActions:
            newAction = XBMC_Actions(name=action, device=self, command=action)
            newAction.save()

class XBMC_DeviceForm(DevicesForm):
    ip = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. localhost, 192.168.1.1, etc.'}))
    port = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 8080 (default), 8081, etc.'}))
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '(optional)'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder': '(optional)'}, render_value=True))
    class Meta:
        model = XBMC_Devices
        app_label = 'webmote'

#################
# Example Action
#################

class XBMC_Actions(Actions):
    command = models.CharField(max_length=50)
    args = models.CharField(max_length=50, default='')
    class Meta:
        app_label = 'webmote'

    def runAction(self):
        server = jsonrpc.Server(self.device.getSubclassInstance().serverAddress())
        server._request(self.command, self.args)
        

