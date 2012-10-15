from webmote_django.webmote.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

################
# Remotes
################

STYLES = (
    (1, 'Grid'),
    (2, 'List (not implemented)'),
    (3, 'Custom (not implemented)'),
)

class Remote(models.Model):
    name = models.CharField(max_length=100)
    style = models.IntegerField(choices=STYLES)
    user = models.ForeignKey(User)
    rows = models.IntegerField()
    class Meta:
        app_label = 'webmote'

class RemoteForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'e.g. Watch TV, Lights, etc.'}))
    style = forms.ChoiceField(choices=STYLES)
    rows = forms.IntegerField(min_value=1, max_value=20, widget=forms.TextInput(attrs={'placeholder' : 'a number between 1 and 20'}))
    class Meta:
        model = Remote
        exclude = ('user',)
        app_label = 'webmote'

################
# Buttons
################
ICONS = (
    ('arrow-l', 'Left Arrow'),
    ('arrow-r', 'Right Arrow'),
    ('arrow-u', 'Up Arrow'),
    ('arrow-d', 'Down Arrow'),
    ('delete', 'Delete'),
    ('plus', 'Plus'),
    ('minus', 'Minus'),
    ('check', 'Check'),
    ('gear', 'Gear'),
    ('refresh', 'Refresh'),
    ('forward', 'Forward'),
    ('back', 'Back'),
    ('grid', 'Grid'),
    ('star', 'Star'),
    ('alert', 'Alert'),
    ('info', 'Info'),
    ('home', 'Home'),
    ('search', 'Search'),
)

COLORS = (
    ('a', 'Dark Gray'),
    ('b', 'Blue'),
    ('d', 'Light Gray'),
    ('e', 'Yellow'),
)

class Button(models.Model):
    name = models.CharField(max_length=100, null=True)
    x = models.IntegerField()
    y = models.IntegerField()
    icon = models.CharField(max_length=50, choices=ICONS)
    color = models.CharField(max_length=1, choices=COLORS)
    action = models.ForeignKey(Actions, null=True)
    url = models.CharField(max_length=1000, null=True)
    remote = models.ForeignKey(Remote)
    class Meta:
        app_label = 'webmote'

class ButtonForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'e.g. Volume Up, Light On, etc.'}))
    icon = forms.ChoiceField(choices=ICONS)
    color = forms.ChoiceField(choices=COLORS)
    class Meta:
        model = Button
        exclude = ('x', 'y', 'command', 'macro', 'url', 'remote')
        app_label = 'webmote'
