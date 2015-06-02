#coding: utf-8

from django.shortcuts import render
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from django.utils.html import strip_tags, escape

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from unidecode import unidecode

import os
import subprocess
import json
import requests
from urlparse import urljoin

from recomendacao.forms import FormTexto
from recomendacao.serializers import SerializerTexto
from recomendacao.search import GoogleSearchUserAgentText

from recomendacao.settings import BASE_DIR
from recomendacao.const import APP_NAME


def strip_escape(texto):
    texto = strip_tags(texto)
    texto = unidecode(texto)
    texto = escape(texto)
    return texto

class ViewBusca(View):
    template_name = None
    
    def get(self, request):
        form_texto = FormTexto()
        
        context = {
            'form': form_texto
        }
        context.update(csrf(request))
        return render(request, os.path.join(APP_NAME, self.template_name), context)

def executa_sobek(texto):
    sobek_path = os.path.join(BASE_DIR, APP_NAME, 'files', 'webServiceSobek_Otavio.jar')
    sobek_output = subprocess.check_output([
        'java', '-jar', sobek_path.encode('utf8'), '-b', '-t', '"' + texto.encode('utf8') + '"'
    ])
    return sobek_output.decode('utf8')

def envia_texto_sobek(request):
    request_body = json.loads(request.body)
    
    texto = request_body['texto']
    texto = strip_escape(texto)
    
    sobek_output = executa_sobek(texto)
    
    response = {
        'texto': texto,
        'sobek_output': sobek_output.split()
    }
    
    return HttpResponse(json.dumps(response), content_type="application/json")

class EnviaTexto(APIView):
    def post(self, request, format=None):
        serializer = SerializerTexto(data=request.DATA)
        if serializer.is_valid():
            texto = request.DATA['texto']
            texto = strip_escape(texto)
            
            sobek_output = executa_sobek(texto)
            
            gs = GoogleSearchUserAgentText(sobek_output, user_agent=request.META['HTTP_USER_AGENT'], lang='pt-br')
            results = gs.get_results()
            
            results_list = []
            for res in results:
                result_dict = {}
                result_dict['titulo'] = res.title
                result_dict['link'] = res.url
                result_dict['snippet'] = res.desc
                results_list.append(result_dict)
            
            response_data = {
                'results_list': results_list
            }
            
            return Response(response_data, status=status.HTTP_200_OK, template_name=os.path.join(APP_NAME, 'resultados.html'))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
