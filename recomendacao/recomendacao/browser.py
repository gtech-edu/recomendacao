#coding: utf-8

import socket
import urllib
import urllib2
import requests
import os
from selenium import webdriver

from xgoogle.browser import Browser, BrowserError, PoolHTTPHandler
from recomendacao.webdriver import ExistingSeleniumSession
from django.core.cache import caches

from recomendacao import config


class BrowserRequests(Browser):
    def get_page(self, url, data=None):
        #handlers = [PoolHTTPHandler]
        #opener = urllib2.build_opener(*handlers)
        #if data: data = urllib.urlencode(data)
        #request = urllib2.Request(url, data, self.headers)
        try:
            #response = opener.open(request)
            #return response.read()
            
            response = requests.get(url)
            return response.text
        except (urllib2.HTTPError, urllib2.URLError), e:
            raise BrowserError(url, str(e))
        except (socket.error, socket.sslerror), msg:
            raise BrowserError(url, msg)
        except socket.timeout, e:
            raise BrowserError(url, "timeout")
        except KeyboardInterrupt:
            raise
        except:
            raise BrowserError(url, "unknown error")

class BrowserSelenium(Browser):
    def get_page(self, url, data=None):
        #handlers = [PoolHTTPHandler]
        #opener = urllib2.build_opener(*handlers)
        #if data: data = urllib.urlencode(data)
        #request = urllib2.Request(url, data, self.headers)
        try:
            #response = opener.open(request)
            #return response.read()
            
            #browser = webdriver.PhantomJS(service_log_path=os.path.devnull)
            browser = self.open_browser()
            browser.get(url)
            page = browser.page_source
            #browser.quit()
            return page
        except (urllib2.HTTPError, urllib2.URLError), e:
            raise BrowserError(url, str(e))
        except (socket.error, socket.sslerror), msg:
            raise BrowserError(url, msg)
        except socket.timeout, e:
            raise BrowserError(url, "timeout")
        except KeyboardInterrupt:
            raise
        except:
            raise BrowserError(url, "unknown error")
    
    def open_browser(self):
        cache = caches['default']
        
        try:
            browser_data = cache.get('browser_data')
            config.browser = ExistingSeleniumSession(command_executor=browser_data['command_executor'], 
                                              desired_capabilities=browser_data['capabilities'], 
                                              session_id=browser_data['session_id'])
            config.browser.title
        except (TypeError, AttributeError, urllib2.URLError) as e:
            config.browser = webdriver.PhantomJS(service_log_path=os.path.devnull)
            browser_data = {
                'command_executor': config.browser.command_executor,
                'capabilities': config.browser.capabilities,
                'session_id': config.browser.session_id,
            }
            cache.set('browser_data', browser_data)
        
        return config.browser
