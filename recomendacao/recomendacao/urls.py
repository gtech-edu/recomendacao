from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

from rest_framework.urlpatterns import format_suffix_patterns

import os

from recomendacao import views

from recomendacao.const import APP_NAME, CSE_ID


api_urlpatterns = [
    url(r'^v2/post/$', views.EnviaTexto.as_view(), name='post'),
]
api_urlpatterns = format_suffix_patterns(api_urlpatterns)

urlpatterns = [
    # Examples:
    # url(r'^$', 'recomendacao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    #project
    url(r'^$', views.TemplateViewContext.as_view(template_name=os.path.join(APP_NAME, 'inicio.html')), name='inicio'),
    url(r'^v1/$', views.ViewBusca.as_view(template_name=os.path.join(APP_NAME, 'busca.html')), name='v1'),
    url(r'^v2/$', views.ViewBusca.as_view(template_name=os.path.join(APP_NAME, 'busca-post.html')), name='v2'),
    
    url(r'^envia-texto-sobek/$', views.envia_texto_sobek, name='envia_texto_sobek'),
    
    url(r'^js/$', views.TemplateViewContext.as_view(template_name=os.path.join(APP_NAME, 'js', 'js.js'), extra_context={'CSE_ID': CSE_ID}), name='js'),
    url(r'^js-aux/$', views.TemplateViewContext.as_view(template_name=os.path.join(APP_NAME, 'js', 'js-aux.js')), name='js_aux'),
    url(r'^jquery.redirect.csrf.js$', views.TemplateViewContext.as_view(template_name=os.path.join(APP_NAME, 'js', 'jquery.redirect.csrf.js')), name='jquery_redirect_csrf'),
    
    #admin
    url(r'^admin/', include(admin.site.urls)),
]
urlpatterns += api_urlpatterns
