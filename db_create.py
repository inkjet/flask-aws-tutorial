import time
from environs import Env
import boto3
from botocore.config import Config

env = Env()
env.read_env()

my_config = Config(
    region_name='us-east-2'
)

client = boto3.client('rds',
                      aws_access_key_id=env.str("AWS_ACCESS_KEY_ID"),
                      aws_secret_access_key=env.str("AWS_SECRET_ACCESS_KEY"),
                      config=my_config)


class AWSPostgreSQL():
    def __init__(self):
        self.created = False
        self.db_create_response = {}
        self.exists_response = {}

        if not self.exists:
            self.create_db()

            # wait until db finishes creating

            while not self.available:
                print('avail: ', self.available)
                time.sleep(10)

    def create_db(self):
        self.db_create_response = client.create_db_instance(
            AllocatedStorage=10,
            DBInstanceClass='db.m6g.large',
            DBName=env.str("AWS_DB"),
            DBInstanceIdentifier=env.str("AWS_INSTANCE"),
            Engine='postgres',
            MasterUserPassword=env.str("AWS_PW"),
            MasterUsername=env.str("AWS_USER"),
            MultiAZ=False,
            PubliclyAccessible=True,
            VpcSecurityGroupIds=['sg-05cb5081bff60ae8a', ],
            EnableIAMDatabaseAuthentication=False,
            EnablePerformanceInsights=False,
            BackupRetentionPeriod=0
        )
        self.created = True
        print("DB creating.")

    @property
    def exists(self):
        try:
            self.exists_response = client.describe_db_instances(
                DBInstanceIdentifier=env.str("AWS_INSTANCE")
            )
            print(self.exists_response)
            exists = True

        except (client.exceptions.DBInstanceNotFoundFault, KeyError) as e:
            exists = False

        return exists

    @property
    def available(self):
        available = False
        try:
            if self.exists and self.exists_response['DBInstances'][0]['DBInstanceStatus'] == 'available':
                available = True
        except (client.exceptions.DBInstanceNotFoundFault, KeyError) as e:
            pass

        return available

    @property
    def uri(self):
        # 'postgresql://'+env.str("AWS_USER")+':'+env.str("AWS_PW")+'@'+env.str("AWS_SERVER")+':5432/'+env.str("AWS_DB")

        uri = 'postgresql://'+env.str("AWS_USER")+':'+env.str("AWS_PW")+'@'
        uri += self.exists_response['DBInstances'][0]['Endpoint']['Address']
        uri += ':5432/'+env.str("AWS_DB")

        return uri
