from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from X10.models import *

@login_required
def main(request):
    context = {}
    context['devices'] = X10_Devices.objects.all()
    return render_to_response('x10.html', context, context_instance=RequestContext(request))

@login_required
def help(request):
    context = {}
    return render_to_response('x10_help.html', context, context_instance=RequestContext(request))

@login_required
def devices(request):
    context = {}
    if request.method == 'POST':
        if 'addDevice' in request.POST:
            newDeviceForm = X10_DevicesForm(request.POST)
            if newDeviceForm.is_valid():
                newDeviceForm.save()
            else:
                context['error'] = "Device was invalid."
        elif 'deleteDevice' in request.POST:
            X10_Devices.objects.filter(id=request.POST['deleteDevice'])[0].delete()
    context['devices'] = X10_Devices.objects.select_related().all()
    context['deviceForm'] = X10_DevicesForm()
    return render_to_response('x10_devices.html', context, context_instance=RequestContext(request))

@login_required
def device(request, num="1"):
    context = {}
    device = Devices.objects.filter(id=int(num))[0]
    deviceForm = X10_DevicesForm()
    actionForm = X10_ActionsForm()
    if request.method == 'POST':
        if 'updateDevice' in request.POST:
            updatedDevice = deviceForm(request.POST, instance=device.getSubclassInstance())
            if updatedDevice.is_valid():
                updatedDevice.save()
            else:
                context['error'] = "New value(s) was invalid."
        elif 'deleteAction' in request.POST:
            X10_Actions.objects.filter(id=request.POST['deleteAction']).delete()
    device = Devices.objects.filter(id=int(num))[0]
    context['device'] = device
    context['deviceForm'] = X10_DevicesForm(instance=device.getSubclassInstance())
    context['actions'] = device.actions_set.all()
    return render_to_response('x10_device.html', context, context_instance=RequestContext(request))
