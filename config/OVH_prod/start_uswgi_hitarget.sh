uwsgi --socket mysite.sock --wsgi-file test.py --chmod-socket=666 --module hitargetMVP.wsgi
