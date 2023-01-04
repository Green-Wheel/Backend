#!/bin/sh

# entrypoint.sh file of Dockerfile

# Section 1- Bash options
set -o errexit
set -o pipefail
set -o nounset
echo "Bash options set"
# Section 2: Health of dependent services
#postgres_ready() {
#    python << END
#import sys
#
#from psycopg2 import connect
#from psycopg2.errors import OperationalError
#
#try:
#    connect(
#        dbname="${DJANGO_POSTGRES_DATABASE}",
#        user="${DJANGO_POSTGRES_USER}",
#        password="${DJANGO_POSTGRES_PASSWORD}",
#        host="${DJANGO_POSTGRES_HOST}",
#        port="${DJANGO_POSTGRES_PORT}",
#    )
#except OperationalError:
#    sys.exit(-1)
#END
#}
#
#until postgres_ready; do
#  >&2 echo "Waiting for PostgreSQL to become available..."
#  sleep 5
#done
#>&2 echo "PostgreSQL is available"

# Section 3- Idempotent Django commands
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/inicial_data.json

# create service user
python manage.py loaddata fixtures/service_user.json

# create superuser
#python manage.py shell -c "from api.users.models import Users; Users.objects.create_superuser('admin', 'admin@example.com', '90np3AE7#IH&')"

exec "$@"