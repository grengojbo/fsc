INSTALL
sudo pip install nose coverage
sudo pip install tddspry

sudo pip install -r http://github.com/grengojbo/fsc/raw/master/scripts/req.txt

create config file in home dir ~/.fsc.ini
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

chown freeswitch:root /etc/fsc.ini
chmod 660 /etc/fsc.ini

Добавляем пользователя
fs-api -c account -a create -u <username> -e <email> [-p <password> --enabled=<1|0> -t <tariff_id>] [first_name last_name]
    если указано -s dev то подключение к API будет от имени пользователя dev.example.com

Просмотр аккаунтов
    fs-api # все аккаунты
    fs-api --start=10 --limit=15 # все аккаунты с 10 по 25
    fs-api -s diller # все аккаунты для диллера diller
    fs-api -u <username> # просмотр аккаунта username

Добавляем новый номер телефона
    fs-api -c endpoint -a create -u <username> --phone=<phone> [-p <password> --enabled=<1|0>] [-s site]

Запись CDR
Если по каким либо причинам FreeSWITCH несмог передать CDR запись он сохраняет файлы в /opt/freeswitch/log/xml_cdr/
то для добавления Вы можете использовать fs-cdr скрипт