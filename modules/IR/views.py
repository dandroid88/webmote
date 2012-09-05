from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from IR.models import *

@login_required
def main(request):
    context = {}
    context['transceivers'] = IR_Transceivers.objects.all()
    context['devices'] = IR_Devices.objects.all()
    return render_to_response('ir.html', context, context_instance=RequestContext(request))

@login_required
def transceivers(request):
    context = {}
    if request.method == 'POST':
        if 'addTransceiver' in request.POST:
            newTForm = IR_TransceiversForm(request.POST)
            if newTForm.is_valid():
                newTran = newTForm.save()
                newTran.assignID()
            else:
                context['error'] = "Transciever was invalid."
        elif 'deleteTransceiver' in request.POST:
            IR_Transceivers.objects.filter(id=request.POST['deleteTransceiver'])[0].delete()
        elif 'resetTransceivers' in request.POST:
            resetAllTransceivers()
    context['transceivers'] = IR_Transceivers.objects.all()
    context['transceiversForm'] = IR_TransceiversForm()
    return render_to_response('transceiver.html', context, context_instance=RequestContext(request))

@login_required
def transceiverSearch(request):
    return searchForTransceiver()

@login_required
def devices(request):
    context = {}
    if request.method == 'POST':
        if 'addDevice' in request.POST:
            newDeviceForm = IR_DevicesForm(request.POST)
            if newDeviceForm.is_valid():
                newDeviceForm.save()
            else:
                context['error'] = "Device was invalid."
        elif 'deleteDevice' in request.POST:
            IR_Devices.objects.filter(id=request.POST['deleteDevice'])[0].delete()
    context['devices'] = IR_Devices.objects.select_related().all()
    context['deviceForm'] = IR_DevicesForm()
    return render_to_response('devices.html', context, context_instance=RequestContext(request))

@login_required
def actions(request):
    return render_to_response('actions.html', context, context_instance=RequestContext(request))

@login_required
def device(request, num="1"):
    context = {}
    device = Devices.objects.filter(id=int(num))[0]
    deviceForm = IR_DevicesForm()
    actionForm = IR_ActionsForm()
    if request.method == 'POST':
        if 'updateDevice' in request.POST:
            updatedDevice = deviceForm(request.POST, instance=device.getSubclassInstance())
            if updatedDevice.is_valid():
                updatedDevice.save()
            else:
                context['error'] = "New value(s) was invalid."
        elif 'addAction' in request.POST:
            actionType = device.getCorrespondingCommandType()
            action = actionType(device=device)
            newAction = actionForm(request.POST, instance=action)
            if newAction.is_valid():
                newAction.save()
            else:
                context['error'] = "Action was invalid."
        elif 'deleteAction' in request.POST:
            IR_Actions.objects.filter(id=request.POST['deleteAction']).delete()
    device = Devices.objects.filter(id=int(num))[0]
    context['device'] = device
    context['deviceForm'] = IR_DevicesForm(instance=device.getSubclassInstance())
    context['actions'] = device.actions_set.all()
    context['actionForm'] = actionForm
    return render_to_response('device.html', context, context_instance=RequestContext(request))


@login_required
def runActionView(request, deviceNum="1", action="0"):
    # should be a permissions check here if it isn't already in the runcommand...
    context = runAction(deviceNum, action)
    return render_to_response('index.html', context, context_instance=RequestContext(request))


@login_required
def recordAction(request):
    if request.method == 'POST':
        newActionInfo = simplejson.loads(request.raw_post_data)
        device = Devices.objects.filter(id=int(newActionInfo[0]))[0]
        action = IR_Actions(device=device, name=newActionInfo[1])
        if action.recordAction():
            action.save()
        print 'returned'
    return HttpResponse(simplejson.dumps(''), mimetype='application/javascript')

@login_required
def importIR(request):
    context = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            device = Devices.objects.filter(id=int(request.POST['device']))[0]
            readCodes = False
            codeType = 0
            codeLen = 0
            for line in f:
                if 'end codes' in line:
                    readCodes = False

                if readCodes:
                    name, code = line.split()
                    code = str(codeType) + str(codeLen) + code[2:]
                    action = IR_Actions(name=name, code=code, device=device)
                    action.save()

                if 'begin codes' in line:
                    readCodes = True
    else:
        context['form'] = UploadFileForm()
    return render_to_response('import.html', context, context_instance=RequestContext(request))

@login_required
def exportIR(request):
    return HttpResponse(simplejson.dumps(''), mimetype='application/javascript')

@login_required
def lirc(request):
    return HttpResponse(simplejson.dumps(''), mimetype='application/javascript')

##################
# Helper Functions 
##################

def searchForTransceiver():
    msg = False
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        msg = str(ser.readline())
    except Exception, exc:
        print str(exc)
    return HttpResponse(simplejson.dumps({'deviceType' : msg.split('_')[0] }), mimetype='application/javascript')

def resetAllTransceivers():
    IR_Transceivers.objects.all().delete()
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        ser.write('reset')
    except Exception, exc:
        print str(exc)
