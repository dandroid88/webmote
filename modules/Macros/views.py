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
    return render_to_response('macro.html', context, context_instance=RequestContext(request))

@login_required
def macros(request):
    context = {}
    if request.method == 'POST':
        if 'saveMacro' in request.POST:
            newMacro = Macros(macroName=request.POST['macroName'], user=request.user)
            newMacro.save()
            return redirect('/macro/' + str(newMacro.id) + '/')
        if 'deleteMacro' in request.POST:
            Macros.objects.filter(macroName=request.POST['deleteMacro'], user=request.user).delete()
        if 'runMacro' in request.POST:
            runMacro(request.POST['runMacro'], request.user)
    context['macros'] = Macro.objects.filter(before=False)
    return render_to_response('macros.html', context, context_instance=RequestContext(request))
