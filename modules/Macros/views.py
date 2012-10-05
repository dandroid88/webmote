from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from Macros.models import *

@login_required
def macro(request, num="0"):
    context = {}
    context['macro'] = Macro.objects.filter(id=int(num))[0]
    if request.method == 'POST':
        if 'addAction' in request.POST:
            action = Actions.objects.filter(id=request.POST['addAction'])[0]
            lastAction = context['macro']
            while lastAction.after:
                lastAction = lastAction.after
            newMacroAction = Macro(before=lastAction, action=action, name=action.name)
            newMacroAction.save()
            lastAction.after = newMacroAction
            lastAction.save()
        if 'deleteAction' in request.POST:
            action = Actions.objects.filter(id=request.POST['deleteAction'])[0].getSubclassInstance()
            action.before.after = action.after
            action.before.save()
            print action.id
            action.delete()

    # Populate current Actions within the macro
    # if the action has a device it should be displayed...
    context['currentActions'] = []
    action = context['macro']
    while action.after:
        action = action.after
        context['currentActions'].append(action)

    # Populate new action options
    context['devices'] = []
    for device in Devices.objects.all():
        device.actions = device.actions_set.all()
        context['devices'].append(device)
    device = Devices(name="Macros")
    device.actions = []
    for macro in Macro.objects.filter(before=None).exclude(id=int(num)):
        device.actions.append(macro)
    if device.actions:
        context['devices'].append(device)
    return render_to_response('macro.html', context, context_instance=RequestContext(request))

@login_required
def macros(request):
    context = {}
    if request.method == 'POST':
        if 'saveMacro' in request.POST:
            newMacro = Macro(name=request.POST['macroName'], visible=True)
            newMacro.save()
            return redirect('/macros/macro/' + str(newMacro.id) + '/')
        if 'deleteMacro' in request.POST:
            Macro.objects.filter(id=request.POST['deleteMacro']).delete()
        if 'runMacro' in request.POST:
            Macro.objects.filter(id=request.POST['runMacro'])[0].runAction()
    context['macros'] = Macro.objects.filter(before=None)
    return render_to_response('macros.html', context, context_instance=RequestContext(request))
