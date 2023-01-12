import glob
import os

files = glob.glob('api/*/migrations/*.py')
for f in files:

    if not f.endswith('__init__.py'):
        os.remove(f)
print("Migration files deleted")
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
os.system("python manage.py loaddata fixtures/inicial_data.json")
os.system("python manage.py loaddata fixtures/service_user.json")
os.system("python manage.py loaddata fixtures/contamination.json")
os.system('python manage.py shell -c "from api.users.models import Users; Users.objects.create_superuser(\'administration\', \'administration@example.com\', \'1234\')"')