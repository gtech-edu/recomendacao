#coding: utf-8

from django.shortcuts import render
from django.core.context_processors import csrf
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
import subprocess
import json

from recomendacao.forms import FormTexto
from recomendacao.serializers import SerializerTexto
from recomendacao.search import GoogleSearchUserAgentText

from recomendacao.settings import BASE_DIR
from recomendacao.const import APP_NAME


def render_pagina(request, destino):
    context = {}
    context.update(csrf(request))
    return render(request, destino, context)

def base(request):
    form_texto = FormTexto()
    
    context = {
        'form': form_texto
    }
    context.update(csrf(request))
    return render(request, APP_NAME + '/busca.html', context)

def resultados(request):
    request_body = json.loads(request.body.decode('utf8'))
    
    form_texto = FormTexto()
    
    context = {
        'form': form_texto
    }
    context.update(csrf(request))
    return render(request, APP_NAME + '/resultados.html', context)

def js(request):
    return render_pagina(request, APP_NAME + '/js/js.js')

def js_aux(request):
    return render_pagina(request, APP_NAME + '/js/js-aux.js')

def jquery_redirect_csrf(request):
    return render_pagina(request, APP_NAME + '/js/jquery.redirect.csrf.js')

def executa_sobek(texto):
    sobek_path = os.path.join(BASE_DIR, APP_NAME, 'files', 'webServiceSobek_Otavio.jar')
    sobek_output = subprocess.check_output([
        'java', '-jar', sobek_path.encode('latin1'), '-b', '-t', '"' + texto.encode('latin1') + '"'
    ])
    return sobek_output

def envia_texto_sobek(request):
    request_body = json.loads(request.body.decode('utf8'))
    
    texto = request_body['texto']
    sobek_output = executa_sobek(texto)
    
    response = {
        'texto': texto,
        'sobek_output': sobek_output.decode('latin1').split()
    }
    
    return HttpResponse(json.dumps(response), content_type="application/json")

class EnviaTexto(APIView):
    def post(self, request, format=None):
        serializer = SerializerTexto(data=request.DATA)
        if serializer.is_valid():
            texto = request.DATA['texto']
            sobek_output = executa_sobek(texto)
            
            gs = GoogleSearchUserAgentText(sobek_output.decode('latin1').encode('utf8'), user_agent=request.META['HTTP_USER_AGENT'], lang='pt-br')
            results = gs.get_results()
            
            results_list = []
            for res in results:
                result_dict = {}
                result_dict['titulo'] = res.title
                result_dict['link'] = res.url
                result_dict['snippet'] = res.desc
                results_list.append(result_dict)
            
            return Response(results_list, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
