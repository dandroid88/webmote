from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from IR.models import *

@login_required
def main(request):
    return render_to_response('ir.html', context_instance=RequestContext(request))

@login_required
def transceivers(request):
    if request.user.is_superuser:
        context = {}
        if request.method == 'POST':
            if 'addTransceiver' in request.POST:
                newTForm = TransceiversForm(request.POST)
                if newTForm.is_valid():
                    newTran = newTForm.save()
                    newTran.assignID()
                else:
                    context['error'] = "Transciever was invalid."
            elif 'deleteTransceiver' in request.POST:
                Transceivers.objects.filter(id=request.POST['deleteTransceiver'])[0].delete()
            elif 'resetTransceivers' in request.POST:
                resetAllTransceivers()
        context['transceivers'] = Transceivers.objects.all()
        context['transceiversForm'] = TransceiversForm()
        return render_to_response('transceiver.html', context, context_instance=RequestContext(request))


@login_required
def transceiverSearch(request):
    if request.user.is_superuser:
        return searchForTransceiver()

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
    Transceivers.objects.all().delete()
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        ser.write('reset')
    except Exception, exc:
        print str(exc)
