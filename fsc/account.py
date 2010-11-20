# -*- mode: python; coding: utf-8; -*-
from __future__ import print_function
import sys
import optparse
from decimal import Decimal
from fsc.client import ClietAPI
from restfull.client import Connection
import time, datetime
import hashlib
import random
import ConfigParser
PATH_CACHE = ".cache"

#----------------------------------------------------------------------
def view(account):
    if account.get('enabled'):
        enabled = 'enabled'
    else:
        enabled = 'disabled'
    print('Cash: {0}'.format(account.get('cash')))
    print(u'User: {0} [{1}]'.format(account.get('accountcode').get('username'), enabled))
    print(u'Tariff: {0} [{1}]'.format(account.get('tariff').get('name'), account.get('tariff').get('id')))
    print(u'User Name: {0} {1}'.format(account.get('accountcode').get('first_name'), account.get('accountcode').get('last_name')))
    print(u'Date create account: {0}'.format(account.get('accountcode').get('date_joined')))
    print(u'Email: {0}'.format(account.get('accountcode').get('email')))

#----------------------------------------------------------------------
def get(opt, conf, username=None, arg=None):
    """
    Просмотр аккаунтов
    fs-api # все аккаунты
    fs-api --start=10 --limit=15 # все аккаунты с 10 по 25
    fs-api -s diller # все аккаунты для диллера diller
    fs-api -u <username> # просмотр аккаунта username
    """
    url = "{2}://{0}{1}".format(conf.get(opt.section, 'host'),conf.get(opt.section, 'pref'),conf.get(opt.section, 'protocol'))
    con = Connection(url, username=conf.get(opt.section, 'user'), password=conf.get(opt.section, 'passwd'), path_cache=PATH_CACHE)
    args={'start': opt.start, 'limit': opt.limit}
    if username is not None:
        mod_query = "/account/{0}/".format(username)
        res = con.search(mod_query, args)
        #print("res:{0}".format(res))
        if res:
            view(res.get("accounts"))
        else:
            print('No account: {0}; status: {1}'.format(username,con.status))
    else:
        mod_query = "/account/"
        res = con.search(mod_query, args)
        #print(con.response)
        #print("res:{0}".format(res))
        if res:
            print("count: {0}".format(res.get("count")))
            print("next: {0}".format(res.get("next")))
            print("previous: {0}".format(res.get("previous")))

            accounts = res.get("accounts")
            for a in accounts:
                if a.get('enabled'):
                    enabled = 'enabled'
                else:
                    enabled = 'disabled'
                print("cash: {0}; tariff: [{4}] {5};  username: {1}({3}) {2}".format(a.get("cash"), a.get("accountcode").get('username'), enabled, a.get("accountcode").get('email'), a.get('tariff').get('id'), a.get('tariff').get('name')))
        else:
            print('No account, status: {0}'.format(con.status))

#----------------------------------------------------------------------
def create(opt, conf, username, first_name=None, last_name=None):
    """
    Добавляем пользователя
    fs-api -c account -a create -u <username> -e <email> [-p <password> --enabled=<1|0> -t <tariff_id>] [first_name last_name] # новый аккаунт
    """
    url = "{2}://{0}{1}".format(conf.get(opt.section, 'host'),conf.get(opt.section, 'pref'),conf.get(opt.section, 'protocol'))
    if opt.email == 'no':
        print('fs-api -c account -a create -u <username> -e <email> [-p <password> --enabled=<1|0> -t <tariff_id>] [first_name last_name]')
    else:

        if int(opt.enabled) == 1:
            enabled = 'true'
        else:
            enabled = 'false'
        args={'username': username, 'email': opt.email, 'enabled': enabled}
        if first_name is not None:
            args['first_name'] = first_name
        if last_name is not None:
            args['last_name'] = last_name
        if opt.password != 'no':
            args['password'] = opt.password
        #print(args)
        con = Connection(url, username=conf.get(opt.section, 'user'), password=conf.get(opt.section, 'passwd'), path_cache=PATH_CACHE)
        res = con.save("post", '/account/', args)
        if res:
            view(res)
        else:
            print('No create account: {0}; status: {1}'.format(username,con.status))

#----------------------------------------------------------------------
def update(opt, conf, username, arg):
    """
    обновление аккаунта
    fs-api -c account -a update -u <username> <key> <val>
    Пример:
        fs-api -c account -a update -u testuser first_name Neskaju
    """
    url = "{2}://{0}{1}".format(conf.get(opt.section, 'host'),conf.get(opt.section, 'pref'),conf.get(opt.section, 'protocol'))
    con = Connection(url, username=conf.get(opt.section, 'user'), password=conf.get(opt.section, 'passwd'), path_cache=PATH_CACHE)
    res = con.save('put', '/account/{0}/'.format(username), arg)

#----------------------------------------------------------------------
def delete(opt, conf, username):
    """
    Удаляем аккаунт
    fs-api -c account -a delete -u <username>
    """
    url = "{2}://{0}{1}".format(conf.get(opt.section, 'host'),conf.get(opt.section, 'pref'),conf.get(opt.section, 'protocol'))
    con = Connection(url, username=conf.get(opt.section, 'user'), password=conf.get(opt.section, 'passwd'), path_cache=PATH_CACHE)
    res = con.delete('/account/{0}/'.format(username))
    if res:
        print("Delete: {0}".format(res))
