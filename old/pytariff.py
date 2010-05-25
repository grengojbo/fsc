from restful_lib import Connection
import simplejson
#import urllib
import os
from freeswitch import *


def get_tariff(tariff_id, phone):
    # Should also work with https protocols
    rest_user = "test.lincom3000.com.ua"
    rest_pass = "lSbv5sbhPfhsU9sNK4kC5"
    rest_url = "http://test.lincom3000.com.ua/api"

    conn = Connection(rest_url, username=rest_user, password=rest_pass)

    #nibble_rate
    t = "/tariff/%i/%s/" % (int(tariff_id), phone)
    response = conn.request_get(t, headers={'Accept':'text/json'})
    headers = response.get('headers')
    status = headers.get('status', headers.get('Status'))

    if status in ["200", 200]:
        body = simplejson.loads(response.get('body').encode('UTF-8'))
        return body.get('rate')
    else:
        return None

def fsapi(session, stream, env, args):

    stream.write("w00t!\n" + env.serialize())
    stream.write("tariff_id: %s\n" % args.get("tariff_id"))
    stream.write("phone: %s\n" % args.get("phone"))
    stream.write("nibble_rate: %s\n" % get_tariff(args.get("tariff_id"), args.get("phone")))

def handler(session, args):

    #session.answer()
    #session.setHangupHook(hangup_hook)
    #session.setInputCallback(input_callback)
    #session.execute("playback", session.getVariable("hold_music"))
    consoleLog("info", " tariff: " + session.getVariable("nibble_tariff") + "\n")
    consoleLog("info", " destination_number: " + session.getVariable("destination_number") + "\n")
    nibble_rate = get_tariff(session.getVariable("nibble_tariff"), session.getVariable("destination_number"))
    session.setVariable("nibble_rate", nibble_rate);


#conn.request_get("/search", args={'q':'Test'}, headers={'Accept':'text/json'})

#new_member['title'] = " on a stick"
#conn.request("/item", method="POST", args=simplejson.dumps(new_member))
#"POST", urllib.parse.urlencode({'status':status})) #Send the status
