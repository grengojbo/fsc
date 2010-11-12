INSTALL

pip install -r http://github.com/grengojbo/fsc/raw/master/scripts/req.txt

create config file /etc/fsc.ini
[cdr]
base_url = http://example.com/api/
api_user = login
api_pass = password
cdr_dir = /opt/freeswitch/log/xml_cdr/
cdr_dir_410 = /opt/freeswitch/log/xml_cdr_410/

run
fscdr