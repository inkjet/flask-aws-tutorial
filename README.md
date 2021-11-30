### CI/CD deployment of a Flask application in AWS using RDS PostgreSQL as the database

## Technologies
Python 3.8, Flask, AWS RDS - PostgreSQL, GitHub, GitHub Actions, AWS Code Pipeline, AWS
Elastic Beanstalk

## Demo Videos

## Objective
To create a production quality web application deployment pipeline. This pipeline automatically
deploys a simple Flask application to AWS upon commit to the master branch on GitHub.

In addition, I’d compared GitHub Actions and AWS Code Pipeline by designing the pipeline with
each tool.

## Benefits
CI/CD eliminates change management pain and human error. With a process like this, code can be automatically tested and
deployed.

## Architecture

## About Elastic Beanstalk
According to the [documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html),
Elastic Beanstalk will create the following objects:

 - EC2 instance – An Amazon Elastic Compute Cloud (Amazon EC2) virtual machine configured to run web apps on the platform that you choose.
 - Instance security group – An Amazon EC2 security group configured to allow inbound traffic on port 80. This resource lets HTTP traffic from the load balancer reach the EC2 instance running your web app. By default, traffic isn't allowed on other ports.
 - Load balancer – An Elastic Load Balancing load balancer configured to distribute requests to the instances running your application. A load balancer also eliminates the need to expose your instances directly to the internet.
 - Load balancer security group – An Amazon EC2 security group configured to allow inbound traffic on port 80. This resource lets HTTP traffic from the internet reach the load balancer. By default, traffic isn't allowed on other ports.
 - Auto Scaling group – An Auto Scaling group configured to replace an instance if it is terminated or becomes unavailable.
 - Amazon S3 bucket – A storage location for your source code, logs, and other artifacts that are created when you use Elastic Beanstalk.
 - Amazon CloudWatch alarms – Two CloudWatch alarms that monitor the load on the instances in your environment and that are triggered if the load is too high or too low. When an alarm is triggered, your Auto Scaling group scales up or down in response.
 - AWS CloudFormation stack – Elastic Beanstalk uses AWS CloudFormation to launch the resources in your environment and propagate configuration changes. The resources are defined in a template that you can view in the AWS CloudFormation console.
 - Domain name – A domain name that routes to your web app in the form subdomain.region.elasticbeanstalk.com.

## Elastic Beanstalk Expectations for Flask
Elastic Beanstalk (EB) is particular in how your app is structured and named. To keep it simple, you are stuck with having 
the following stucture/naming. 

```
├── applicaion
│   ├── __init__.py
│   └── othercode.py
├── Pipfile.lock
└── application.py
```
Along with this structure, the application variable itself should be called application. To quote the documentation:

"Using application.py as the filename and providing a callable application object (the Flask object, in this case) allows 
EB to easily find your application's code. "

In theory you can change some of these names (the application.py for example can be set with the WSGIPath in app.config), 
but I found it to be more effort than it is worth. That being said, having many things named the same was also problematic.

This was by far the trickiest part of the whole pipeline. Flask would always run locally perfectly, but EB could not 
find/import the application to run. Many examples use just one application.py file, which is simple and easy.
However, no real world application would be one file, so I wanted to use a package structure, and that complicated 
everything. I am still a bit confused what exactly EB runs when it loads the application. It doesn't just run  `python 
application.py`. It requires that, but somewhere, gunicorn (the WSGI web server) also imports application using a call
similar to application:application, which confuses things when it has a both a module and packaged called application in the
structure. You would think an import would reference the package, but clearly this process works when only one script exists.
In any case, if you have a simple one-script app (no package), you can set the WSGIPath to "application.py", 
but if you have a package it has to be set to just "application". Somehow that magic lets it both run and gunicorn to 
correctly import it. 

## Pipeline Overview
GitHub Actions Pipeline Overview
1. Commit to the master branch of a GitHub repository (pull request ideally)
2. GitHub actions will then deploy the repository to Elastic Beanstalk. This creates the server environment.
3. GitHub actions will create the environment variables in the environment.
4. GitHub actions will re-deploy the repository to correctly start the application using the environment variables.
5. The Python application will create the database if it does not exist (and create any new tables).
6. Once the database is created, the application is ready to use via the Elastic Beanstalk endpoint.

## Database Considerations
Elastic Beanstalk does have the [option](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.db.html) 
to configure an integrated RDS DB instance as part of the deployment process.

However, I chose to manage the database within Python. Initially I chose Python for the level of control. I still like
this path, but looking back I'm not sure there is a significant difference between handling it myself in python vs 
using options in teh aws:rds:instance namespace. Using Python you have the full control of the rds client api, and I
don't believe all of those are available in the namespace. For example, in Python I was able to specify a security group, 
which ended up being a nice feature, to be able to have a static (not-auto-created) group. However, using the config
the groups might all create correctly if you have no need to have them static.

I chose PostgreSQL just because it is a nice option. 

# Configuration Considerations
The configs will cleanly allow you to change between local, dev, test, and prod environments.

Most configs are included in the .env file. I've included a template that you would just need to fill out and rename.
- You always need an APP_SECRET for Flask encryption.
- If you want to develop locally, you would need PostgreSQL installed, set LOCAL_DEVELOPMENT=True and include LOCAL_USER
and LOCAL_PW.
- To develop on AWS you need to set all of the AWS* variables.

When using GitHub Actions, you need to set up all of these 
[env variables](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment) 
within GitHub.


For this demo, I just used repository secrets and my master branch. You could easily use environments, but you would 
need to edit the main.yml and create different workflows for different branches + environment. 

Elastic Beanstalk knows what env vars to expect based on the .ebextensions > environment.config. This is nice for 
environment variables that might change but are not actually secret. Technically I don't think you need to have the placeholders
here since the .yml will create them upon deployment, but I kept them all for consistency. If you create a new env var
that isn't sensitive, you can only add it just in environment.config. If you add a new sensitive secret, you could add
it only within GitHub and within the last line of the .yml.

If you were going to use this in production, you would probably want to change some of the create_db options in database.py.

## How To Run Locally

1. Clone, or fork and clone this repo.
   git clone https://github.com/Karana316/flask-aws-tutorial

2. Configure your environment (commands run from flask_aws_tutorial folder)
   - I suggest using pipenv. You could use venv and install the requirements.txt just the same.
```
$ pipenv install
```
   - Note if you make changes in pipenv, re-lock the requirements.txt or remove it. Elasitc Beanstalk on Amazon Linux 2
    supports both, and the [precendence](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/python-configuration-requirements.html) order is requirements.txt and then Pipfile.lock.
```
$ pipenv lock -r > requirements.txt
```
   - [Install PostgreSQL](https://www.postgresqltutorial.com/install-postgresql-linux/) according to your OS and set up 
     a user and password (or use the default of your system user/pw)

   - Make sure your .env is filled out for local development  
     - LOCAL_DEVELOPMENT=True  
     - LOCAL_USER: User you create in local install of PostgreSQL/PGAdmin
     - LOCAL_PW: Password you create in local install of PostgreSQL/PGAdmin 

3. Run the application. View in your browser at http://127.0.0.1:5000.
```
$ pipenv shell
$ python application.py
```

## How To Run the app locally, but the db on AWS
Same steps as Locally, except make sure your .env is filled out for AWS development. Once you run the application, it will
take 5 minutes or so for the db to create in RDS.

- LOCAL_DEVELOPMENT=False
- AWS_USER: This can be anything. It is the user that will be created to connect to your db  
- AWS_PW: This can be anything. It is the password that will be created to connect to your db  
- AWS_DB: This can be anything. It will be the name of your database. Note there are naming restrictions, only letters and 
underscores I believe.
- AWS_INSTANCE: this can be anything, it will be the name of the instance your db will be created on. Note there are naming 
  restrictions, only letters and dashes I believe.
- AWS_SECRET_ACCESS_KEY: Create a programmatic user in IAM to get Access Key and ID. Make sure it has permissions to create
  RDS instances.
- AWS_ACCESS_KEY_ID:  Create a programmatic user in IAM to Access Key and ID. Make sure it has permissions to create
  RDS instances.
- AWS_DB_SECURITY_GROUP_ID: Create a security group, let's call it flask-aws-db-sg, in EC2 with an inbound rule for 
  PostgreSQL (port 5432) to accept traffic from your IP (outbound can be left to all traffic allowed). Set this variable 
  to the Security Group ID of the group.

## How To Run on AWS via GithubActions
1. Fork this repo
2. Set up environment/repository variables for all variables in the AWS step above.
   - Create another security group in EC2. Name it flask-aws-eb (if you name it something else, change it in 
     .ebextensions > app.config).
    Inbound rules should be HTTP for all traffic (outbound can be left to all traffic allowed).
   - Add a new inbound rule to the previously created to flask-aws-db-sg. This should be PostgreSQL (port 5432) rule using
     the newly created flask-aws-eb security group as the source.
3. Commit or pull request a change to the master branch. It will take 5-10 mins to set eveything up, and then you should
see the app and environment in Elastic Beanstalk and the db in RDS. From the environment in Elastic Beanstalk, you can
find the endpoint and/or Open the application from the left menu.

## How To Run on AWS via CodePipeline


## Future Improvements
I skipped two things that would be necessary for a production application.

1. The build step. I left this setp in GitHub actions, but the testing piece is commented out, so it isn't doing much
other than testing the install. Generally you would run unit tests in this step, but that is difficult to do with my current
setup. You don't want to test with the real database, so you would probably want to write tests against a local (to the
test runner) postgreSQL install or an in-memory SQLite db. This was just out of scope for this project.

2. The database migration. In the current code, the database tables either exist or they don't. It doesn't handle changes to 
existing tables. [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/index.html) does exist and should be used.

## Sources
I started this project by forking https://github.com/inkjet/flask-aws-tutorial, but ended up making significant changes 
to the Python structure. I looked to here for structure suggestions: https://github.com/cookiecutter-flask/

The GitHub actions came mainly from: https://python.plainenglish.io/deploy-a-python-flask-application-to-aws-elastic-beanstalk-55fb39f4903a
I only had to make the minor changes of excluding the test step and adding the environment creation step. 








