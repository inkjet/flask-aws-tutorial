'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

import logging
from myapplication import application
from environs import Env

env = Env()
env.read_env()

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    logging.info('Start application.py')
    application.debug = True
    application.run()
    logging.info('Application run command complete.')
