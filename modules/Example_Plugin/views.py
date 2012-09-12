from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from Example_Plugin.models import *

@login_required
def main(request):
    context = {}
    context['devices'] = Example_Devices.objects.all()
    context['actions'] = Example_Actions.objects.all()
    return render_to_response('example.html', context, context_instance=RequestContext(request))

@login_required
def instructions(request, num="0"):
    context = {}
    context['devices'] = Example_Devices.objects.all()
    context['actions'] = Example_Actions.objects.all()
    return render_to_response('instructions.html', context, context_instance=RequestContext(request))
