# run script de python desde una github action. aquest script utilitza boto3 i amb ssm (funcio send_command) fem executar una comanda
import os
import boto3

commands_crate_dc_file = ["""echo "
        version: '3.9'
        services:
          backend-app:
            container_name: backend_app
            image: crismigo/greenwheel_backend:latest
            restart: always
            ports:
              - '80:8080'
            environment:
              DJANGO_SECRET_KEY: 'om%_rbj(rdm*t$dt^!q)2o(3uztqzxtmv361d@j0lpza+q#zd)'
              DJANGO_DATABASE_HOST: 'cloudformation-stack.ccvipjjamp2m.eu-west-1.rds.amazonaws.com'
              DJANGO_DATABASE_PORT: '5432'
              DJANGO_DATABASE_NAME: 'GreenWheelDB'
              DJANGO_DATABASE_USER: 'greenwheel'
              DJANGO_DATABASE_PASSWORD: """ + os.getenv('DB_PASSWORD') + """
              AWS_ACCESS_KEY_ID: """ + os.getenv('AWS_ACCESS_KEY_ID') + """
              AWS_SECRET_ACCESS_KEY: """ + os.getenv('AWS_SECRET_ACCESS_KEY') + """
              DEBUG_MODE: 'False'
              CORS_ALLOW_ALL_ORIGINS: 'True'
        " > docker-compose.yml"""]

commands_run_docker_compose = ['sudo /usr/local/bin/docker-compose up -d']

commands = commands_crate_dc_file + commands_run_docker_compose

access_key = os.getenv('AWS_ACCESS_KEY_ID')
access_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

session = boto3.session.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=access_secret_key
)

ssm_client = session.client('ssm')
response = ssm_client.send_command(
    InstanceIds=['i-05ff6135c2643fd05'],
    DocumentName="AWS-RunShellScript",
    Parameters=
    {
        'commands': commands
    },
)

command_id = response['Command']['CommandId']
output = ssm_client.get_command_invocation(
    CommandId=command_id,
    InstanceId='i-05ff6135c2643fd05',
)
print(output)
