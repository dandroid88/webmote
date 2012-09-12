from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from Macros.models import *

@login_required
def main(request):
    context = {}
    context['macros'] = Macros.objects.all()
    return render_to_response('macros.html', context, context_instance=RequestContext(request))

@login_required
def macro(request, num="0"):
    context = {}
    context['macro'] = Macro.objects.filter(id=int(num))[0]
    return render_to_response('macro.html', context, context_instance=RequestContext(request))
