#coding: utf-8

from django.shortcuts import render
from django.core.context_processors import csrf
from django.http import HttpResponse

import os
import subprocess
import json

from recomendacao.forms import FormTexto

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
    return render(request, APP_NAME + '/base.html', context)

def js(request):
    return render_pagina(request, APP_NAME + '/js/js.js')

def js_aux(request):
    return render_pagina(request, APP_NAME + '/js/js-aux.js')

def envia_texto_sobek(request):
    request_body = json.loads(request.body.decode('utf8'))
    
    texto = request_body['texto']
    
    sobek_path = os.path.join(BASE_DIR, APP_NAME, 'files', 'webServiceSobek_Otavio.jar')
    sobek_output = subprocess.check_output([
        'java', '-jar', sobek_path.encode('latin1'), '-b', '-t', '"' + texto.encode('latin1') + '"'
    ])
    
    response = {
        'texto': texto,
        'sobek_output': sobek_output.decode('latin1').split()
    }
    
    return HttpResponse(json.dumps(response), content_type="application/json")
