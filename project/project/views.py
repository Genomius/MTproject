# coding: utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from settings import YANDEX_TRANSLATE_API_KEY
from django.views.decorators.csrf import ensure_csrf_cookie
import urllib2


@ensure_csrf_cookie
@xframe_options_exempt
def home(request):
    if request.POST:
        if request.is_ajax():
            url = 'https://translate.yandex.net/api/v1.5/tr/detect?key=%s&text=%s' % \
                   (YANDEX_TRANSLATE_API_KEY, request.body)
            lang = urllib2.urlopen(url).read().split('lang="')[1].split('"')[0]

            if lang == 'ru':
                return JsonResponse({'russian': 'Текст песни и так на русском языке!'})
            elif lang == '':
                return JsonResponse({'error': 'Не удалось перевести текст песни'})
            else:
                url = 'https://translate.yandex.net/api/v1.5/tr/translate?key=%s&lang=%s-ru&text=%s' % \
                      (YANDEX_TRANSLATE_API_KEY, lang, request.body)
                result = urllib2.urlopen(url).read()

                return JsonResponse({'result': result})
        else:
            return HttpResponseBadRequest({'error': 'error'})
    else:
        return render_to_response(
            'home.html',
            {
                'request': request,
            },
            context_instance=RequestContext(request)
        )


@ensure_csrf_cookie
def translate(request):
    if request.POST:
        if request.is_ajax():
            url = 'http://www.amalgama-lab.com/songs/r/rammstein/ich_will.html'
            result = urllib2.urlopen(url).read()
            print result
            return JsonResponse({'result': result})
        else:
            return HttpResponseBadRequest({'error': 'is not ajax'})
    else:
        return HttpResponseBadRequest({'error': 'method is not POST'})