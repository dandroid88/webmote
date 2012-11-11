from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from Scheduler.models import *

@login_required
def schedules(request):
    context = {}
    if request.method == 'POST':
        if 'newSchedule' in request.POST:
            newSchedule = Schedule_Form(request.POST)
            if newSchedule.is_valid():
                newSchedule = newSchedule.save(commit=False)
                newSchedule.active = True
                newSchedule.save()
        if 'deleteSchedule' in request.POST:
            Schedules.objects.filter(id=request.POST['deleteSchedule'])[0].delete()
    context['schedules'] = Schedules.objects.all()
    context['scheduleForm'] = Schedule_Form()
    return render_to_response('scheduler.html', context, context_instance=RequestContext(request))

@login_required
def schedule(request, id="0"):
    context = {}
    if request.method == 'POST':
        if 'newSchedlet' in request.POST:
            newSchedlet = Schedlet_Form(request.POST)
            if newSchedlet.is_valid():
                schedlet = newSchedlet.save(commit=False)
                schedlet.schedule = Schedules.objects.filter(id=id)[0]
                schedlet.save()
        if 'deleteSchedlet' in request.POST:
            Schedlet.objects.filter(id=request.POST['deleteSchedlet'])[0].delete()
    context['schedule'] = Schedules.objects.select_related().filter(id=id)[0]
    context['schedletForm'] = Schedlet_Form()
    return render_to_response('schedule.html', context, context_instance=RequestContext(request))

@login_required
def editActive(request, id="0"):
    if request.method == 'POST':
        activeState = simplejson.loads(request.raw_post_data)
        schedule = Schedules.objects.filter(id=id)[0]
        schedule.active = 1 if "True" in activeState else 0
        schedule.save()
        return HttpResponse(simplejson.dumps(activeState), mimetype='application/javascript')

def runSchedlet(request, id="0"):
    if '127.0.0.1' in request.META['REMOTE_ADDR']:
        schedlet = Schedlet.objects.filter(id=id)[0]
        if schedlet.schedule.active:
            schedlet.action.runAction()
        return HttpResponse(simplejson.dumps(''), mimetype='application/javascript')

 
