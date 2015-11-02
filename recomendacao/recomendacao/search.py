#coding: utf-8

import re
import urllib

from xgoogle.search import GoogleSearch, SearchError, ParseError
from recomendacao.browser import BrowserRequests, BrowserSelenium
from xgoogle.browser import BrowserError, BROWSERS
from xgoogle.BeautifulSoup import BeautifulSoup


class SearchResult(object):
    def __init__(self, title, url, desc):
        self.title = title
        self.url = url
        self.desc = desc

    def __str__(self):
        return 'Google Search Result: "%s"' % self.title

class SearchResultMarkup(SearchResult):
    def __init__(self, title, url, desc, title_markup, url_markup, desc_markup):
        super(SearchResultMarkup, self).__init__(title, url, desc)
        self.title_markup = title_markup
        self.url_markup = url_markup
        self.desc_markup = desc_markup


class GoogleSearchUserAgent(GoogleSearch):
    def __init__(self, query, user_agent=BROWSERS[0], debug=False, **kwargs):
        super(GoogleSearchUserAgent, self).__init__(query, **kwargs)
        self.browser = BrowserRequests(user_agent=user_agent, debug=debug)

class GoogleSearchUserAgentCse(GoogleSearchUserAgent):
    SEARCH_URL_0 = "http://cse.google.%(tld)s/cse?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
    NEXT_PAGE_0 = "http://cse.google.%(tld)s/cse?hl=%(lang)s&q=%(query)s&start=%(start)d"
    SEARCH_URL_1 = "http://cse.google.%(tld)s/cse?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
    NEXT_PAGE_1 = "http://cse.google.%(tld)s/cse?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"
    
    def __init__(self, query, cx=None, **kwargs):
        super(GoogleSearchUserAgentCse, self).__init__(query, **kwargs)
        self._cx = cx
        #self._nojs = '0' # The nojs parameter is no longer supported
    
    def _get_results_page(self):
        if self._page == 0:
            if self._results_per_page == 10:
                url = self.SEARCH_URL_0
            else:
                url = self.SEARCH_URL_1
        else:
            if self._results_per_page == 10:
                url = self.NEXT_PAGE_0
            else:
                url = self.NEXT_PAGE_1

        safe_url = [url % { 'query': urllib.quote_plus(self.query),
                           'start': self._page * self._results_per_page,
                           'num': self._results_per_page,
                           'tld' : self._tld,
                           'lang' : self._lang }]
        
        # possibly extend url with optional properties
        if self._first_indexed_in_previous:
            safe_url.extend(["&as_qdr=", self._first_indexed_in_previous])
        if self._filetype:
            safe_url.extend(["&as_filetype=", self._filetype])
        if self._cx:
            safe_url.extend(["&cx=", self._cx])
            #safe_url.extend(["&nojs=", self._nojs]) # The nojs parameter is no longer supported
        
        safe_url = "".join(safe_url)
        self._last_search_url = safe_url
        
        try:
            page = self.browser.get_page(safe_url)
        except BrowserError, e:
            raise SearchError, "Failed getting %s: %s" % (e.url, e.error)

        return BeautifulSoup(page)
    
    def _extract_results(self, soup):
        results = soup.findAll('div', {'class': 'g'})
        ret_res = []
        for result in results:
            eres = self._extract_result(result)
            if eres:
                ret_res.append(eres)
        return ret_res
    
    def _extract_description(self, result):
        desc_span = result.find('span', {'class': 's'})
        if not desc_span:
            self._maybe_raise(ParseError, "Description tag in Google search result was not found", result)
            return None
        
        desc = ''.join(desc_span.findAll(text=True))
        return self._html_unescape(desc)

class GoogleSearchUserAgentCseMarkup(GoogleSearchUserAgentCse):
    def _extract_result(self, result):
        title, url = self._extract_title_url(result)
        title_markup, url_markup = self._extract_title_url_markup(result)
        desc = self._extract_description(result)
        desc_markup = self._extract_description_markup(result)
        if not title or not url or not desc:
            return None
        return SearchResultMarkup(title, url, desc, title_markup, url_markup, desc_markup)
    
    def _extract_title_url_markup(self, result):
        #title_a = result.find('a', {'class': re.compile(r'\bl\b')})
        title_a = result.find('a')
        if not title_a:
            self._maybe_raise(ParseError, "Title tag in Google search result was not found", result)
            return None, None
        
        title = title_a.renderContents(encoding=None)
        title = self._html_unescape(title)
        
        url_div = result.find('span', {'class': 'a'})
        
        url = url_div.renderContents(encoding=None)
        match = re.match(r'/url\?q=(http[^&]+)&', url)
        if match:
            url = urllib.unquote(match.group(1))
        
        return title, url
    
    def _extract_description_markup(self, result):
        desc_span = result.find('span', {'class': 's'})
        if not desc_span:
            self._maybe_raise(ParseError, "Description tag in Google search result was not found", result)
            return None
        
        desc = desc_span.renderContents(encoding=None).replace('<br />', '')
        return self._html_unescape(desc)


class GoogleSearchUserAgentCseSelenium(GoogleSearchUserAgentCse):
    def __init__(self, query, user_agent=BROWSERS[0], debug=False, **kwargs):
        super(GoogleSearchUserAgentCseSelenium, self).__init__(query, **kwargs)
        self.browser = BrowserSelenium(user_agent=user_agent, debug=debug)
    
    def _extract_results(self, soup):
        results = soup.findAll('div', {'class': 'gs-webResult gs-result', 'data-vars': None})
        ret_res = []
        for result in results:
            eres = self._extract_result(result)
            if eres:
                ret_res.append(eres)
        return ret_res
    
    def _extract_description(self, result):
        desc_span = result.find('div', {'class': 'gs-bidi-start-align gs-snippet'})
        if not desc_span:
            self._maybe_raise(ParseError, "Description tag in Google search result was not found", result)
            return None
        
        desc = ''.join(desc_span.findAll(text=True))
        return self._html_unescape(desc)

class GoogleSearchUserAgentCseSeleniumMarkup(GoogleSearchUserAgentCseSelenium):
    def _extract_result(self, result):
        title, url = self._extract_title_url(result)
        title_markup, url_markup = self._extract_title_url_markup(result)
        desc = self._extract_description(result)
        desc_markup = self._extract_description_markup(result)
        if not title or not url or not desc:
            return None
        return SearchResultMarkup(title, url, desc, title_markup, url_markup, desc_markup)
    
    def _extract_title_url_markup(self, result):
        #title_a = result.find('a', {'class': re.compile(r'\bl\b')})
        title_a = result.find('a')
        if not title_a:
            self._maybe_raise(ParseError, "Title tag in Google search result was not found", result)
            return None, None
        
        title = title_a.renderContents(encoding=None)
        title = self._html_unescape(title)
        
        url_div = result.find('div', {'class': 'gs-bidi-start-align gs-visibleUrl gs-visibleUrl-long'})
        
        url = url_div.renderContents(encoding=None)
        match = re.match(r'/url\?q=(http[^&]+)&', url)
        if match:
            url = urllib.unquote(match.group(1))
        
        return title, url
    
    def _extract_description_markup(self, result):
        desc_span = result.find('div', {'class': 'gs-bidi-start-align gs-snippet'})
        if not desc_span:
            self._maybe_raise(ParseError, "Description tag in Google search result was not found", result)
            return None
        
        desc = desc_span.renderContents(encoding=None)
        return self._html_unescape(desc)

class GoogleSearchUserAgentCseSeleniumMarkupImages(GoogleSearchUserAgentCseSeleniumMarkup):
    def _extract_description_markup(self, result):
        desc_span = result.find('table', {'class': 'gsc-table-result'})
        if not desc_span:
            self._maybe_raise(ParseError, "Description tag in Google search result was not found", result)
            return None
        
        desc = desc_span.renderContents(encoding=None)
        return self._html_unescape(desc)


class GoogleSearchUserAgentHtml(GoogleSearchUserAgent):
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
