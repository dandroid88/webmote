from webmote_django.webmote.models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.forms.widgets import *
import time

#################
# Macro Action
#################

class Macro(Actions):
    before = models.ForeignKey('self', null=True, related_name='macro_before')
    after = models.ForeignKey('self', null=True, related_name='macro_after')
    action = models.ForeignKey(Actions, null=True, related_name='macro_action')
    delay = models.IntegerField(default=1)
    visible = models.BooleanField(default=False)
    class Meta:
        app_label = 'webmote'

    def runAction(self):
        if self.action:
            self.action.runAction()

        time.sleep(float(self.delay))

        if self.after:
            self.after.runAction()

