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
    """
    Добавляем пользователя
    """
    con = ClietAPI(rest_url, options)
    args={'username': 'dil_lodoti', 'email': 'oleg.dolya@gmail.com', 'enabled': 'true', 'password': 'asdf3365756j9753', 'first_name': 'Олег', 'last_name': 'Доля'}
    res = con.save("post", '/account/', args)
    #args={'username': 'u089103004', 'email': 'example@lincom3000.com.ua', 'enabled': 'true',}
    #res = con.save("post", '/account/', args)
    #args={'enabled': 'true', 'first_name': 'hax nah'}
    #res = con.save("put", '/account/u089103000/', args)
    if res:
        print(res)

def delete_account(options, rest_url):
    """"""
    con = ClietAPI(rest_url, options)
    res = con.delete('/account/u089103004/')
    if res:
        print("Delete: {0}".format(res))

#----------------------------------------------------------------------
def post_payment(options, rest_url, pay_user, moneys, pay_details="", pay_date='2010-05-25 22:05:34'):
    """"""
    con = ClietAPI(rest_url, options)
    temp_txt = "".join([str(random.randint(0, 9)) for i in range(20)])
    pay_name = "add:::lincom3000:::payment:::{0}:::{1}".format(pay_user, temp_txt[0:7])
    pay_amount = Decimal(moneys)
    pay_transaction_id = "{0}X{1}".format(int(time.time()), temp_txt)
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

def get_payment(options, rest_url, account):
    con = ClietAPI(rest_url, options)
    mod_query = "/payment/query/{0}/{1}/".format('2010-05-24', '2010-05-26')
    res = con.search(mod_query)
    if res:
        #print("count: {0} cash: {1}".format(res.get("count"), res.get("payment").get("amount")))
        print("count: {0}".format(res.get("count")))
        print("next: {0}".format(res.get("next")))
        print("previous: {0}".format(res.get("previous")))
        for p in res.get("payment"):
            print("cash: {0}".format(p.get("amount")))
    #mod_query = "/payment/{0}/query/{1}/{2}/".format(account.get("accountcode").get('username'), '2010-05-25', '2010-05-26')
    #mod_query = "/payment/{0}/".format(account.get("accountcode").get('username'))
    mod_query = "/payment/"
    mod_query = '/payment/list/1274876663X48540537100116616803/'
    res = con.search(mod_query)
    print(res)
#----------------------------------------------------------------------
def post_endpoint(options, rest_url, pay_user, phone):
    """
    Добавлям номер телефона к акаунту
    """
    con = ClietAPI(rest_url, options)
    args={'phone': phone, 'username': pay_user, 'enable': 'true', 'password': '48337124', 'description': 'тестовый номер'}
    res = con.save("post", '/endpoint/', args)
    if res:
        print(res)

#----------------------------------------------------------------------
def get_endpoint(options, rest_url, phone):
    """"""
    con = ClietAPI(rest_url, options)
    res = con.search('/endpoint/phone/{0}/'.format(phone))
    #print(res)
    return res.get("phone")

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

    #print('User: {0}'.format(options.user))
    rest_url = "http://%s" % options.host

    #pay_user = 'u089103000'
    #pay_user = "dil_lodoti"
    pay_user = "oleg"
    #phone = "380895001010"
    #phone = "380895005055"
    #phone = "380895001111"
    #phone = "380895005050"
    phone = "380895005010"
    # Добавили акаунт
    #post_account(options, rest_url)
    # Добавляем деньги
    #post_payment(options, rest_url, pay_user, "10", pay_details="пробные деньги", pay_date='2010-06-24 01:05:34')

    # Смотрим акаунт
    #account = get_account_user(options, rest_url, username=pay_user)
    #print("cash: {0} username: {1}".format(account.get("cash"), account.get("accountcode").get('username')))
    post_endpoint(options, rest_url, pay_user, phone)
    #endpoint = get_endpoint(options, rest_url, phone)

    #print("phone: {0} username: {1} password {2} enable:{3} sip server:{4}".format(endpoint.get("uid"), endpoint.get('username'), endpoint.get('password'), endpoint.get('enable'), endpoint.get('sip_server')))
    #get_payment(options, rest_url, account)

    #get_account(options, rest_url)
    #delete_account(options, rest_url)

def mymain():
    d = "1,2,3,4,6"
    for i in eval(d):
        print("i: {0}".format(i))

if __name__=='__main__':
    main()
