#coding: utf-8

from django.shortcuts import render
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.views.generic import View, TemplateView
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
from time import sleep

from recomendacao.forms import FormText
from recomendacao.serializers import SerializerText
from recomendacao.search import GoogleSearchCse, GoogleSearchCseMarkup, GoogleSearchCseSeleniumMarkupImg

from recomendacao.settings import BASE_DIR
from recomendacao.const import APP_NAME, ENCODING, CSE_ID


def strip_escape(text):
    text = strip_tags(text)
    #text = escape(text)
    return text

def encode_string(string):
    return string.encode(ENCODING)

def decode_string(string):
    return string.decode(ENCODING)

class TemplateViewContext(TemplateView):
    extra_context = {}
    
    def get_context_data(self, **kwargs):
        context = super(TemplateViewContext, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

class ViewBusca(View):
    template_name = None
    
    def get(self, request):
        form_text = FormText()
        
        context = {
            'form': form_text
        }
        context.update(csrf(request))
        return render(request, self.template_name, context)

def executa_sobek(text):
    sobek_path = os.path.join(BASE_DIR, 'misc', 'webServiceSobek_Otavio.jar')
    
    try:
        quoted_text = urllib.quote(text)
        sobek_command = ['java', '-Dfile.encoding=' + ENCODING, '-jar', encode_string(sobek_path), '-b', '-t', '"' + encode_string(quoted_text) + '"']
        sobek_output = subprocess.check_output(sobek_command)
    except subprocess.CalledProcessError:
        text += ' ' + text
        
        quoted_text = urllib.quote(text)
        sobek_command = ['java', '-Dfile.encoding=' + ENCODING, '-jar', encode_string(sobek_path), '-b', '-t', '"' + encode_string(quoted_text) + '"']
        sobek_output = subprocess.check_output(sobek_command)
    
    sobek_output = sobek_output.replace('\n', ' ')
    
    if len(sobek_output.split()) > 30:
        sobek_output = executa_sobek(sobek_output)
    
    return sobek_output

def executa_xgoogle(search_input, request):
    gs = GoogleSearchCseMarkup(search_input, user_agent=request.META['HTTP_USER_AGENT'], lang='pt-br', tld='com.br', cx=CSE_ID)
    results = gs.get_results()
    
    results_list = []
    for res in results:
        result_dict = OrderedDict()
        
        result_dict['title'] = res.title
        result_dict['url'] = res.url
        result_dict['snippet'] = res.desc
        
        result_dict['title_markup'] = res.title_markup
        result_dict['url_markup'] = res.url_markup
        result_dict['snippet_markup'] = res.desc_markup
        
        results_list.append(result_dict)
    
    return results_list

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

class EnviaTextoV2(APIView):
    def post(self, request, format=None):
        serializer = SerializerText(data=request.DATA)
        if serializer.is_valid():
            text = request.DATA['text']
            text = strip_escape(text)
            text = encode_string(text)
            
            response_data = {}
            
            
            sobek_output = self.run_sobek(text)
            search_input = sobek_output
            
            results_list = self.run_xgoogle(search_input, request)
            
            response_data['sobek_output'] = decode_string(sobek_output).split()
            response_data['results_list'] = results_list
            
            
            if request.accepted_renderer.format == 'html':
                text_hash = hashlib.sha224(text).hexdigest()
                
                response_data['text_hash'] = text_hash
                
                xml_response_data = serialize_render(response_data, XMLRenderer)
                self.create_response_data_file(xml_response_data, text_hash, XMLRenderer.format)
                
                json_response_data = serialize_render(response_data, JSONRenderer)
                self.create_response_data_file(json_response_data, text_hash, JSONRenderer.format)
            
            
            response = Response(response_data, status=status.HTTP_200_OK, template_name=os.path.join(APP_NAME, 'resultados-v2.html'))
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def run_sobek(self, text):
        sobek_path = os.path.join(BASE_DIR, 'misc', 'webServiceSobek_Otavio.jar')
        
        try:
            quoted_text = urllib.quote(text)
            sobek_command = ['java', '-Dfile.encoding=' + ENCODING, '-jar', encode_string(sobek_path), '-b', '-t', '"' + encode_string(quoted_text) + '"']
            sobek_output = subprocess.check_output(sobek_command)
        except subprocess.CalledProcessError:
            text += ' ' + text
            
            quoted_text = urllib.quote(text)
            sobek_command = ['java', '-Dfile.encoding=' + ENCODING, '-jar', encode_string(sobek_path), '-b', '-t', '"' + encode_string(quoted_text) + '"']
            sobek_output = subprocess.check_output(sobek_command)
        
        sobek_output = sobek_output.replace('\n', ' ')
        
        if len(sobek_output.split()) > 30:
            sobek_output = self.run_sobek(sobek_output)
        
        return sobek_output
    
    def run_xgoogle(self, search_input, request):
        gs = GoogleSearchCse(search_input, user_agent=request.META['HTTP_USER_AGENT'], lang='pt-br', tld='com.br', cx=CSE_ID)
        results = gs.get_results()
        
        results_list = []
        for res in results:
            result_dict = OrderedDict()
            
            result_dict['title'] = res.title
            result_dict['url'] = res.url
            result_dict['snippet'] = res.desc
            
            results_list.append(result_dict)
        
        return results_list
    
    def create_response_data_file(self, response_data, text_hash, file_format):
        filename = text_hash + '.' + file_format
        with open(os.path.join(BASE_DIR, 'files', filename), 'wb') as response_data_file:
            response_data_file.write(response_data)
            response_data_file.close()

class EnviaTextoV3(APIView):
    def post(self, request, format=None):
        serializer = SerializerText(data=request.DATA)
        if serializer.is_valid():
            text = request.DATA['text']
            text = strip_escape(text)
            text = encode_string(text)
            
            mode = request.DATA.get('mode')
            images = request.DATA.get('images')
            
            response_data = {}
            
            
            if mode == 'sobek':
                sobek_output = self.run_sobek(text)
                
                response_data['sobek_output'] = decode_string(sobek_output).split()
            elif mode == 'google':
                search_input = text
                
                results_list = self.run_xgoogle(search_input, request, images)
                
                response_data['results_list'] = results_list
            else:
                sobek_output = self.run_sobek(text)
                search_input = sobek_output
                
                results_list = self.run_xgoogle(search_input, request, images)
                
                response_data['sobek_output'] = decode_string(sobek_output).split()
                response_data['results_list'] = results_list
            
            
            if request.accepted_renderer.format == 'html':
                text_hash = hashlib.sha224(text).hexdigest()
                
                response_data['text_hash'] = text_hash
                
                xml_response_data = serialize_render(response_data, XMLRenderer)
                self.create_response_data_file(xml_response_data, text_hash, XMLRenderer.format)
                
                json_response_data = serialize_render(response_data, JSONRenderer)
                self.create_response_data_file(json_response_data, text_hash, JSONRenderer.format)
            
            
            response = Response(response_data, status=status.HTTP_200_OK, template_name=os.path.join(APP_NAME, 'resultados-v3.html'))
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def run_sobek(self, text):
        sobek_path = os.path.join(BASE_DIR, 'misc', 'webServiceSobek_Otavio.jar')
        
        try:
            quoted_text = urllib.quote(text)
            sobek_command = ['java', '-Dfile.encoding=' + ENCODING, '-jar', encode_string(sobek_path), '-b', '-t', '"' + encode_string(quoted_text) + '"']
            sobek_output = subprocess.check_output(sobek_command)
        except subprocess.CalledProcessError:
            text += ' ' + text
            
            quoted_text = urllib.quote(text)
            sobek_command = ['java', '-Dfile.encoding=' + ENCODING, '-jar', encode_string(sobek_path), '-b', '-t', '"' + encode_string(quoted_text) + '"']
            sobek_output = subprocess.check_output(sobek_command)
        
        sobek_output = sobek_output.replace('\n', ' ')
        
        if len(sobek_output.split()) > 30:
            sobek_output = self.run_sobek(sobek_output)
        
        return sobek_output
    
    def run_xgoogle(self, search_input, request, images):
        if not images:
            gs = GoogleSearchCseMarkup(search_input, user_agent=request.META['HTTP_USER_AGENT'], lang='pt-br', tld='com.br', cx=CSE_ID)
        else:
            gs = GoogleSearchCseSeleniumMarkupImg(search_input, user_agent=request.META['HTTP_USER_AGENT'], lang='pt-br', tld='com.br', cx=CSE_ID)
        results = gs.get_results()
        
        results_list = []
        for res in results:
            result_dict = OrderedDict()
            
            result_dict['title'] = res.title
            result_dict['url'] = res.url
            result_dict['snippet'] = res.desc
            
            result_dict['title_markup'] = res.title_markup
            result_dict['url_markup'] = res.url_markup
            result_dict['snippet_markup'] = res.desc_markup
            
            if images:
                result_dict['img'] = getattr(res, 'img', None)
            
            results_list.append(result_dict)
        
        return results_list
    
    def create_response_data_file(self, response_data, text_hash, file_format):
        filename = text_hash + '.' + file_format
        with open(os.path.join(BASE_DIR, 'files', filename), 'wb') as response_data_file:
            response_data_file.write(response_data)
            response_data_file.close()
