from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from Custom_Remotes.models import *

@login_required
def bookmarkActions(request):
    context = {}
    context['devices'] = []
    for device in getAllowedDevices(request.user.id):
        device.commands = device.commands_set.all()
        context['devices'].append(device)
    context['macros'] = []
    macroNames = []
    for macro in Macros.objects.filter(user=request.user):
        if not macro.macroName in macroNames:
            context['macros'].append(macro)
            macroNames.append(macro.macroName)
    context['profiles'] = []
    profileNames = []
    for profile in Profiles.objects.filter(user=request.user):
        if not profile.profileName in profileNames:
            context['profiles'].append(profile)
            profileNames.append(profile.profileName)
    return render_to_response('bookmark_actions.html', context, context_instance=RequestContext(request))

@login_required
def bookmark(request, actionType, deviceID, commandID):
    context = {}
    context['name'] = performAction(request.user, actionType, deviceID, commandID)
    return render_to_response('bookmark.html', context, context_instance=RequestContext(request))
