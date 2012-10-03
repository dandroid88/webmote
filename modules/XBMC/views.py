from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from XBMC.models import *

@login_required
def hosts(request):
    context = {}
    if request.method == 'POST':
        if 'addDevice' in request.POST:
            newDeviceForm = XBMC_DeviceForm(request.POST)
            if newDeviceForm.is_valid():
                newDevice = newDeviceForm.save()
                newDevice.saveInputActions()
            else:
                context['error'] = "Device was invalid."
        elif 'deleteDevice' in request.POST:
            XBMC_Devices.objects.filter(id=request.POST['deleteDevice'])[0].delete()
    context['devices'] = XBMC_Devices.objects.all()
    context['deviceForm'] = XBMC_DeviceForm()
    return render_to_response('hosts.html', context, context_instance=RequestContext(request))

@login_required
def host(request, num="0"):
    context = {}
    if request.method == 'POST':
        if 'updateDevice' in request.POST:
            updatedDevice = XBMC_DeviceForm(request.POST, instance=XBMC_Devices.objects.filter(id=int(num))[0])
            if updatedDevice.is_valid():
                updatedDevice.save()
            else:
                context['error'] = "New value(s) was invalid."
    context['devices'] = XBMC_Devices.objects.all()
    context['deviceForm'] = XBMC_DeviceForm(instance=XBMC_Devices.objects.filter(id=int(num))[0])
    return render_to_response('host.html', context, context_instance=RequestContext(request))
