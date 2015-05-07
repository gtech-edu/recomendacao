from django.apps import AppConfig

class RecomendacaoConteudoAppConfig(AppConfig):
    name = 'recomendacao'
    verbose_name = "Recomendação de Conteúdo"
    
    def ready(self): # startup code here
        pass