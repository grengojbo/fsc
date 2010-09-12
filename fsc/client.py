# -*- mode: python; coding: utf-8; -*-
import urllib2
from urllib2 import urlparse
import simplejson
from restfull.client import Connection

########################################################################
class ClietAPI():
    """"""

    #----------------------------------------------------------------------
    def __init__(self, base_url, options):
        """ Base URL for the store should be pretty self-explanatory. E.g. something like
            "http://api.linktel.com.ua/api"
            Only needs to enter the username/password if this class is going to tinker
             with things."""
        if base_url.endswith('/'):
            base_url = base_url[:-1]

        self.base_url = base_url
        # Split the given URL
        if base_url:
            self.conn = Connection(base_url, username=options.user, password=options.passwd)

    def _query_search(self, query, args={}):
        """Low-level content box query - returns the message and response headers from the server.
           You may be looking for Store.search instead of this."""

        passed_args = {}
        passed_args.update(args)
        return self.conn.request_get(query, args=passed_args, headers={'Accept':'text/json'})

    def save(self, metod, resource, args={}, body = None):
        """
        metod post or put
        """
        response = self.conn.request(resource, metod, args = args, body = body)
        headers = response.get('headers')
        status = headers.get('status', headers.get('Status'))

        if status in ['200', 200, '201', 201]:
            body = simplejson.loads(response.get('body').encode('UTF-8'))
            return body
        else:
            return False

    def delete(self, resource):
        """
        metod post or put
        """
        response = self.conn.request_delete(resource)
        headers = response.get('headers')
        status = headers.get('status', headers.get('Status'))

        if status in ['200', 200, '204', 204]:
            return True
        else:
            return False

    def search(self, query, args={}):
        """Performs a search query and simply returns the body of the response if successful
           - if there is an issue, such as a code 404 or 500, this method will return False.

           Use the _query_search_service method to get hold of
           the complete response in this case."""
        response = self._query_search(query, args)
        headers = response.get('headers')
        status = headers.get('status', headers.get('Status'))

        if status in ['200', 200, '204', 204]:
            body = simplejson.loads(response.get('body').encode('UTF-8'))
            return body
        else:
            return False


