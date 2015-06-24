#coding: utf-8

from django.shortcuts import render
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.views.generic import View
from django.utils.html import strip_tags, escape

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer

import os
import subprocess
import json
import urllib
import hashlib
from collections import OrderedDict

from recomendacao.forms import FormText
from recomendacao.serializers import SerializerText
from recomendacao.search import GoogleSearchUserAgentText

from recomendacao.settings import BASE_DIR
from recomendacao.const import APP_NAME, ENCODING


def strip_escape(text):
    text = strip_tags(text)
    text = escape(text)
    return text

def encode_string(string):
    return string.encode(ENCODING)

def decode_string(string):
    return string.decode(ENCODING)

class ViewBusca(View):
    template_name = None
    
    def get(self, request):
        form_text = FormText()
        
        context = {
            'form': form_text
        }
        context.update(csrf(request))
        return render(request, os.path.join(APP_NAME, self.template_name), context)

def executa_sobek(text):
    sobek_path = os.path.join(BASE_DIR, 'misc', 'webServiceSobek_Otavio.jar')
    text = urllib.quote(encode_string(text))
    
    sobek_command = ['java', '-Dfile.encoding=' + ENCODING, '-jar', encode_string(sobek_path), '-b', '-t', '"' + encode_string(text) + '"']
    sobek_output = subprocess.check_output(sobek_command)
    return sobek_output

def serialize_render(data, renderer_class):
    renderer = renderer_class()
    return renderer.render(data)

def envia_texto_sobek(request):
    request_body = json.loads(request.body)
    
    text = request_body['text']
    text = strip_escape(text)
    
    sobek_output = executa_sobek(text)
    
    response = {
        'sobek_output': sobek_output.split()
    }
    
    return HttpResponse(json.dumps(response), content_type="application/json")

class EnviaTexto(APIView):
    def post(self, request, format=None):
        serializer = SerializerText(data=request.DATA)
        if serializer.is_valid():
            text = request.DATA['text']
            text = strip_escape(text)
            
            sobek_output = executa_sobek(text)
            
            gs = GoogleSearchUserAgentText(sobek_output, user_agent=request.META['HTTP_USER_AGENT'], lang='pt-br')
            results = gs.get_results()
            
            results_list = []
            for res in results:
                result_dict = OrderedDict()
                result_dict['title'] = res.title
                result_dict['url'] = res.url
                result_dict['snippet'] = res.desc
                results_list.append(result_dict)
            
            response_data = {
                'results_list': results_list
            }
            
            if request.accepted_renderer.format == 'html':
                text_hash = hashlib.sha224(encode_string(text)).hexdigest()
                
                xml_response_data = serialize_render(results_list, XMLRenderer)
                self.create_response_data_file(xml_response_data, text_hash, XMLRenderer.format)
                
                json_response_data = serialize_render(results_list, JSONRenderer)
                self.create_response_data_file(json_response_data, text_hash, JSONRenderer.format)
                
                response_data['text_hash'] = text_hash
                response_data['sobek_output'] = sobek_output.split()
                
            response = Response(response_data, status=status.HTTP_200_OK, template_name=os.path.join(APP_NAME, 'resultados.html'))
            
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def create_response_data_file(self, response_data, text_hash, file_format):
        filename = text_hash + '.' + file_format
        with open(os.path.join(BASE_DIR, 'files', filename), 'wb') as response_data_file:
            response_data_file.write(response_data)
            response_data_file.close()
