from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from Custom_Remotes.models import *

@login_required
def customRemotes(request):
    context = {}
    context['customRemotes'] = Remote.objects.all()
    context['devices'] = Devices.objects.all()
    return render_to_response('custom_remotes.html', context, context_instance=RequestContext(request))

@login_required
def autoRemotes(request):
    context = {}
    context['devices'] = Devices.objects.all()
    return render_to_response('auto_remotes.html', context, context_instance=RequestContext(request))

@login_required
def editButton(request, buttonID):
    context = {}
    if request.method == 'POST':
        if 'clearButton' in request.POST:
            b = Button.objects.filter(id=buttonID)[0]
            remoteID = b.remote.id
            b.delete()
            return redirect('/remote/' + str(remoteID) + '/')
    return render_to_response('button.html', context, context_instance=RequestContext(request))

@login_required
def newButton(request, remoteID, y, x):
    if request.method == 'POST':
        data = simplejson.loads(request.raw_post_data)
        actionID = data[0]
        name = data[1]
        icon = data[2]
        remote = Remote.objects.filter(id=remoteID)[0]
        action = Actions.objects.filter(id=actionID)[0]
        print action
        newButton = Button(name=name, x=x, y=y, action=action, icon=icon, remote=remote)
        newButton.save()
        return redirect('/remote/' + str(remoteID) + '/')

    context = {}
    context['newButton'] = True
    form = ButtonForm()
    formActions = []
    for action in Actions.objects.all():
        actualAction = action.getSubclassInstance()
        if hasattr(actualAction, 'visible'):
            if actualAction.visible:
                formActions.append(action.id)
        else:
            formActions.append(action.id)
    form.fields['action'].queryset = Actions.objects.filter(id__in=formActions)
    context['buttonForm'] = form
    
    return render_to_response('button.html', context, context_instance=RequestContext(request))

@login_required
def runButton(request, buttonID):
    b = Button.objects.filter(id=buttonID)[0]
    b.action.runAction()
    return HttpResponse(simplejson.dumps(''), mimetype='application/javascript')

@login_required
def remote(request, remoteID):
    context = {}
    context['edit'] = True
    remote = Remote.objects.filter(id=remoteID)[0]
    buttons = []
    assignedButtons = Button.objects.filter(remote=remote)
    for row in range(0, remote.rows):
        buttons.append({})
    for button in assignedButtons:
        buttons[button.y][str(button.x)] = button
    if not len(assignedButtons):
        context['no_assigned_buttons'] = True
    remote.buttons = buttons
    context['remote'] = remote
    return render_to_response('remote.html', context, context_instance=RequestContext(request))
    
@login_required
def deviceRemote(request, deviceID):
    context = {}
    buttons = []
    context['edit'] = False
    device = Devices.objects.filter(id=deviceID)[0]
    actions = Actions.objects.filter(device=device)
    remote = Remote(name=device.name, style=1, user=request.user)
    numActions = len(actions)
    remote.rows = numActions / 3
    if numActions % 3:
        remote.rows += 1
    for row in range(0, remote.rows):
        buttons.append({})
        for col in range(0, 3):
            if row * 3 + col < numActions:
                action = actions[row * 3 + col]
                buttons[row][col] = Button(name=action.name, icon='star', action=action, id=str(action.id))
    remote.buttons = buttons
    context['remote'] = remote
    return render_to_response('remote.html', context, context_instance=RequestContext(request))

@login_required
def remotes(request):
    context = {}
    if request.method == 'POST':
        if 'saveRemote' in request.POST:
            r = Remote(user=request.user)
            newRemote = RemoteForm(request.POST, instance=r)
            if newRemote.is_valid():
                newRemote.save()
        if 'deleteRemote' in request.POST:
            Remote.objects.filter(id=request.POST['deleteRemote']).delete()
            # delete related buttons here if nec.
    context['remotes'] = Remote.objects.filter(user=request.user)
    context['remoteForm'] = RemoteForm()
    return render_to_response('remotes.html', context, context_instance=RequestContext(request))

