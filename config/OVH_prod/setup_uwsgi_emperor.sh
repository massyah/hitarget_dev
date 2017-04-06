# create a directory for the vassals
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
# symlink from the default config directory to your config file
sudo ln -s /home/hayssam/hitarget_dev/config/OVH_prod/hitarget_uswgi.ini /etc/uwsgi/vassals/
# run the emperor
uwsgi --emperor /etc/uwsgi/vassals --uid hayssam --gid hayssam