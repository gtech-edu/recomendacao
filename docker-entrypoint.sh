#!/bin/bash
j2 /templates/settings_local.py > ${DOCKYARD_SRVPROJ}/${DOCKYARD_PKG}/settings_local.py
j2 /templates/site.conf > /etc/apache2/sites-available/site.conf
a2ensite site.conf

python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

chown www-data:www-data ${DOCKYARD_SRVPROJ}

# Prepare log files and start outputting logs to stdout
touch ${DOCKYARD_SRVHOME}/logs/apache.log
touch ${DOCKYARD_SRVHOME}/logs/access.log
tail -n 0 -f ${DOCKYARD_SRVHOME}/logs/*.log &

# Start Apache process
echo Starting Apache... 
apache2ctl -D FOREGROUND
