#!/usr/bin/env python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 25.05.2010
from __future__ import print_function
import sys
import optparse 
from fsc.client import ClietAPI

#----------------------------------------------------------------------
def api_account(options):
    rest_url = "http://%s/api" % options.host
    
    con = ClietAPI(rest_url, options)
    #res = get_api("account", options)
    mod_name = "account"
    mod_query = "/%s/" % mod_name
    res = con.search(mod_query)
    if res:
        print("count: {0}".format(res.get("count")))
        accounts = res.get("accounts")
        for a in accounts:
            print("cash: {0} username: {1}".format(a.get("cash"), a.get("accountcode").get('username')))
    
#----------------------------------------------------------------------
def main():
    """
    """
    try:
        parser = optparse.OptionParser()
        #opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
        parser.add_option('-u', '--user', action="store", dest="user", help="Auth User Name", default="test")
        parser.add_option('-p', '--passwd', action="store", dest="passwd", help="Auth User Passwd", default="test")
        parser.add_option('--host', action="store", dest="host", help="Url API", default="test.examle.com")
        options, args = parser.parse_args()
    except: 
        parser.print_help()
        sys.exit(2)
    
    print('User: {0}'.format(options.user))
    api_account(options)

if __name__=='__main__':
    main()