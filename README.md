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

#Cron Jobs
Set up a CRON to trigger RSS feed updates at the desired interval:
`curl http://localhost:8000/parse-feed/`

#API Examples
`curl -X POST -H "Content-Type: application/json" -d '{"feed_entry_id": 47, "status": "decline"}' http://localhost:8000/view/`
`curl -X POST -H "Content-Type: application/json" -d '{"feed_entry_id": 50, "status": "accept"}' http://localhost:8000/view/`
`curl -L 'http://localhost:8000/view?recycle=true&feed_entry_id=49'`

Jobs

Create
`curl -X POST -H "Content-Type: application/json" -d '{"feed_entry":1,"status":"accept"}' http://localhost:8000/jobs/`

Read
`curl -X GET http://localhost:8000/jobs/`
`curl -X GET http://localhost:8000/jobs/1/`

Update
`curl -X PUT -H "Content-Type: application/json" -d '{"feed_entry":1,"status":"decline"}' http://localhost:8000/jobs/1/`

Delete
`curl -X DELETE http://localhost:8000/jobs/1/`

#Notes
To update Requirements:
`pip freeze > requirements.txt`

To push to Github
`git add .`
`git commit -m ""`
`git push origin main`

