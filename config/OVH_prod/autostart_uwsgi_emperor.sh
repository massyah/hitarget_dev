# inject into /etc/rc.local
# /usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid hayssam --gid hayssam --daemonize /var/log/uwsgi-emperor.log

sudo /etc/init.d/rc.local start
