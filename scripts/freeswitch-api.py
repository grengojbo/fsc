#!/usr/bin/env python
#coding:utf-8
# Author:   --<>
# Purpose:
# Created: 25.05.2010
from __future__ import print_function
import sys
import optparse
from decimal import Decimal
from fsc.client import ClietAPI
import time, datetime
import hashlib
import random

#----------------------------------------------------------------------
def get_account(options, rest_url):
    con = ClietAPI(rest_url, options)
    mod_name = "account"
    mod_query = "/%s/" % mod_name
    args={'start': 0, 'limit': 2}
    res = con.search(mod_query, args)
    if res:
        print("count: {0}".format(res.get("count")))
        print("next: {0}".format(res.get("next")))
        print("previous: {0}".format(res.get("previous")))

        accounts = res.get("accounts")
        for a in accounts:
            print("cash: {0} username: {1}".format(a.get("cash"), a.get("accountcode").get('username')))

def get_account_user(options, rest_url, username):
    con = ClietAPI(rest_url, options)
    res = con.search('/account/{0}/'.format(username))
    return res.get("accounts")

#----------------------------------------------------------------------
def post_account(options, rest_url):
    """"""
    con = ClietAPI(rest_url, options)
    args={'username': 'u089103000', 'email': 'example@lincom3000.com.ua', 'enabled': 'false', 'password': 'asdf3365756j9753', 'first_name': 'first', 'last_name': 'last'}
    res = con.save("post", '/account/', args)
    args={'username': 'u089103004', 'email': 'example@lincom3000.com.ua', 'enabled': 'true',}
    res = con.save("post", '/account/', args)
    args={'enabled': 'true', 'first_name': 'hax nah'}
    res = con.save("put", '/account/u089103000/', args)
    if res:
        print(res)

def delete_account(options, rest_url):
    """"""
    con = ClietAPI(rest_url, options)
    res = con.delete('/account/u089103004/')
    if res:
        print("Delete: {0}".format(res))

#----------------------------------------------------------------------
def post_payment(options, rest_url):
    """"""
    con = ClietAPI(rest_url, options)
    pay_user = 'u089103000'
    temp_txt = "".join([str(random.randint(0, 9)) for i in range(20)])
    pay_name = "add:::lincom3000:::payment:::{0}:::{1}".format(pay_user, temp_txt[0:7])
    pay_amount = Decimal("10.05")
    pay_transaction_id = "{0}X{1}".format(int(time.time()), temp_txt)
    pay_details = "fig pyftn xnj"
    pay_date = '2010-05-25 22:05:34'
    code = "".join(str(pay_user)).join(str(pay_amount)).join(str(pay_transaction_id)).join(str(pay_name)).join(str(options.user))
    mcode = hashlib.md5()
    mcode.update(code.upper())
    #mcode.hexdigest()
    args={'username': pay_user, 'name': pay_name, 'amount': str(pay_amount), 'transaction_id': pay_transaction_id, 'details': pay_details, 'pay_date': pay_date}
    #print("args: {0}".format(args))
    res = con.save("post", '/payment/', args)
    if res:
        if res.get("reason_code") == mcode.hexdigest() and res.get("success"):
            print("transaction: {0}".format(res.get("success")))
        else:
            print("transaction: {0} error".format(pay_transaction_id))

def get_payment(options, rest_url, accaunt):
    con = ClietAPI(rest_url, options)
    mod_query = "/payment/query/{0}/{1}".format('2010-05-24', '2010-05-25')
    res = con.search(mod_query, args)
    if res:
        print("count: {0}".format(res.get("count")))
        print("next: {0}".format(res.get("next")))
        print("previous: {0}".format(res.get("previous")))
    mod_query = "/payment/{0}/query/{1}/{2}".format('', '2010-05-24', '2010-05-25')
    res = con.search(mod_query, args)
#----------------------------------------------------------------------
def main():
    """
    """
    try:
        parser = optparse.OptionParser()
        parser.add_option('-u', '--user', action="store", dest="user", help="Auth User Name", default="test")
        parser.add_option('-p', '--passwd', action="store", dest="passwd", help="Auth User Passwd", default="test")
        parser.add_option('--host', action="store", dest="host", help="Url API", default="test.examle.com")
        options, args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(2)

    print('User: {0}'.format(options.user))
    rest_url = "http://%s/api" % options.host

    pay_user = 'u089103000'

    #get_account(options, rest_url)
    #post_account(options, rest_url)
    #delete_account(options, rest_url)
    post_payment(options, rest_url)
    accaunt = get_account_user(options, rest_url, username=pay_user)
    print("cash: {0} username: {1}".format(accaunt.get("cash"), accaunt.get("accountcode").get('username')))


if __name__=='__main__':
    main()
