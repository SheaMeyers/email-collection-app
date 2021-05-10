# Email Collection App

This projects allows users to create a customizable webpage 
that allows them to collect emails from users or customers.
It also displays them in user friendly admin screen and 
allows them to be exported for easy usage.

## Quickstart instructions

1. Create a virtual environment (optional but recommended) https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

2. Install python requirements

```bash
pip install -r requirements.txt
```

3. Compile static resources

```bash
python manage.py collectstatic --no-input
```

4. Run migrations

```bash
python manage.py migrate
```

5. Run server

```bash
python manage.py runserver
```

6. The project should be running and accessible by going to localhost:8000
The home page will give further instructions for setting up an account


## Deploying to Heroku

This project also contains the configuration to be deploy to Heroku (https://devcenter.heroku.com/articles/django-app-configuration). 
If you created a project in Heroku you should only need to set the git upstream run git push heroku master in order for this project to be run on Heroku. 
For further instructions please reference Heroku documentation.
