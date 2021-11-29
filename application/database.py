import time
import logging
from environs import Env
import boto3
from botocore.config import Config


env = Env()
env.read_env()

logging.basicConfig(level=logging.INFO)

my_config = Config(
    region_name='us-east-2'
)

client = boto3.client('rds',
                      aws_access_key_id=env.str("AWS_ACCESS_KEY_ID"),
                      aws_secret_access_key=env.str("AWS_SECRET_ACCESS_KEY"),
                      config=my_config)


class AWSPostgreSQL():
    def __init__(self):
        logging.info('DB init start.')
        self.created = False
        self.db_create_response = {}
        self.exists_response = {}

        if not self.exists:
            self.create_db()

        # wait until db finishes creating
        while not self.available:
            logging.info(f'DB status is available?: {self.available}')
            time.sleep(10)

            logging.info('DB create finish.')

        logging.info('DB init complete.')

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
            VpcSecurityGroupIds=[env.str("AWS_DB_SECURITY_GROUP_ID"), ],
            EnableIAMDatabaseAuthentication=False,
            EnablePerformanceInsights=False,
            BackupRetentionPeriod=0
        )
        self.created = True
        logging.info('DB create start.')


    @property
    def exists(self):
        try:
            self.exists_response = client.describe_db_instances(
                DBInstanceIdentifier=env.str("AWS_INSTANCE")
            )
            logging.info(f'DB exist. Details: {self.exists_response}')
            exists = True

        except Exception as e:
            logging.error(e)
            exists = False

        return exists

    @property
    def available(self):
        available = False
        try:
            if self.exists and self.exists_response['DBInstances'][0]['DBInstanceStatus'] == 'available':
                available = True
        except Exception as e:
            logging.error(e)
            pass

        return available

    @property
    def uri(self):
        # 'postgresql://'+env.str("AWS_USER")+':'+env.str("AWS_PW")+'@'+env.str("AWS_SERVER")+':5432/'+env.str("AWS_DB")

        uri = 'postgresql://'+env.str("AWS_USER")+':'+env.str("AWS_PW")+'@'
        uri += self.exists_response['DBInstances'][0]['Endpoint']['Address']
        uri += ':5432/'+env.str("AWS_DB")

        return uri

