# -*- mode: python; coding: utf-8; -*-
from __future__ import print_function
from restfull.client import Connection

PATH_CACHE = ".cache"

#----------------------------------------------------------------------
def view(endpoint):
    if endpoint.get('enable'):
        enabled = 'enabled'
    else:
        enabled = 'disabled'
    print('Phone: {0}'.format(endpoint.get('uid')))
    print(u'User: {0} [{1}]'.format(endpoint.get('username'), enabled))
    print('Password: {0}'.format(endpoint.get('password')))
    print(u'Caller Name: {0}'.format(endpoint.get('effective_caller_id_name')))
    #print('Date create account: {0}'.format(.get('accountcode').get('date_joined')))
    #print('Email: {0}'.format(.get('accountcode').get('email')))

#----------------------------------------------------------------------
def get(opt, conf, arg=None):
    """
    просмотр номера телефона
    fs-api -c endpoint -u <username> # все телефонные номера для аккаунта username
    fs-api -c endpoint -u <username> --start=10 --limit=15 # все телефоны с 10 по 25
    """
    # TODO: доделать пока неработает
    url = "{2}://{0}{1}".format(conf.get(opt.section, 'host'),conf.get(opt.section, 'pref'),conf.get(opt.section, 'protocol'))
    con = Connection(url, username=conf.get(opt.section, 'user'), password=conf.get(opt.section, 'passwd'), path_cache=PATH_CACHE)
    args={'start': opt.start, 'limit': opt.limit}
    if opt.username is not None:
        mod_query = "/endpoint/{0}/".format(opt.username)
        res = con.search(mod_query, args)
        #print("res:{0}".format(res))
        if res:
            view(res.get("accounts"))
        else:
            print('No account: {0}; status: {1}'.format(username,con.status))
    else:
        mod_query = "/endpoint/"
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
                print("phone: {0}; password: {1}({2})".format(a.get("uid"), a.get('password'), enabled))
        else:
            print('No endpoint, status: {0}'.format(con.status))

#----------------------------------------------------------------------
def create(opt, conf, username, phone="no"):
    """
    Добавляем новый номер телефона
    fs-api -c endpoint -a create -u <username> --phone=<phone> [-p <password> --enabled=<1|0>] [-s site]
    """
    url = "{2}://{0}{1}".format(conf.get(opt.section, 'host'),conf.get(opt.section, 'pref'),conf.get(opt.section, 'protocol'))
    #TODO: если неуказан номер то берет первый из списка
    if phone == 'no':
        print('fs-api -c endpoint -a create -u <username> --phone=<phone> [-p <password> --enabled=<1|0>] [-s site]')
    else:
        if int(opt.enabled) == 1:
            enabled = 'true'
        else:
            enabled = 'false'
        args={'username': username, 'phone': phone, 'enabled': enabled}
        #if first_name is not None:
        #    args['first_name'] = first_name
        #if last_name is not None:
        #    args['last_name'] = last_name
        if opt.password != 'no':
            args['password'] = opt.password
        #print(args)
        con = Connection(url, username=conf.get(opt.section, 'user'), password=conf.get(opt.section, 'passwd'), path_cache=PATH_CACHE)
        res = con.save("post", '/endpoint/', args)
        if res:
            view(res)
        else:
            print('No create endpoint: {0}; status: {1}'.format(opt.phone,con.status))

#----------------------------------------------------------------------
def update(opt, conf, arg):
    """
    обновление параметров телефонного номера
    fs-api -c endpoint -a update --phone <phone> <key> <val>
    Пример:
        fs-api -c endpoint -a update --phone 380895000000 effective_caller_id_name Neskaju
    """
    url = "{2}://{0}{1}".format(conf.get(opt.section, 'host'),conf.get(opt.section, 'pref'),conf.get(opt.section, 'protocol'))
    con = Connection(url, username=conf.get(opt.section, 'user'), password=conf.get(opt.section, 'passwd'), path_cache=PATH_CACHE)
    res = con.save('put', '/endpoint/phone/{0}/'.format(opt.phone), arg)
    if res:
        view(res)
    else:
        print('No update endpoint: {0}; status: {1}'.format(opt.phone,con.status))

#----------------------------------------------------------------------
def delete(opt, conf, username):
    """
    Деактивируем телефон
    fs-api -c endpoint -a delete --phone <phone>
    """
    url = "{2}://{0}{1}".format(conf.get(opt.section, 'host'),conf.get(opt.section, 'pref'),conf.get(opt.section, 'protocol'))
    con = Connection(url, username=conf.get(opt.section, 'user'), password=conf.get(opt.section, 'passwd'), path_cache=PATH_CACHE)
    res = con.delete('/endpoint/phone/{0}/'.format(opt.phone))
    if res:
        print("Delete: {0}".format(res))
