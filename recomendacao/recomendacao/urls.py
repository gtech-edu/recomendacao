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
    
    url(r'^envia-texto-sobek/$', views.envia_texto_sobek, name='envia_texto_sobek'),
    
    url(r'^js/$', views.js, name='js'),
    url(r'^js-aux/$', views.js_aux, name='js_aux'),
    
    #admin
    url(r'^admin/', include(admin.site.urls)),
]
