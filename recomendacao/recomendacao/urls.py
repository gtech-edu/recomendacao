from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

from rest_framework.urlpatterns import format_suffix_patterns

import os

from recomendacao import views

from recomendacao.const import APP_NAME


api_urlpatterns = [
    url(r'^v2/post/$', views.EnviaTexto.as_view(), name='post'),
]
api_urlpatterns = format_suffix_patterns(api_urlpatterns)

urlpatterns = [
    # Examples:
    # url(r'^$', 'recomendacao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    #project
    url(r'^$', views.ViewBusca.as_view(template_name='busca.html'), name='base'),
    url(r'^v1/$', views.ViewBusca.as_view(template_name='busca.html'), name='busca'),
    url(r'^v2/$', views.ViewBusca.as_view(template_name='busca-post.html'), name='busca_post'),
    
    url(r'^envia-texto-sobek/$', views.envia_texto_sobek, name='envia_texto_sobek'),
    
    url(r'^js/$', TemplateView.as_view(template_name=os.path.join(APP_NAME, 'js', 'js.js')), name='js'),
    url(r'^js-aux/$', TemplateView.as_view(template_name=os.path.join(APP_NAME, 'js', 'js-aux.js')), name='js_aux'),
    url(r'^jquery.redirect.csrf.js$', TemplateView.as_view(template_name=os.path.join(APP_NAME, 'js', 'jquery.redirect.csrf.js')), name='jquery_redirect_csrf'),
    
    #admin
    url(r'^admin/', include(admin.site.urls)),
]
urlpatterns += api_urlpatterns
