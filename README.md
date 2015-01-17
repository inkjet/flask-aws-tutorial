### Deploying a Flask application in AWS: An end-to-end tutorial

This is the code that goes along with the detailed writeup here:

https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80

It's an app that writes and reads from a database. Nothing earth shattering, but good for an intro to Flask.  It uses Amazon RDS for the database backend, but you can make things even simpler and use a local DB.

To tool around with the app directly, here's a quickstart guide. 

Clone this repo to your local machine. In the top level directory, create a virtual environment:
```
$ virtualenv flask-aws
$ source flask-aws/bin/activate
```
Now install the required modules:
```
$ pip install requirements.txt
```
Edit the config.py file to point to a local database.  Then run:
```
$ python db_create.py
```
And the tables are created.  Now you can launch the app:
```
$ python application.py
```
And point your browser to http://0.0.0.0:5000

You can write to the database:




