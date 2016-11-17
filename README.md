Simple Django application to manage (CRUD) users and their bank account data (IBAN).

# Bootstraping dev environment

- Run ```pip install -r requirements.txt```
- Create a PostgreSQL database named ```superman``` or define ```DATABASE_URL``` environment variable
- Run ```./manage.py migrate```
- Create super user ```./manage.py createsuperuser``` or load test users ```./manage.py loaddata test_users```
  - Password for all test users is ```superman!@#```
- Visit ```http://localhost:8000/``` and login with admin account or any of test users.
