from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from Custom_Remotes.models import *

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
    context = {}
    context['newButton'] = True
    if request.method == 'POST':
        data = simplejson.loads(request.raw_post_data)
        print data
        name = data[4]
        icon = data[5]
        remote = Remote.objects.filter(id=remoteID)[0]
        if data[1] == 'device':
            device = Devices.objects.filter(name=data[2])[0]
            command = Commands.objects.filter(name=data[3], device=device)[0]
            newButton = Button(name=name, x=x, y=y, command=command, icon=icon, remote=remote)
            newButton.save()
        if data[1] == 'profile':
            profile = Profiles.objects.filter(profileName=data[2])[0]
            newButton = Button(name=name, x=x, y=y, profile=profile, icon=icon, remote=remote)
            newButton.save()
        if data[1] == 'macro':
            macro = Macros.objects.filter(macroName=data[2])[0]
            newButton = Button(name=name, x=x, y=y, macro=macro, icon=icon, remote=remote)
            newButton.save()
        return redirect('/remote/' + str(remoteID) + '/')
    context['buttonForm'] = ButtonForm()
    return render_to_response('button.html', context, context_instance=RequestContext(request))

@login_required
def runButton(request, buttonID):
    b = Button.objects.filter(id=buttonID)[0]
    if b.macro:
       runMacro(b.macro.macroName, request.user)
    if b.profile:
        loadProfile(b.profile.profileName)
    if b.command:
        runCommand(b.command.device.id, b.command.id)
    return HttpResponse(simplejson.dumps(''), mimetype='application/javascript')

@login_required
def commandButton(request, commandID):
    command = Commands.objects.filter(id=commandID)[0]
    device = command.device
    runCommand(device.id, command.id)
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
    commands = Commands.objects.filter(device=device)
    remote = Remote(name=device.name, style=1, user=request.user)
    numCommands = len(commands)
    print numCommands
    remote.rows = numCommands / 3
    if numCommands % 3:
        remote.rows += 1
    for row in range(0, remote.rows):
        buttons.append({})
        for col in range(0, 3):
            if row * 3 + col < numCommands:
                command = commands[row * 3 + col]
                buttons[row][col] = Button(name=command.name, icon='star', command=command, id='command/' + str(command.id))
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

