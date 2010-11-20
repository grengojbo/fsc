INSTALL

pip install -r http://github.com/grengojbo/fsc/raw/master/scripts/req.txt

create config file /etc/fsc.ini
[default]
user = fsuser
host = example.com
passwd = password
pref = /api/
protocol = http

[dev]
user = dev.example.com
host = example.com
passwd = password
pref = /api/
protocol = http

[cdr]
base_url = http://example.com/api/
api_user = login
api_pass = password
cdr_dir = /opt/freeswitch/log/xml_cdr/
cdr_dir_410 = /opt/freeswitch/log/xml_cdr_410/

Добавляем пользователя
fs-api -c account -a create -u <username> -e <email> [-p <password> --enabled=<1|0> -t <tariff_id>] [first_name last_name]
    если указано -s dev то подключение к API будет от имени пользователя dev.example.com

run
fs-cdr