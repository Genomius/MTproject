# coding: utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def home(request):
    return render_to_response(
        'home.html',
        {
            'request': request,
        },
        context_instance=RequestContext(request)
    )
