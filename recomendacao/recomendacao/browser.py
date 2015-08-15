#coding: utf-8

import socket
import urllib
import urllib2
import os
from selenium import webdriver

from xgoogle.browser import Browser, BrowserError, PoolHTTPHandler


class BrowserSelenium(Browser):
    def get_page(self, url, data=None):
        #handlers = [PoolHTTPHandler]
        #opener = urllib2.build_opener(*handlers)
        #if data: data = urllib.urlencode(data)
        #request = urllib2.Request(url, data, self.headers)
        try:
            #response = opener.open(request)
            #return response.read()
            
            browser = webdriver.PhantomJS(service_log_path=os.path.devnull)
            browser.get(url)
            page = browser.page_source
            browser.quit()
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
