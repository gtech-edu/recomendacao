#coding: utf-8

from {{ DOCKYARD_PKG }}.settings import *


DEBUG = False

ALLOWED_HOSTS.append('{{ DOCKYARD_HOSTNAME }}')

STATIC_URL = '{{ DOCKYARD_MOUNTPOINT | default() }}/static/'

FILES_URL = '{{ DOCKYARD_MOUNTPOINT | default() }}/files/'
