Simple Django application to manage (CRUD) users and their bank account data (IBAN).

# Bootstraping dev environment

- Run ```pip install -r requirements.txt```

# Setup *.env* file to define environment variables
  - `DEBUG` (default=False)
  - `SOCIAL_AUTH_ENABLED` (default=True)
    - Allow users to login via social account, this does not create new users.
  - `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` (default=None)
    - Should be set if `SOCIAL_AUTH_ENABLED=True` (see instruction below)
  - `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` (default=None)
    - Should be set if `SOCIAL_AUTH_ENABLED=True` (see instruction below)
   
  - Example `.env` file might look like this
    ```
      DEBUG=True
      DATABASE_URL=postgres://localhost/superman
    ```

- Run ```./manage.py migrate```
- Create super user ```./manage.py createsuperuser``` or load test users ```./manage.py loaddata test_users```
  - Password for all test users is ```superman!@#```
- Visit ```http://localhost:8000/``` and login with admin account or any of test users.

# Run tests
- ```./manage.py test```

# Run tests with coverage
- Install coverage package ```pip install coverage```
- ```coverage run manage.py test superman.apps.accounts -v 2```
- To see html report of coverage ```coverage html --omit="venv/*"``` and open ```index.html``` in browser

# How to obtain google app credentials
- Visit [Google Developer Console](https://console.developers.google.com)
- Create a new project
- Setup Consent Screen
- Create credentials for application type `Web Application`
- Set Authorized JavaScript origins to `http://localhost:8000`
- Set Authorized redirect URIs to `http://localhost:8000/complete/google-oauth2/`
- Copy Client ID and Secret Key
