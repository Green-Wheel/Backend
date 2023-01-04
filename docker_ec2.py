# run script de python desde una github action. aquest script utilitza boto3 i amb ssm (funcio send_command) fem executar una comanda
import os
import boto3

command_cd = ['cd /home/ec2-user/']
command_create_dc_file = ["""echo "
        version: '3.9'
        services:
          backend-app:
            container_name: backend_app
            image: crismigo/greenwheel_backend:latest
            restart: always
            ports:
              - '80:8080'
            volumes:
                - ./migrations/bikes:/usr/src/app/api/bikes/migrations
                - ./migrations/users:/usr/src/app/api/users/migrations
                - ./migrations/bookings:/usr/src/app/api/bookings/migrations
                - ./migrations/chargers:/usr/src/app/api/chargers/migrations
                - ./migrations/chats:/usr/src/app/api/chats/migrations 
                - ./migrations/ratings:/usr/src/app/api/ratings/migrations
                - ./migrations/reports:/usr/src/app/api/reports/migrations
                - ./migrations/vehicles:/usr/src/app/api/vehicles/migrations
                - ./migrations/publications:/usr/src/app/api/publications/migrations
                 
            environment:
              DJANGO_SECRET_KEY: 'om%_rbj(rdm*t$dt^!q)2o(3uztqzxtmv361d@j0lpza+q#zd)'
              DJANGO_DATABASE_HOST: 'greenwheel-rds-pre.cvktoxcvbtpd.eu-west-1.rds.amazonaws.com'
              DJANGO_DATABASE_PORT: '5432'
              DJANGO_DATABASE_NAME: 'GreenWheelDB'
              DJANGO_DATABASE_USER: 'greenwheel'
              DJANGO_DATABASE_PASSWORD: """ + os.environ['DB_PASSWORD'] + """
              AWS_ACCESS_KEY_ID: """ + os.environ['AWS_ACCESS_KEY_ID'] + """
              AWS_SECRET_ACCESS_KEY: """ + os.environ['AWS_SECRET_ACCESS_KEY'] + """
              DEBUG_MODE: 'False'
              CORS_ALLOW_ALL_ORIGINS: 'True'
        " > docker-compose.yml"""]

command_run_docker_compose = ['sudo /usr/local/bin/docker-compose up -d']
command_pull_docker = ['sudo docker pull crismigo/greenwheel_backend:latest']
commands = command_cd + command_create_dc_file + command_pull_docker + command_run_docker_compose

access_key = os.getenv('AWS_ACCESS_KEY_ID')
access_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

session = boto3.session.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=access_secret_key,
    region_name='eu-west-1'
)

ssm_client = session.client('ssm')
response = ssm_client.send_command(
    InstanceIds=['i-0378d5026cfb1453b'],
    DocumentName="AWS-RunShellScript",
    Parameters=
    {
        'commands': commands
    },
)