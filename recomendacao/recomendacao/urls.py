from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

from recomendacao import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'recomendacao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    #project
    url(r'^$', views.base, name='base'),
    url(r'^resultados/$', views.resultados, name='resultados'),
    
    url(r'^envia-texto-sobek/$', views.envia_texto_sobek, name='envia_texto_sobek'),
    url(r'^post/$', views.EnviaTexto.as_view(), name='post'),
    
    url(r'^js/$', views.js, name='js'),
    url(r'^js-aux/$', views.js_aux, name='js_aux'),
    url(r'^jquery.redirect.csrf.js$', views.jquery_redirect_csrf, name='jquery_redirect_csrf'),
    
    #admin
    url(r'^admin/', include(admin.site.urls)),
]
