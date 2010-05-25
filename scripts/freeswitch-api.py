#!/usr/bin/env python
#coding:utf-8
# Author:   --<>
# Purpose: 
# Created: 25.05.2010

import sys
import optparse 
import simplejson

#----------------------------------------------------------------------
def main():
    """
    """
    try:
        parser = optparse.OptionParser()
        #opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
        parser.add_option('-u', '--user', action="store", dest="user", help="Auth User Name", default="test")
        parser.add_option('-p', '--passwd', action="store", dest="passwd", help="Auth User Passwd", default="test")
        parser.add_option('-h', '--host', action="store", dest="host", help="Url API", default="test.examle.com")
        options, args = parser.parse_args()
        base_url = "http://%s/api/" % options.host
    except: 
        parser.print_help()
        sys.exit(2)
    print 'Query string:', options.user

if __name__=='__main__':
    main()