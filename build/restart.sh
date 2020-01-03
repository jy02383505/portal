#!/bin/sh
echo 'start kill'
pids=`ps aux|grep '[f]usion_nova_uwsgi'|awk -F' ' '{print $2}'`
if [ "$pids" ];then
        kill -9 $pids
fi
echo 'stop end...'

cd /var/www/fusion_nova_portal
/root/.pyenv/versions/fusion_nova/bin/uwsgi --ini build/fusion_nova_uwsgi.ini --stats 0.0.0.0:1717 --stats-http &
echo 'restart end...'
