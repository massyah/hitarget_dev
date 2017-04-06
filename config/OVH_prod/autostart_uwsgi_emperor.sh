# inject into /etc/rc.local
# /usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log

sudo /etc/init.d/rc.local start
