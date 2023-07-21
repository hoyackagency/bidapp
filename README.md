# bidapp
Start the VENV:
```
python3 -m venv env
source env/bin/activate
```

Install Requirements
`pip install -r requirements.txt`

To start the project 1st run:
`python manage.py migrate`

create an admin user:
`python manage.py createsuperuser`

Start the webserver:
`python manage.py runserver`

#Notes
To update Requirements:
`pip freeze > requirements.txt`

To push to Github
`git add .`
`git commit -m ""`
`git push origin main`

