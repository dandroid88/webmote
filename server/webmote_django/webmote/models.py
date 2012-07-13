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
    location = models.CharField(max_length=100)

    def getSubclassInstance(self):
        for deviceType in Devices.__subclasses__():
            device = deviceType.objects.filter(name=self.name)
            if len(device):
                return device[0]
        return False

class DevicesForm(ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. Kitchen, Den, etc.'}))
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

    def performAction(self):
        return self.getSubclassInstance.performAction()

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
# http://wiki.python.org/moin/ModulesAsPlugins

#for dirName in os.listdir(MODULES_DIR):
#    print MODULES_DIR + dirName
#    from ...modules + dirName import models

#def find_modules(path="."):
#    """Return names of modules in a directory.

#    Returns module names in a list. Filenames that end in ".py" or
#    ".pyc" are considered to be modules. The extension is not included
#    in the returned list.
#    """
#    modules = set()
#    for filename in os.listdir(path):
#        module = None
#        if filename.endswith(".py"):
#            module = filename[:-3]
#        #elif filename.endswith(".pyc"):
#        #    module = filename[:-4]
#        if module is not None:
#            modules.add(module)
#    return list(modules)

#def load_module(name, path="."):
#    """Return a named module found in a given path."""
#    (file, pathname, description) = imp.find_module(name, path)
#    return imp.load_module(name, file, pathname, description)

#modules = []
##for dirName in os.listdir(MODULES_DIR):
#modules += [load_module(name, MODULES_DIR + os.listdir(MODULES_DIR)[0]) for name in find_modules(MODULES_DIR + os.listdir(MODULES_DIR)[0])]

