#coding: utf-8

from django.apps import AppConfig


class RecomendacaoConteudoAppConfig(AppConfig):
    name = u'recomendacao'
    verbose_name = u'Recomendação de Conteúdo'
    
    def ready(self): # startup code here
        pass
