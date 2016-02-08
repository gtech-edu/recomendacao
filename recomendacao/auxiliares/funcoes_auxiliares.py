#coding: utf-8

import os
import errno
import re
from HTMLParser import HTMLParser as hp


def is_float(string):
    try:
        float(string)  
    except (ValueError, TypeError):
        return False
    else:
        return True

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST or not os.path.isdir(path):
            raise

def request_referer(request):
    referer = request.META.get('HTTP_REFERER')
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    referer = u'/' + u'/'.join(referer[1:])
    return referer

def request_path_info(request):
    path_info = request.META.get('PATH_INFO')
    return path_info

# Substitui as vírgulas de um string por pontos.
def replace_comma_with_dot(string):
    try:
        string = string.replace(',','.');
    except (TypeError):
        pass
    return string;

# Substitui os pontos de um string por vírgulas.
def replace_dot_with_comma(string):
    try:
        string = string.replace('.',',');
    except (TypeError):
        pass
    return string;

def unescape_list(list_values):
    for index, value in enumerate(list_values):
        list_values[index] = hp().unescape(value)
