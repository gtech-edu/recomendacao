#coding: utf-8

import re
import urllib

from xgoogle.search import GoogleSearch, ParseError
from xgoogle.browser import Browser, BROWSERS


class GoogleSearchUserAgent(GoogleSearch):
    def __init__(self, query, user_agent=BROWSERS[0], debug=False, **kwargs):
        super(GoogleSearchUserAgent, self).__init__(query, **kwargs)
        self.browser = Browser(user_agent=user_agent, debug=debug)

class GoogleSearchUserAgentHTML(GoogleSearchUserAgent):
    def _extract_title_url(self, result):
        title_h3 = result.find('h3', {'class': 'r'})
        title_a = result.find('a')
        if not title_a:
            self._maybe_raise(ParseError, "Title tag in Google search result was not found", result)
            return None, None
        
        url = title_a['href']
        match = re.match(r'/url\?q=(http[^&]+)&', url)
        if match:
            url = urllib.unquote(match.group(1))
            title_a['href'] = url
        
        title = unicode(title_h3)
        title = self._html_unescape(title)
        return title, url
    
    def _extract_description(self, result):
        desc_div = result.find('div', {'class': 's'})
        if not desc_div:
            self._maybe_raise(ParseError, "Description tag in Google search result was not found", result)
            return None
        
        desc = unicode(desc_div)
        return self._html_unescape(desc)

class GoogleSearchUserAgentText(GoogleSearchUserAgent):
    def _extract_description(self, result):
        desc_span = result.find('span', {'class': 'st'})
        if not desc_span:
            self._maybe_raise(ParseError, "Description tag in Google search result was not found", result)
            return None
        
        desc = ''.join(desc_span.findAll(text=True))
        return self._html_unescape(desc)
